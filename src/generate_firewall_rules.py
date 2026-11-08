import json
from collections import Counter
from pathlib import Path

LOG_FILE = Path("logs/server_logs.json")
OUTPUT_SCRIPT = Path("block_attackers.sh")
THRESHOLD = 3  # Block IPs with more than 3 failed attempts


def generate_iptables_script():
    if not LOG_FILE.exists():
        print("[-] No logs found to analyze.")
        return

    ip_counts = Counter()

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                try:
                    data = json.loads(line)
                    ip_counts[data.get("source_ip")] += 1
                except json.JSONDecodeError:
                    continue

    # Filter IPs that exceed the threshold
    malicious_ips = [ip for ip, count in ip_counts.items() if count >= THRESHOLD]

    if not malicious_ips:
        print("[+] No IPs exceeded the blocking threshold.")
        return

    with open(OUTPUT_SCRIPT, "w", encoding="utf-8") as file:
        file.write("#!/bin/bash\n")
        file.write("# Auto-generated iptables blocking script\n\n")
        file.writelines(f"iptables -A INPUT -s {ip} -j DROP\n" for ip in malicious_ips)

    print(f"[+] Generated {OUTPUT_SCRIPT} with {len(malicious_ips)} IP blocks.")
    print(f"[*] Run 'sudo bash {OUTPUT_SCRIPT}' to apply rules.")


if __name__ == "__main__":
    generate_iptables_script()
