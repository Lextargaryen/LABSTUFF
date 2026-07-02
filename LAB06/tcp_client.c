#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PORT 5050
#define SERVER_IP "127.0.0.1"

int main() {
    int sock_fd;
    struct sockaddr_in server_addr;
    char buffer[1024];

    // Create socket
    sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd < 0) {
        perror("socket failed");
        exit(1);
    }

    // Prepare server address
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr);

    // Connect to server
    if (connect(sock_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("connect failed");
        close(sock_fd);
        exit(1);
    }

    // Read welcome message
    memset(buffer, 0, sizeof(buffer));
    int bytes_received = recv(sock_fd, buffer, sizeof(buffer) - 1, 0);
    if (bytes_received > 0) {
        printf("Server says: %s\n", buffer);
    }

    // Get message from the user
    char msg[1024];
    printf("Enter your message: ");
    fgets(msg, sizeof(msg), stdin);

    // Remove trailing newline from fgets
    msg[strcspn(msg, "\n")] = '\0';

    // Send message
    send(sock_fd, msg, strlen(msg), 0);
    printf("Sent: %s\n", msg);

    close(sock_fd);

    return 0;
}