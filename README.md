# Earnings Call Sentiment & Keywords Explorer

This web application analyzes recent earnings call transcripts from publicly traded companies. Enter a stock ticker (e.g., `NVDA`) to visualize sentiment trends and key discussion topics across the past few quarters.

---

## Features

- **Sentiment Analysis**: Detects positive, negative, and neutral tones in management commentary and Q&A.
- **Keyword Extraction**: Extracts main topics discussed each quarter.
- **LLM-Powered NLP**: Uses pretrained models and generative AI to analyze unstructured text.
- **Modern UI**: Built with React and FastAPI.

---

## 🛠️ How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/earnings-sentiment-app.git
cd earnings-sentiment-app
```

### 2. Backend Setup (Python + FastAPI)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Create a `.env` file in the `backend` folder with your API key:

```
API_NINJAS_KEY=your_actual_key_here
```

Start the backend server:

```bash
uvicorn main:app --reload
```

### 3. Frontend Setup (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Make sure your frontend `.env` or `vite.config.ts` points to the backend URL.

---

## AI/NLP Tools Used

- **Sentiment Model**: [`yiyanghkust/finbert-tone`](https://huggingface.co/yiyanghkust/finbert-tone)  
  > Based on: Araci, D. (2019). *FinBERT: Financial Sentiment Analysis with Pre-trained Language Models*. arXiv:1908.10063

- **Keyword Extraction**:  
  Google Gemini 1.5 Flash

- **Transcript Source**:  
  [API Ninjas](https://api-ninjas.com/api/earningstranscript)

---

## Assumptions & Limitations

- Transcripts are fetched via API Ninjas and may not be available for all tickers.
- Sentiment model is limited to short passages (max 512 tokens); transcripts are split into chunks.
- Gemini keyword results are accurate but not domain-tuned to finance.
- Q&A sections may be missing or empty in some transcripts.
- Currently analyzes the most recent *n* quarters (default: 4).

---

## Author

**Isaac Li**  
isaacbngli@gmail.com
