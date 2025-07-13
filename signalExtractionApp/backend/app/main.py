from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_NINJAS_API_KEY = os.getenv("API_NINJAS_KEY")

from app import nlp_utils


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

@app.get("/transcript")
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

@app.get("/analyze_sentiment")
def analyze_sentiment(
    ticker: str = Query("NVDA"),
    year: int = Query(...),
    quarter: int = Query(...)
):
    earnings_call_url = f"https://api.api-ninjas.com/v1/earningstranscript?ticker={ticker}&year={year}&quarter={quarter}"
    earnings_call_request = requests.get(earnings_call_url, headers={"X-Api-Key": API_NINJAS_API_KEY})
    if earnings_call_request.status_code != 200:
        raise HTTPException(earnings_call_request.status_code, earnings_call_request.text)
    
    raw_transcript = earnings_call_request.json().get("transcript", "")
    if raw_transcript == "":
        raise HTTPException(404, "Transcript missing")
    
    transcript_text = nlp_utils.preprocess(raw_transcript)

    sentiment_output = nlp_utils.run_sentiment(transcript_text)
    keywords = nlp_utils.extract_keywords(transcript_text)

    return {
        "ticker": ticker,
        "year": year,
        "quarter": quarter,
        "sentiment": sentiment_output,
        "keywords": keywords
    }
    