#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PORT 5050

int main() {
    int server_fd, client_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    char buffer[1024];
    char response[1024];

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) { perror("socket failed"); exit(1); }

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("bind failed"); close(server_fd); exit(1);
    }

    if (listen(server_fd, 1) < 0) {
        perror("listen failed"); close(server_fd); exit(1);
    }

    printf("Server listening on port %d...\n", PORT);

    client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_len);
    if (client_fd < 0) { perror("accept failed"); close(server_fd); exit(1); }

    printf("New connection established.\n");

    // Send welcome message
    char *welcome = "Hawkins Lab: Secure channel established.";
    send(client_fd, welcome, strlen(welcome), 0);

    // Chat loop
    while (1) {
        memset(buffer, 0, sizeof(buffer));
        int bytes = recv(client_fd, buffer, sizeof(buffer) - 1, 0);
        if (bytes <= 0) break;

        printf("Received: %s\n", buffer);

        // Break if client says bye
        if (strcmp(buffer, "bye") == 0) {
            printf("Client disconnected.\n");
            break;
        }

        // Send response with "Server: " prefix
        printf("Enter response: ");
        fgets(response, sizeof(response), stdin);
        response[strcspn(response, "\n")] = '\0';

        char full_response[1100];
        snprintf(full_response, sizeof(full_response), "Server: %s", response);

        send(client_fd, full_response, strlen(full_response), 0);
        printf("Sent: %s\n", full_response);
    }

    close(client_fd);
    close(server_fd);

    return 0;
}