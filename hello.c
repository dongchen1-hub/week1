#include <stdio.h>
#include <string.h>

int main(void) {
    const char word[] = "infrastructure";

    puts("Hello!");
    for (size_t remaining = strlen(word); remaining > 0; --remaining) {
        putchar(word[remaining - 1]);
    }
    putchar('\n');
    return 0;
}
