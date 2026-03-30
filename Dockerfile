FROM python:3.11-slim

WORKDIR /app

# Copy and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/app ./app

# Copy frontend so FastAPI can serve it
COPY frontend ../frontend

# Render sets PORT dynamically; default to 8000 for local use
ENV PORT=8000

# Run the FastAPI server
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
