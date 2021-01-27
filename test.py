from assembler import assemble
from emulator import Emulator
from render import render
from time import sleep 

example = '''
start:  MOV R0, #5
        MOV R1, #6
        ADD R2, R0, R1
        STR R2, abc
        HALT
abc:    0x30
greeting:
        0x48656c6c
        0x6f2c2077
        0x6f726c64
        0x21000000
'''

code, sourcemap = assemble(example)

e = Emulator()
e.load(code)

RESET = "\033[0;0H"

while not e.halted:
    e.step()
    print(RESET + render(e, example, sourcemap))
    sleep(0.1)
