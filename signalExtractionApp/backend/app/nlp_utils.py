"""
This file contains functions that deal with natural language processing of a 
NVDA earnings call transcript. 
"""

import re
from typing import List

import os, textwrap, openai
from dotenv import load_dotenv
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

_END_PUNCT = re.compile(r"(?<=[.!?])\s+")
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY") 

def preprocess(transcript: str) -> str:
    # Remove bracketed speaker instructions like [Operator Instructions]
    transcript = re.sub(r"\[.*?\]", "", transcript)

    # Remove newline characters and excessive whitespace
    transcript = re.sub(r"\s+", " ", transcript)

    # Optionally strip any non-ASCII characters
    transcript = transcript.encode("ascii", "ignore").decode()

    return transcript.strip()

def split_sentences(text: str) -> List[str]:
    return [s.strip() for s in _END_PUNCT.split(text) if s.strip()]

def run_sentiment(text: str) -> float:
    CHUNK = 350
    chunks = [" ".join(split_sentences(text)[i:i+CHUNK])
              for i in range(0, len(split_sentences(text)), CHUNK)]

    scores = []
    for chunk in chunks:
        prompt = f"Rate the overall sentiment of this passage on a scale -1 (negative) to 1 (positive) and respond with just the number:\n\n{chunk}"
        rsp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}],
            temperature=0
        )
        scores.append(float(rsp.choices[0].message.content.strip()))

    return sum(scores) / len(scores)

def extract_keywords(text: str, top_n: int = 10):
    kw_model = KeyBERT(SentenceTransformer("all-MiniLM-L6-v2"))

    kws = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 3),
        stop_words=None,
        top_n=top_n
    )
    return [{"phrase": k, "score": round(s,3)} for k,s in kws]