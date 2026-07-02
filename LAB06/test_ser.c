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

    // Create TCP socket
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        perror("socket failed");
        exit(1);
    }

    // Prepare server address
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    // Bind
    if (bind(server_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("bind failed");
        close(server_fd);
        exit(1);
    }

    // Listen
    if (listen(server_fd, 1) < 0) {
        perror("listen failed");
        close(server_fd);
        exit(1);
    }

    printf("Server listening on port %d...\n", PORT);

    // Accept one connection
    client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_len);
    if (client_fd < 0) {
        perror("accept failed");
        close(server_fd);
        exit(1);
    }

    printf("New connection established.\n");

    // Send welcome message
    char *welcome_msg = "Hawkins Lab: Secure channel established.";
    send(client_fd, welcome_msg, strlen(welcome_msg), 0);
    printf("Sent: %s\n", welcome_msg);

    // Receive message from client
    memset(buffer, 0, sizeof(buffer));
    int bytes_received;
    char msg[1024];

    for (int i = 0; strcmp(buffer, "bye") != 0; i++){
        memset(buffer, 0, sizeof(buffer));
        bytes_received = recv(client_fd, buffer, sizeof(buffer) - 1, 0);
        if (bytes_received > 0) {
            printf("Received from client: %s\n", buffer);
            printf("Enter your message: ");
            fgets(msg, sizeof(msg), stdin);
            send(client_fd, msg, strlen(msg), 0);
            
        }
        memset(buffer, 0, sizeof(buffer));
    }

    // Close connection
    close(client_fd);
    close(server_fd);

    return 0;
}