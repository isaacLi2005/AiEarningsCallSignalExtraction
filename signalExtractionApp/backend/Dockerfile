# Dockerfile
FROM python:3.12-slim

# Keep image small; set HF cache path (we'll mount a volume here at runtime)
ENV PIP_NO_CACHE_DIR=1 \
    HF_HOME=/app/.cache/huggingface \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1) Install Python deps first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

# 2) Copy the rest of your code
COPY . .

# Expose and run
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
