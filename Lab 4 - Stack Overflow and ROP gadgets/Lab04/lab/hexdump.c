#include <stdio.h>
#include <inttypes.h>
#include <string.h>
#include <stdlib.h>

#define MAX_BUFFER_SIZE 1000

int function2(char* filename) {
  FILE* f = NULL;
  char buffer[MAX_BUFFER_SIZE];
  char* mbuffer = NULL;
  uint64_t size = 0;
  uint64_t i = 0;


  f = fopen(filename, "rb");
  fseek(f, 0, SEEK_END);
  size = ftell(f);
  fseek(f, 0, SEEK_SET);

  // copy content of the file to the buffer on
  // the heap
  mbuffer = malloc(size);
  fread(mbuffer, size, 1, f);
  fclose(f);

  // copy content from the buffer on the heap
  // to the buffer on the stack
  memcpy(buffer, mbuffer, size);

  // dump hexa representation
  for (i = 0; i < MAX_BUFFER_SIZE; i++) {
    printf("%02X ", buffer[i]);
    if ((i+1) % 8 == 0) printf("    ");
    if ((i+1) % 16 == 0) printf("\n");
  }
  printf("\n");

  return 0;
}

int main(int argc, char** argv) {

  if (argc != 2) {
    printf("error: the first argument must \
        be the path to the file to hexdump.\n");
    return -1;
  }

  function2(argv[1]);

  // everything went according to plan
  return 0;
}
