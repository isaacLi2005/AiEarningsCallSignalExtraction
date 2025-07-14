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



MAX_CHARS = 70000 

kw_model = KeyBERT(SentenceTransformer("all-MiniLM-L6-v2"))

def preprocess(transcript: str) -> str:
    start_time = time.time()


    # Remove bracketed speaker instructions like [Operator Instructions]
    transcript = re.sub(r"\[.*?\]", "", transcript)

    # Remove newline characters and excessive whitespace
    transcript = re.sub(r"\s+", " ", transcript)

    # Optionally strip any non-ASCII characters
    transcript = transcript.encode("ascii", "ignore").decode()

    print(f"Preprocess time: {time.time() - start_time}")

    return transcript.strip()

def split_sentences(text: str) -> List[str]:    
    return [s.strip() for s in _END_PUNCT.split(text) if s.strip()]


def _chunks(text, size=MAX_CHARS):
    for i in range(0, len(text), size):
        yield text[i : i + size]




def run_sentiment(text: str) -> float:
    start_time = time.time()

    scores = []

    for chunk in _chunks(text, size=2000): 
        chunk_start_time = time.time()

        result = _finbert(chunk[:512])[0]    

        s = sum(_LABEL2VAL[d["label"]] * d["score"] for d in result)

        print(s)
        print(chunk)
        print(time.time() - chunk_start_time)

        scores.append(s)

    print(f"run_sentiment() took {time.time() - start_time}")

    return sum(scores) / len(scores)

def extract_keywords(text: str, top_n: int = 10):
    start_time = time.time()


    kws = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 3),
        stop_words=None,
        top_n=top_n
    )
    
    print(f"extract_keywords took {time.time() - start_time}")

    return [{"phrase": k, "score": round(s,3)} for k,s in kws]