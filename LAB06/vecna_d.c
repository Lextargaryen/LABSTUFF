#include <stdio.h>
#include <string.h>
#include <stdbool.h>

int main() {
    FILE* vecna_diary = fopen("vecna_diary.txt", "r");
    if (vecna_diary == NULL) { perror("fopen failed"); exit(1); }
    char buffer[256];
    int i = 1;
    int s_count = 0;
    bool c = true;

    while ((fgets(buffer, sizeof(buffer), vecna_diary)) != NULL) {
        printf("Line %d: %s", i, buffer);
        for (int j = 0; buffer[j] != '\0'; j++) {
            
            if (buffer[j] == ' ' || buffer[j] == '\n') {
                if (!(c)) {
                    s_count++;
                    c = true;
                }
            } else {
                c = false;
            }
        }
        i++;
    }
    printf("\nTotal lines: %d\n", i - 1);
    printf("Total words: %d\n", s_count);

    fclose(vecna_diary);

    return 0;
}