FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt ./requirements.txt

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend ./backend

# Tell Python where "app" lives
ENV PYTHONPATH=/app/backend

EXPOSE 10000

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
