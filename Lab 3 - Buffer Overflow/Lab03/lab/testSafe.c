#include <stdio.h>
#include <string.h>

//Size of buffer can be changed from here
#define SIZE 100 

void function1(char * arg) {
    char buffer[SIZE];

    // Safe string copy assures that at most (SIZE - 1) characters are copied from arg to buffer
    strncpy(buffer, arg, SIZE - 1);

    // The buffer should end with 0
    buffer[SIZE - 1] = '\0';

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

