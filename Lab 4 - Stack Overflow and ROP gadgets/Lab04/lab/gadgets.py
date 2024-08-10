import sys
from capstone import *
import binascii
from elftools.elf.constants import SH_FLAGS
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection
import argparse

##############################################################
# takes a string of arbitrary length and formats it 0x for Capstone
def convertXCS(s):
    if len(s) < 2: 
        print "Input too short!"
        return 0
    
    if len(s) % 2 != 0:
        print "Input must be multiple of 2!"
        return 0

    conX = ''
    
    for i in range(0, len(s), 2):
        b = s[i:i+2]
        b = chr(int(b, 16))
        conX = conX + b
    return conX


##############################################################

def getHexStreamsFromElfExecutableSections(filename):
    print "Processing file:", filename
    execSections = []
    with open(filename, 'rb') as f:
        elf = ELFFile(f)
        for section in elf.iter_sections():
            # Only process the .text section
            if section.name not in ['.text']:
                continue
            name = section.name
            addr = section['sh_addr']
            byteStream = section.data()
            hexStream = binascii.hexlify(byteStream)
            newExecSection = {}
            newExecSection['name'] = name
            newExecSection['addr'] = addr
            newExecSection['hexStream'] = hexStream
            execSections.append(newExecSection)
    return execSections

# For 4.6: We want the list of gadgets of arbitrary length
def getGadgets(hexStream, length):
    gadgets = []
    i = 0
    while i < len(hexStream):
        gadget = hexStream[i : i + length]
        # Checks if gadget ends with "ret" instruction
        if gadget.endswith(b'c3'):  
            gadgets.append(gadget)
        # Moves to the next instruction
        i += 2  
    return gadgets

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--length', type=int, default=100)
    parser.add_argument('filename', nargs='+')
    args = parser.parse_args()

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    for filename in args.filename:
        execSections = getHexStreamsFromElfExecutableSections(filename)
        print("Found", len(execSections), "executable sections:")
        for s in execSections:
            print("Name:", s['name'])
            print("0x")
            print("Address:", hex(s['addr']))
            print("Hex Stream:", s['hexStream'])
            gadgets = getGadgets(s['hexStream'], args.length)
            print("Gadgets:")
            for gadget in gadgets:
                offset = 0
                hexdata = s['hexStream']
                gadget = hexdata[0 : 100]           
                gadget = convertXCS(gadget)
                for (address, size, mnemonic, op_str) in md.disasm_lite(gadget, offset):
                    #Exclude branching instructions
                    if 'jmp' not in mnemonic and 'je' not in mnemonic and 'jne' not in mnemonic and 'jg' not in mnemonic and 'jle' not in mnemonic:
                        print("Gadget: %s %s" % (mnemonic, op_str))
            print()

            # For 4.7: We want the number of gadgets of lengths 1, 2, 3 in the .text section of the /bin/ls binary
            one_instr_gadgets = []
            two_instr_gadgets = []
            three_instr_gadgets = []

            if s['name'] == '.text':
                gadgets = getGadgets(s['hexStream'], args.length)
                for gadget in gadgets:
                    # Excludes the "ret" instruction
                    instr_count = sum(1 for _ in md.disasm_lite(gadget, 0)) - 1 
                    if instr_count == 1:
                        one_instr_gadgets.append(gadget)
                    elif instr_count == 2:
                        two_instr_gadgets.append(gadget)
                    elif instr_count == 3:
                        three_instr_gadgets.append(gadget)

            print("Number of gadgets of length 1:", len(one_instr_gadgets))
            print("Number of gadgets of length 2:", len(two_instr_gadgets))
            print("Number of gadgets of length 3:", len(three_instr_gadgets))
