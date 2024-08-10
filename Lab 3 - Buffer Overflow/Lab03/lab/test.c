#include <stdio.h>
#include <string.h>

void function1(char * arg) {
    char buffer[100];
    strcpy(buffer, arg);
    printf("buffer is: '%s' \n", buffer);
}

int main(int argc, char** argv) {
    printf("Welcome to this vulnerable program!\n");
    if (argc <= 1) {
        printf("[error] one argument is required!\n");
        return -1;
    }
    printf("argv[0]: '%s' argv[1]: '%s'\n", argv[0], argv[1]);
    function1(argv[1]);
    return 0;
}