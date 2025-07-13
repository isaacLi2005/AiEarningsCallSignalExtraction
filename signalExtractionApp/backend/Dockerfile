# Base image with Python 3.12
FROM python:3.12-slim

# Create working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Copy pre-downloaded model weights into Hugging Face cache
COPY hf_cache /root/.cache/huggingface

# Set environment variable to use that cache at runtime
ENV HF_HOME=/root/.cache/huggingface

# Expose port for FastAPI
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
