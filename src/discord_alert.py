import json
import os
import time
from pathlib import Path

import httpx

# Configurable via environment variables
LOG_FILE = Path("logs/server_logs.json")
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def tail_logs_and_alert():
    if not WEBHOOK_URL:
        print("[-] DISCORD_WEBHOOK_URL not set in environment.")
        return

    if not LOG_FILE.exists():
        LOG_FILE.touch(exist_ok=True)

    print(f"[*] Monitoring {LOG_FILE} for new attacks...")

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        # Move pointer to the end of the file to only read new logs
        file.seek(0, 2)

        while True:
            line = file.readline()
            if not line:
                time.sleep(1)  # Wait for new entries
                continue

            try:
                log = json.loads(line)
                if log.get("status") == "AUTH_FAILED":
                    send_discord_alert(log)
            except json.JSONDecodeError:
                continue


def send_discord_alert(log_data):
    embed = {
        "embeds": [{
            "title": "🚨 Honeypot Alert: Failed Access",
            "color": 16711680,  # Hex code for Red
            "fields": [
                {"name": "Attacker IP", "value": log_data.get("source_ip", "Unknown"), "inline": True},
                {"name": "Target User", "value": log_data.get("username", "Unknown"), "inline": True},
                {"name": "Protocol", "value": log_data.get("protocol", "Unknown"), "inline": True},
            ],
            "footer": {"text": "SOC Honeypot Monitor"},
        }]
    }

    try:
        httpx.post(WEBHOOK_URL, json=embed, timeout=10.0)
        print(f"[+] Alert sent for IP: {log_data.get('source_ip')}")
    except httpx.RequestError as exc:
        print(f"[-] Failed to send Discord alert: {exc}")


if __name__ == "__main__":
    tail_logs_and_alert()
