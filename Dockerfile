FROM python:3.11-slim

WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code and templates
COPY src/ ./src/
COPY templates/ ./templates/

# Ensure the logs directory exists
RUN mkdir -p /app/logs
