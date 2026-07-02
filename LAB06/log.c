#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>

int main() {
    FILE* log = fopen("mind_flayer_log.txt", "w");

    char buffer[256] = ""; 

    for (int i = 0; strcmp(buffer, "exit") != 0; i++) {
        scanf("%s", buffer);
        if (strcmp(buffer, "exit") == 0) {
            break;
        }
        time_t rawtime;
        time(&rawtime);
        struct tm *timeinfo = localtime(&rawtime);
        fprintf(log, "[%02d:%02d:%02d] %s\n", 
                timeinfo->tm_hour, 
                timeinfo->tm_min, 
                timeinfo->tm_sec, 
                buffer);
    }
    fclose(log);
    return 0;
}