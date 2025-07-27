"""
This file contains functions that deal with natural language processing of a 
NVDA earnings call transcript. 
"""

import re
from typing import List
import os
import json


from dotenv import load_dotenv
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
import google.generativeai as genai


from transformers import pipeline

from fastapi import HTTPException       


_finbert = pipeline(
    "sentiment-analysis",
    model="yiyanghkust/finbert-tone",
    top_k=None,
    truncation=True,
    max_length=512) 

_LABEL2VAL = {"positive": 1.0, "negative": -1.0, "neutral": 0.0}


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
genai.configure(api_key=os.getenv("GOOGLE_GEMINI_KEY"))
_GEMINI = genai.GenerativeModel("gemini-1.5-flash")

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
    split = resp.get("transcript_split")
    if split:
        issuer = next(
            (seg.get("company") for seg in split if seg.get("company")), ""
        ).lower()

        for idx, seg in enumerate(split):
            comp = (seg.get("company") or "").lower()
            if issuer and comp and comp != issuer:
                prepared = " ".join(s["text"] for s in split[:idx]).strip()
                qa       = " ".join(s["text"] for s in split[idx:]).strip()
                return prepared, qa

        return " ".join(s["text"] for s in split).strip(), ""

    txt = resp.get("transcript", "")
    m = re.search(r'(?i)(question[- ]and[- ]answer|q[&/]a|begin the q&a)', txt)
    if m:
        return txt[:m.start()].rstrip(), txt[m.start():].lstrip()
    return txt, ""

def run_sentiment(text: str) -> float:

    scores = []

    for chunk in _chunks(text, size=2000): 
        result = _finbert(chunk[:512])[0]    

        s = sum(_LABEL2VAL[d["label"].lower()] * d["score"] for d in result)

        scores.append(s)

    if len(scores) == 0:
        raise HTTPException(
            status_code=404,
            detail="FinBERT returned no scores for this transcript. I am on a free version, so sometimes the transcript becomes unavailable :("
        )

    return sum(scores) / len(scores)

def extract_keywords(text: str, top_n: int = 3):
    prompt = f"""
        You are a discerning financial analyst. 
        Read the following chunk of a transcript from an earnings call 
        and come up with a list of between {top_n} to {top_n + 2} of the 
        key themes, initiatives, or strategic focuses emphasized within. 
        Prefer to keep closer to {top_n} rather than {top_n + 2}, the extra one or
        two should only be used if there are actually {top_n + 1} to {top_n + 2} 
        very important topics. 
        The target is to find pertinent topics for the quarter, rather than
        procedural or generic bookeeping phrases. 
        The response should have the focuses separated 
        by a comma and a space, ready to be printed out to a viewer in bullet points. Remember to capitalize
        the first letters as if they are sentences, but do not add any punctuation. Remember to also capitalize
        names of products if they are capitalized, for example "F-35" the fighter jet rather than "f-35".

        Text is here:

        {text}
    """
    try:
        resp = _GEMINI.generate_content(
            prompt,
            generation_config={
                "temperature": 0,
                "response_mime_type": "application/json"
            }
        )
        return json.loads(resp.text) 
    except Exception as e:
        print(f"[Gemini fallback] Keyword extraction failed: {e}")
        return []