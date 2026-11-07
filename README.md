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


▶️ How to Run

1. Setup Environment
Create a .env file in the root directory and add your API key:

Bash
ABUSEIPDB_API_KEY=your_api_key_here
2. Deploy via Docker (Recommended)

Bash
docker-compose up --build -d
The FastAPI dashboard will be available at http://localhost:8000/dashboard.(Note: You must pass the header X-Admin-Token: super_secure_admin_token_123 to authenticate to the dashboard).

3. Run the C-Level Tarpit

Bash
gcc src/failed_pentest_simulation.c -o pentest_sim
./pentest_sim
4. Generate Firewall Rules

Bash
python3 src/generate_firewall_rules.py
sudo bash block_attackers.sh
📊 What the Simulation Shows

Repeated login attempts rejected and logged in NDJSON format.

C-script actively delaying responses (tarpitting) to waste attacker time.

Dashboard rendering threat scores showing the historical maliciousness of the attacking IPs.

Dynamic creation of iptables -A INPUT -s <IP> -j DROP commands.

⚠️ Disclaimer
This project does NOT perform real hacking or exploitation. It is strictly for learning, demonstrating security concepts, and showcasing defensive programming. Do not use these scripts against systems you do not own.

🚀 Future Improvements

Add Slack/Discord webhook alerts for critical threshold breaches.

Expand to a full Docker network with a reverse proxy (Nginx).

Integrate Fail2Ban parsing directly from the JSON logs.

👨‍💻 Authorzaceswin
Created as part of a cybersecurity learning journey.

⭐ Contribute
Feel free to fork this repository, improve the simulation, and submit a pull request!


<ElicitationsGroup message="To refine this setup before you push to GitHub:">
  <Elicitation label="Configure Nginx Reverse Proxy" query="Write an Nginx configuration to put in front of the FastAPI dashboard to handle SSL and header injection."/>
  <Elicitation label="Write Discord Webhook Alert" query="Draft a Python script that reads the JSON log and sends a Discord webhook alert when a high-threat IP is detected."/>
  <Elicitation label="Implement Fail2Ban config" query="Show me how to configure Fail2Ban to read the server_logs.json file and block IPs automatically instead of using the python script."/>
</ElicitationsGroup>

<FollowUp label="Want to secure the `.env` file from accidental commits?" query="Show me the standard .gitignore file for a Python/Docker project so I don't accidentally commit my AbuseIPDB API key."/>
