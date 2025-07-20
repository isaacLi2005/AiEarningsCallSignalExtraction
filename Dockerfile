# ── From your original: pick up Python 3.12 slim as the base
FROM python:3.12-slim

# ── Set working directory
WORKDIR /app

# ── Copy & install dependencies from the backend folder
COPY signalExtractionApp/backend/requirements.txt .
RUN pip install --no‑cache‑dir --extra‑index‑url https://download.pytorch.org/whl/cpu -r requirements.txt

# ── (Optional) Pre‑download FinBERT at build time if you want it cached in the image
RUN python - <<EOF
from transformers import AutoModelForSequenceClassification, AutoTokenizer
AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")
AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
EOF

# ── Copy your backend source
COPY signalExtractionApp/backend/ .

# ── Expose the port your app listens on
EXPOSE 8000

# ── Launch FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]