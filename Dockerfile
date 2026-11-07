FROM python:3.11-slim

WORKDIR /app

# Install dependencies for the FastAPI dashboard
RUN pip install --no-cache-dir fastapi uvicorn jinja2 httpx

# Copy the source code and templates
COPY src/ ./src/
COPY templates/ ./templates/

# Ensure the logs directory exists
RUN mkdir -p /app/logs
