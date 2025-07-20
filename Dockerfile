WORKDIR /app

# Copy requirements and install
COPY signalExtractionApp/backend/requirements.txt .
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

# (model download line stays the same...)

# Copy rest of your backend code
COPY signalExtractionApp/backend/ . 

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
