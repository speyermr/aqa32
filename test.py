from assembler import assemble
import emulator
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

e = emulator.build(code)

RESET = "\033[0;0H"

history = []
while not e.halted:
    history.append(e.copy())
    e.step()

while True:
    for e in history:
        print(RESET + render(e, example, sourcemap))
        sleep(0.1)
