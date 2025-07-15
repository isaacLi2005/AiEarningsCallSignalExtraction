#!/usr/bin/env python3
"""
debug_split.py
~~~~~~~~~~~~~~
Standalone tester for API Ninjas earnings‑call transcript split.

Usage
-----
    export API_NINJAS_KEY="your‑key"
    python debug_split.py NVDA 2025 3
"""

from __future__ import annotations
import os, sys, argparse, textwrap, shutil, re, requests

API_URL = "https://api.api-ninjas.com/v1/earningstranscript"
API_KEY = os.getenv("API_NINJAS_KEY") or ""
SEPARATOR = "=" * shutil.get_terminal_size().columns


# ----------------------------------------------------------------------
# Fetch full API payload
# ----------------------------------------------------------------------
def fetch_transcript(ticker: str, year: int, quarter: int) -> dict:
    params = {"ticker": ticker, "year": year, "quarter": quarter}
    r = requests.get(API_URL, params=params, headers={"X-Api-Key": API_KEY})
    if r.status_code != 200:
        raise RuntimeError(f"{r.status_code} {r.reason}\n{r.text[:400]}")
    data = r.json()
    if isinstance(data, list):                       # sometimes the free tier returns a list
        data = next((d for d in data
                     if d.get("year") == year and d.get("quarter") == quarter),
                    None) or {}
    return data


# ----------------------------------------------------------------------
# Split logic – ONLY first "role":"Analyst"
# ----------------------------------------------------------------------
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


# ----------------------------------------------------------------------
# Helpers / CLI
# ----------------------------------------------------------------------
def preview(txt: str, n=160) -> str:
    return textwrap.shorten(txt.replace("\n", " "), width=n, placeholder=" …")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("year",    type=int)
    ap.add_argument("quarter", type=int)
    args = ap.parse_args()

    ticker  = args.ticker.strip().replace("\u00a0", "").upper()
    year    = args.year
    quarter = args.quarter

    print(f"Fetching {ticker} {year} Q{quarter} …")
    resp = fetch_transcript(ticker, year, quarter)
    full_txt = resp.get("transcript", "")
    print(f"Transcript length: {len(full_txt):,} chars")

    prepared, qa = split_management_qa(resp)

    print(SEPARATOR)
    print("split_management_qa() result:")
    print(f"prepared len: {len(prepared):,}   |   qa len: {len(qa):,}")
    print("-" * len(SEPARATOR))
    print("prepared head:\n", preview(prepared))
    print("\nqa head:\n", preview(qa) or "[NONE]")
    print(SEPARATOR)


if __name__ == "__main__":
    if not API_KEY:
        sys.exit("💥  Please export API_NINJAS_KEY first.")
    main()
