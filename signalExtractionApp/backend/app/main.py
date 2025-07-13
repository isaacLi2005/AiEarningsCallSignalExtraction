from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import requests

app = FastAPI()

load_dotenv()
API_NINJAS_API_KEY = os.getenv("API_NINJAS_KEY")


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