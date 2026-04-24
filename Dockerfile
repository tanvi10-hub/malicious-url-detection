# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY config.py .
COPY src/ src/
COPY templates/ templates/
COPY static/ static/

# Writable models dir (AUTO_DOWNLOAD_MODELS or mounted artifacts)
RUN mkdir -p models

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

ENV PORT=5000
EXPOSE 5000

# Render and other hosts set PORT at runtime
CMD ["/bin/sh", "-c", "exec gunicorn --worker-class=sync --workers=1 --timeout=120 --bind 0.0.0.0:${PORT} src.app:app"]
