FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy source code and frontend assets
COPY backend/app/ ./backend/app/
COPY frontend/ ./frontend/

# Expose port and configure environment
EXPOSE 8080
ENV PYTHONPATH=/app

# Start FastAPI server
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8080"]
