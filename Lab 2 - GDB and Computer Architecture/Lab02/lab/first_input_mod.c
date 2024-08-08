#include <stdio.h>
#include <string.h>

int new_function(){
    printf (":-)\n");
    return 0;
}

int main (int argc, char** argv){
    printf ("argv[1]: %s\n",argv[1]);
    new_function();
    return 0;
}
