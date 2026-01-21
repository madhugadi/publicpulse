FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (optional but safe)
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend ./backend

# Expose port (Render uses 10000)
EXPOSE 10000

# Start FastAPI app
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "10000"]
