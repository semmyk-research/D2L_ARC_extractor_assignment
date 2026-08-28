# Use a minimal Dockerfile to run the NiceGUI app

FROM python:3.11-slim

# Set environment
ENV PYTHONUNBUFFERED=1
ENV PORT=7860
WORKDIR /app

# Install system deps required for some Python packages (kept minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn uvicorn

# Copy application
COPY . /app

EXPOSE 7860

# Run with Gunicorn + Uvicorn worker
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:7860", "--workers", "1"]
