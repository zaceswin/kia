import json
import os
import secrets
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.security import APIKeyHeader
from fastapi.templating import Jinja2Templates

app = FastAPI(title="SOC Honeypot Dashboard")
templates = Jinja2Templates(directory="templates")

# Security: Define API Key auth
API_KEY = os.getenv("ADMIN_API_KEY")
if not API_KEY:
    raise RuntimeError("ADMIN_API_KEY environment variable must be set")

api_key_header = APIKeyHeader(name="X-Admin-Token", auto_error=False)

# Security: Hardcode log path to prevent LFI (Local File Inclusion)
LOG_FILE = Path("server_logs.json")


def verify_api_key(api_key_header_value: str = Depends(api_key_header)):
    if not api_key_header_value or not secrets.compare_digest(api_key_header_value, API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing Admin Token",
        )
    return api_key_header_value


def read_logs():
    if not LOG_FILE.exists():
        return []

    logs = []
    with open(LOG_FILE, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                logs.append(json.loads(line))

    return logs[::-1]  # Return newest first


@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request, _api_key: str = Depends(verify_api_key)):
    logs = read_logs()

    # Calculate basic metrics
    total_attempts = len(logs)
    unique_ips = len(set(log.get("source_ip") for log in logs))

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "logs": logs,
            "total_attempts": total_attempts,
            "unique_ips": unique_ips,
        },
    )
