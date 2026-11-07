from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import APIKeyHeader
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import json
import secrets
from pathlib import Path

app = FastAPI(title="SOC Honeypot Dashboard")
templates = Jinja2Templates(directory="templates")

# Security: Define API Key auth
API_KEY = "super_secure_admin_token_123"
api_key_header = APIKeyHeader(name="X-Admin-Token", auto_error=False)

# Security: Hardcode log path to prevent LFI (Local File Inclusion)
LOG_FILE = Path("server_logs.json")

def verify_api_key(api_key_header: str = Depends(api_key_header)):
    if not api_key_header or not secrets.compare_digest(api_key_header, API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing Admin Token",
        )
    return api_key_header

def read_logs():
    if not LOG_FILE.exists():
        return []
    logs = []
    with open(LOG_FILE, "r") as f:
        for line in f:
            if line.strip():
                logs.append(json.loads(line))
    return logs[::-1]  # Return newest first

@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request, api_key: str = Depends(verify_api_key)):
    logs = read_logs()
    
    # Calculate basic metrics
    total_attempts = len(logs)
    unique_ips = len(set(log.get("source_ip") for log in logs))
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "logs": logs,
        "total_attempts": total_attempts,
        "unique_ips": unique_ips
    })
