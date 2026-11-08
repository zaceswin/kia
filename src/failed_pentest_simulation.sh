#!/bin/bash
# failed_pentest_simulation.sh

echo "=== Simulating Failed Pentest in Bash ==="

VALID_USER="admin"
VALID_PASS="SecurePass123"
LOGFILE="server_logs.txt"

# Array of test attempts
declare -a attempts=("admin:admin" "root:toor" "admin:123456" "administrator:password")

for attempt in "${attempts[@]}"; do
    IFS=":" read username password <<< "$attempt"
    echo "Trying username: $username password: $password"

    if [[ "$username" == "$VALID_USER" && "$password" == "$VALID_PASS" ]]; then
        echo "Access Granted ✅"
        echo "$(date): SUCCESSFUL LOGIN" >> "$LOGFILE"
        break
    else
        echo "Access Denied ❌"
        echo "$(date): FAILED LOGIN - $username" >> "$LOGFILE"
    fi
done

echo "Pentest simulation complete. Check $LOGFILE"
