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

_END_PUNCT = re.compile(r"(?<=[.!?])\s+")
load_dotenv()



import google.generativeai as genai

"""
genai.configure(api_key=os.getenv("GEMINI_API_KEY"),
                transport="grpc")  # gRPC is faster & avoids some HTTP quirks

for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)
"""



MAX_CHARS = 70000 
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")

kw_model = KeyBERT(SentenceTransformer("all-MiniLM-L6-v2"))

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


def _chunks(text, size=MAX_CHARS):
    for i in range(0, len(text), size):
        yield text[i : i + size]

def run_sentiment(text: str) -> float:
    scores = []
    for chunk in _chunks(text):
        prompt = (
            "Rate the overall sentiment of the following passage on a scale "
            "-1 (negative) to 1 (positive). Respond with JUST the number.\n\n"
            + chunk
        )
        resp = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0,
                max_output_tokens=16,
            ),
        )
        scores.append(float(resp.text.strip()))
    return sum(scores) / len(scores)

def extract_keywords(text: str, top_n: int = 10):

    kws = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 3),
        stop_words=None,
        top_n=top_n
    )
    return [{"phrase": k, "score": round(s,3)} for k,s in kws]