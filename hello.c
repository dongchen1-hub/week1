#include <stdio.h>
#include <string.h>

int main(void) {
    char word[256];

    printf("Enter a word: ");
    fflush(stdout);
    if (fgets(word, sizeof word, stdin) == NULL) {
        return 1;
    }

    size_t length = strcspn(word, "\r\n");
    if (length == sizeof word - 1) {
        int next = getchar();
        if (next != '\n' && next != EOF) {
            fputs("Please enter at most 255 characters.\n", stderr);
            return 1;
        }
    }

    while (length > 0) {
        length--;
        putchar(word[length]);
    }
    putchar('\n');
    return 0;
}
