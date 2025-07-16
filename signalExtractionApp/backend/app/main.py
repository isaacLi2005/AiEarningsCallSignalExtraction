from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timezone



load_dotenv()
API_NINJAS_API_KEY = os.getenv("API_NINJAS_KEY")

from app import nlp_utils


import time
from cachetools import LRUCache
from threading import Lock
import typing
from typing import List, Tuple


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/ping")
def ping():
    return {"message": f"pong, API key is {API_NINJAS_API_KEY}"}

def transcript(
    ticker: str = Query("NVDA"),
    year: int = Query(...),
    quarter: int = Query(...)
):
    headers = {"X-Api-Key": API_NINJAS_API_KEY}
    url = f"https://api.api-ninjas.com/v1/earningstranscript?ticker={ticker}&year={year}&quarter={quarter}"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": "Failed to fetch transcript", "status_code": response.status_code, "details": response.text}
    
    return response.json()



_CACHE: LRUCache[str, dict] = LRUCache(maxsize=32)
_CACHE_LOCK = Lock()
def _cache_key(ticker: str, year: int, quarter: int) -> str:
    return f"{ticker.upper()}:{year}:Q{quarter}"

def analyze_sentiment(ticker: str, year: int, quarter: int):
    key = _cache_key(ticker, year, quarter)

    with _CACHE_LOCK:
        if key in _CACHE:
            return _CACHE[key]

    url = f"https://api.api-ninjas.com/v1/earningstranscript?ticker={ticker}&year={year}&quarter={quarter}"
    r = requests.get(url, headers={"X-Api-Key": API_NINJAS_API_KEY})
    if r.status_code != 200:
        raise HTTPException(r.status_code, r.text)

    data = r.json()                       # **keep entire dict**
    if isinstance(data, list):            # free tier sometimes returns list
        data = next(
            (item for item in data
             if item.get("year") == year and item.get("quarter") == quarter),
            None
        ) or {}
    raw_transcript = data.get("transcript", "")
    if not raw_transcript:
        raise HTTPException(404, "Transcript missing")

    mgmt_raw, qa_raw = nlp_utils.split_management_qa(data)

    mgmt_text = nlp_utils.preprocess(mgmt_raw)
    qa_text   = nlp_utils.preprocess(qa_raw)

    mgmt_sent = nlp_utils.run_sentiment(mgmt_text)
    qa_sent   = nlp_utils.run_sentiment(qa_text)
    mgmt_kw   = nlp_utils.extract_keywords(mgmt_text)
    qa_kw     = nlp_utils.extract_keywords(qa_text)

    result = {
        "ticker": ticker,
        "year": year,
        "quarter": quarter,
        "management_sentiment": mgmt_sent,
        "qa_sentiment": qa_sent,
        "management_keywords": mgmt_kw,
        "qa_keywords": qa_kw,
    }

    with _CACHE_LOCK:
        _CACHE[key] = result
    return result


def try_transcript_exists(ticker: str, year: int, quarter: int) -> bool:
    url = (
        f"https://api.api-ninjas.com/v1/earningstranscript?"
        f"ticker={ticker}&year={year}&quarter={quarter}"
    )
    r = requests.get(url, headers={"X-Api-Key": API_NINJAS_API_KEY})
    if r.status_code != 200:
        return False

    data = r.json()
    if isinstance(data, list):
        # Only true if THIS year/quarter is in the list
        return any(
            item.get("year") == year and item.get("quarter") == quarter
            for item in data
        )
    elif isinstance(data, dict):
        # Dict shape means exact match
        return bool(data.get("transcript"))
    return False

def guess_latest_quarters(ticker="NVDA", n=4) -> list[tuple[int, int]]:
    today = datetime.now(timezone.utc)
    q = (today.month - 1) // 3 + 1
    y = today.year
    quarters = []

    for _ in range(n * 2):  # Try more in case some are missing
        try_q = (y, q)
        if try_transcript_exists(ticker, y, q):
            quarters.append(try_q)
            if len(quarters) == n:
                break
        q -= 1
        if q == 0:
            q = 4
            y -= 1
    if len(quarters) == n:
        return quarters
    else:
        raise HTTPException(status_code=400, detail="Could not find 4 most recent quarters.")
    
@app.get("/analyze_last_four_quarters_sentiment")
def analyze_last_n_quarters_sentiment(
    ticker: str = Query("NVDA"),
    year: int | None = Query(None),
    quarter: int | None = Query(None),
    n: int = Query(4)
):
    """
    Interprets the given year and quarter as the last quarter to use. 
    Fetches the previous four quarters of data. 
    year and quarter are both None by default, and signify that we should
    get the latest data available. 
    """

    if (year is None) != (quarter is None):
        raise HTTPException(400, "year and quarter must be provided together (or neither).")

    if (year is None):
        assert(quarter is None)
        latest_quarters_list = guess_latest_quarters(ticker=ticker, n=n)
    else:
        y, q = year, quarter
        latest_quarters_list = []
        for _ in range(n):
            latest_quarters_list.append((y, q))
            q -= 1
            if q == 0:
                q = 4
                y -= 1
        latest_quarters_list.reverse()
    
    nlp_results = []
    for i in range(n):
        (y, q) = latest_quarters_list[i]
        nlp_results.append(analyze_sentiment(ticker, y, q))

    result = {
        "ticker": ticker,
        "results": {
            f"{y}-Q{q}": nlp_results[i]
            for i, (y, q) in enumerate(latest_quarters_list)
        }
    }
    return result

