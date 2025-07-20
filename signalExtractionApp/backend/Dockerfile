# Base image with Python 3.12
FROM python:3.12-slim

# Create working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download FinBERT weights at build time
RUN python -c "from transformers import AutoModelForSequenceClassification, AutoTokenizer; AutoModelForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone'); AutoTokenizer.from_pretrained('yiyanghkust/finbert-tone')"

# Copy backend code
COPY . .

# Expose port for FastAPI
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
