// failed_pentest_simulation.c
#include <stdio.h>
#include <string.h>
#include <time.h>

#define MAX_ATTEMPTS 5

int main() {
    char username[50];
    char password[50];
    const char VALID_USERNAME[] = "admin";
    const char VALID_PASSWORD[] = "SecurePass123";

    printf("=== Simulating Failed Pentest in C ===\n");

    for (int i = 0; i < MAX_ATTEMPTS; i++) {
        printf("\nAttempt %d\n", i+1);
        printf("Enter username: ");
        scanf("%49s", username);
        printf("Enter password: ");
        scanf("%49s", password);

        if (strcmp(username, VALID_USERNAME) == 0 && strcmp(password, VALID_PASSWORD) == 0) {
            printf("Access Granted ✅\n");
            break;
        } else {
            printf("Access Denied ❌\n");

            // Log failed attempt
            time_t now = time(NULL);
            printf("Log: FAILED LOGIN at %s", ctime(&now));
        }
    }

    printf("\nPentest simulation complete.\n");
    return 0;
}
