#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PORT 8080

int main() {
    int server_fd, client_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    char buffer[4096];

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) { perror("socket failed"); exit(1); }

    // Allow port reuse to avoid "address already in use" errors
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

    printf("HTTP server running on port %d...\n", PORT);

    // Keep accepting connections in a loop
    while (1) {
        client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_len);
        if (client_fd < 0) { perror("accept failed"); continue; }

        // Read the HTTP request
        memset(buffer, 0, sizeof(buffer));
        recv(client_fd, buffer, sizeof(buffer) - 1, 0);
        printf("Request:\n%s\n", buffer);

        // Check if it's GET /alert HTTP/1.1
        if (strstr(buffer, "GET /alert HTTP/1.1") != NULL) {
            char *response =
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                "\r\n"
                "Emergency! Final rift detected. Prepare to shut down the gate.";
            send(client_fd, response, strlen(response), 0);
        } else {
            char *response =
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/plain\r\n"
                "\r\n"
                "404 Not Found";
            send(client_fd, response, strlen(response), 0);
        }

        close(client_fd);
    }

    close(server_fd);
    return 0;
}