#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define MAX_ATTEMPTS 5

// Simulate an IP tracking dictionary
int get_failed_attempts(const char *ip) {
    // In a real scenario, this would query an SQLite DB or Hash Map.
    // For simulation, we return a mock incrementing value.
    static int attempts = 0;
    return ++attempts;
}

void simulate_login_attempt(const char *ip, const char *username) {
    printf("[*] Incoming SSH connection from %s for user %s...\n", ip, username);
    
    int attempts = get_failed_attempts(ip);
    
    if (attempts > MAX_ATTEMPTS) {
        printf("[!] IP %s exceeded threshold. Dropping connection.\n", ip);
        return;
    }

    // Tarpitting: Delay response based on number of failed attempts
    int delay_seconds = attempts * 2; 
    
    printf("[-] Authentication failed. Tarpitting response for %d seconds...\n", delay_seconds);
    sleep(delay_seconds); // Suspends execution, exhausting attacker threads
    
    printf("[+] Connection closed for %s.\n\n", ip);
}

int main() {
    printf("Starting C-Level Tarpit Simulation...\n\n");
    
    // Simulating rapid brute force from the same IP
    for (int i = 0; i < 6; i++) {
        simulate_login_attempt("192.168.1.105", "admin");
    }
    
    return 0;
}
