#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PORT 5050

void log_shutdown(int count) {
    // Get current time
    time_t now = time(NULL);
    struct tm *t = localtime(&now);
    char timestamp[20];
    strftime(timestamp, sizeof(timestamp), "%H:%M:%S", t);

    // Append to shutdown_log.txt
    FILE *f = fopen("shutdown_log.txt", "a");
    if (f == NULL) { perror("fopen failed"); return; }
    fprintf(f, "[%s] shutdown\n", timestamp);

    // Rewrite the count at the end (overwrite last line)
    // We'll handle count separately — just append for now
    fclose(f);

    // Rewrite the entire file to update the count line
    // Read existing lines first
    f = fopen("shutdown_log.txt", "r");
    char lines[100][64];
    int num_lines = 0;
    while (fgets(lines[num_lines], sizeof(lines[num_lines]), f)) {
        // Strip old count line
        if (strncmp(lines[num_lines], "Shutdown count:", 15) != 0) {
            num_lines++;
        }
    }
    fclose(f);

    // Write back with updated count
    f = fopen("shutdown_log.txt", "w");
    for (int i = 0; i < num_lines; i++) {
        fputs(lines[i], f);
    }
    fprintf(f, "Shutdown count: %d\n", count);
    fclose(f);
}

int main() {
    int server_fd, client_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    char buffer[1024];
    int shutdown_count = 0;

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) { perror("socket failed"); exit(1); }

    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("bind failed"); close(server_fd); exit(1);
    }

    if (listen(server_fd, 5) < 0) {
        perror("listen failed"); close(server_fd); exit(1);
    }

    printf("Gate server listening on port %d...\n", PORT);

    while (1) {
        client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_len);
        if (client_fd < 0) { perror("accept failed"); continue; }

        printf("Client connected.\n");

        memset(buffer, 0, sizeof(buffer));
        int bytes = recv(client_fd, buffer, sizeof(buffer) - 1, 0);
        if (bytes <= 0) { close(client_fd); continue; }

        printf("Received: %s\n", buffer);

        if (strcmp(buffer, "shutdown") == 0) {
            shutdown_count++;
            log_shutdown(shutdown_count);

            char *reply = "Rift sealed. Goodbye, friends.";
            send(client_fd, reply, strlen(reply), 0);
            printf("Sent: %s\n", reply);
            printf("Shutdown count: %d\n", shutdown_count);
        } else {
            char *reply = "Unknown command.";
            send(client_fd, reply, strlen(reply), 0);
        }

        close(client_fd);
    }

    close(server_fd);
    return 0;
}