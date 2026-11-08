import pytest
import json
from fastapi.testclient import TestClient
from src.dashboard import app, API_KEY

# Initialize the FastAPI test client
client = TestClient(app)

def test_dashboard_unauthorized_no_token():
    """Test that accessing the dashboard without a token returns a 401."""
    response = client.get("/dashboard")
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or missing Admin Token"}

def test_dashboard_unauthorized_wrong_token():
    """Test that accessing the dashboard with an incorrect token returns a 401."""
    headers = {"X-Admin-Token": "hacker_guessing_tokens"}
    response = client.get("/dashboard", headers=headers)
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or missing Admin Token"}

def test_dashboard_authorized_empty_logs(monkeypatch, tmp_path):
    """Test that the dashboard loads successfully when logs are empty."""
    # Use monkeypatch and tmp_path to point LOG_FILE to a safe, temporary location
    mock_log_file = tmp_path / "server_logs.json"
    mock_log_file.touch()
    monkeypatch.setattr("src.dashboard.LOG_FILE", mock_log_file)

    headers = {"X-Admin-Token": API_KEY}
    response = client.get("/dashboard", headers=headers)
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Failed Access Attempt Monitor" in response.text
    # Verify the zero-metrics are rendered
    assert "0</p>" in response.text 

def test_dashboard_authorized_with_logs(monkeypatch, tmp_path):
    """Test that the dashboard parses and renders JSON logs correctly."""
    mock_log_file = tmp_path / "server_logs.json"
    
    # Write a mock JSON log entry
    mock_log_data = {
        "timestamp": "2026-11-08T18:00:00.000Z",
        "source_ip": "10.10.10.10",
        "username": "root",
        "password_attempt": "admin123",
        "protocol": "SSH",
        "status": "AUTH_FAILED",
        "action_taken": "CONNECTION_DROPPED"
    }
    
    with open(mock_log_file, "w") as f:
        f.write(json.dumps(mock_log_data) + "\n")
        
    monkeypatch.setattr("src.dashboard.LOG_FILE", mock_log_file)

    headers = {"X-Admin-Token": API_KEY}
    response = client.get("/dashboard", headers=headers)
    
    assert response.status_code == 200
    # Verify the mock data appears in the HTML output
    assert "10.10.10.10" in response.text
    assert "root" in response.text
