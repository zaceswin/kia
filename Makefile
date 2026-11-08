.PHONY: build up down logs compile-c clean firewall

# --- Docker Commands ---
build:
	docker-compose build

up:
	docker-compose up -d
	@echo "[+] Honeypot stack is running. Dashboard at http://localhost"

down:
	docker-compose down
	@echo "[-] Honeypot stack stopped."

logs:
	docker-compose logs -f

# --- C & Python Commands ---
compile-c:
	gcc src/failed_pentest_simulation.c -o pentest_sim
	@echo "[+] C simulation compiled to ./pentest_sim"

firewall:
	python3 src/generate_firewall_rules.py

# --- Maintenance ---
clean:
	rm -f pentest_sim
	rm -f logs/server_logs.json
	rm -f block_attackers.sh
	@echo "[+] Environment cleaned."
