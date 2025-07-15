"""
This file contains functions that deal with natural language processing of a 
NVDA earnings call transcript. 
"""

import re
from typing import List

import os
from dotenv import load_dotenv
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

from transformers import pipeline

import time

_finbert = pipeline(
    "sentiment-analysis",
    model="yiyanghkust/finbert-tone",
    top_k=None,
    truncation=True,
    max_length=512) 

_LABEL2VAL = {"positive": 1.0, "negative": -1.0, "neutral": 0.0,
              "Positive": 1.0, "Negative": -1.0, "Neutral": 0.0}


_END_PUNCT = re.compile(r"(?<=[.!?])\s+")
load_dotenv()

_QA_CUE = re.compile(
    r"""(?imx)               # i = ignorecase, m = multiline, x = verbose
    ^\s*                     # start of a line
    (?:                      # ---- 1) explicit Q&A heading
        Q\s*&\s*A |
        Questions?\s*&\s*Answers? |
        Question[-\s]*and[-\s]*Answer(?:s)?\s*(?:Session)?
    )
    \s*$                     # end of that **same** line
    |                        # ---- OR ----
    ^\s*Operator:[^\n]*\b    # start of a line that begins "Operator:"
        (?:begin|start|open|take|get)\b[^\n]*\bquestion
    """,
)

_MAX_CHARS = 70000 

kw_model = KeyBERT(SentenceTransformer("all-MiniLM-L6-v2"))

# regex helpers
_META_JSON   = re.compile(r"\{[^{}]*}")                         # {"company": …}
_BRACKET_TAG = re.compile(r"\[.*?]")                            # [Operator …]
_SPEAKER     = re.compile(r"\b[A-Z][A-Za-z .'-]{2,40}:\s")      # Operator:, Jensen:

def preprocess(text: str) -> str:
    """Remove API scaffolding and normalise whitespace."""
    text = _META_JSON.sub(" ", text)      
    text = _BRACKET_TAG.sub(" ", text)  
    text = _SPEAKER.sub("", text)       
    text = re.sub(r"\s+", " ", text)  
    text = text.encode("ascii", "ignore").decode()
    return text.strip()


def split_sentences(text: str) -> List[str]:    
    return [s.strip() for s in _END_PUNCT.split(text) if s.strip()]


def _chunks(text, size=_MAX_CHARS):
    for i in range(0, len(text), size):
        yield text[i : i + size]

def split_management_qa(resp: dict) -> tuple[str, str]:
    """
    Return (prepared, qa).
    Uses `transcript_split` when present (premium tier);
    otherwise falls back to a plain‑text search for '"role":"Analyst"'.
    """
    split = resp.get("transcript_split")

    # ---- preferred: structured list ---------------------------------
    if split:
        for idx, seg in enumerate(split):
            if (seg.get("role") or "").lower() == "analyst":
                prep = " ".join(s["text"] for s in split[:idx]).strip()
                qa   = " ".join(s["text"] for s in split[idx:]).strip()
                return prep, qa
        # no analyst block found
        return " ".join(s["text"] for s in split).strip(), ""

    # ---- fallback: free‑tier raw string -----------------------------
    txt = resp.get("transcript", "")
    m = re.search(r'(?i)"role"\s*:\s*"analyst"', txt)
    if m:
        return txt[:m.start()].rstrip(), txt[m.start():].lstrip()
    return txt, ""



def run_sentiment(text: str) -> float:

    scores = []

    for chunk in _chunks(text, size=2000): 
        chunk_start_time = time.time()

        result = _finbert(chunk[:512])[0]    

        s = sum(_LABEL2VAL[d["label"]] * d["score"] for d in result)



        scores.append(s)

    return sum(scores) / len(scores)

def extract_keywords(text: str, top_n: int = 10):
    kws = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 3),
        stop_words=None,
        top_n=top_n
    )
    return [{"phrase": k, "score": round(s,3)} for k,s in kws]