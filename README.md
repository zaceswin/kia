# 🔐 kia - SOC Honeypot & Failed Pentest Simulation

📌 **Overview**
This repository demonstrates a safe simulation of a failed penetration test and an active defensive honeypot from a Security Operations Center (SOC) perspective. 

Instead of performing real attacks, this architecture shows how a system:
- Handles and tarpits unauthorized login attempts to exhaust attacker resources.
- Logs suspicious activity using structured JSON (SIEM-ready).
- Enriches IP logs with real-world threat intelligence via AbuseIPDB.
- Generates automated firewall (`iptables`) remediation scripts.

This project is designed for educational purposes only, focusing on blue team defensive engineering.

🎯 **Objectives**
- Simulate brute-force login attempts against mock SSH/HTTP endpoints.
- Demonstrate exponential backoff (tarpitting) in C to slow down attackers.
- Visualize attacks via a FastAPI & Tailwind CSS secure dashboard.
- Generate automated active-defense responses using Python.

🛠️ **Technologies Used**
- **Python (FastAPI)** – Dashboard backend and automated iptables script generation.
- **C** – Low-level tarpit implementation for connection delaying.
- **Docker & Docker Compose** – Containerized microservices architecture.
- **Tailwind CSS & Jinja2** – Frontend SOC dashboard rendering.
- **AbuseIPDB API** – Threat intelligence enrichment.
- **GitHub Actions** – CI/CD pipeline for code security and compilation.

📂 **Project Structure**
```text
kia/
│── src/
│   ├── failed_pentest_simulation.c   # C-level Tarpit simulator
│   ├── failed_pentest_simulation.py  # Python brute-force simulator
│   ├── generate_firewall_rules.py    # iptables automation script
│   └── dashboard.py                  # FastAPI Dashboard
│── templates/
│   └── index.html                    # Tailwind CSS UI
│── logs/                             # Docker-mounted log directory
│── docker-compose.yml
│── Dockerfile
└── README.md
