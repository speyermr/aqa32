from aqa32.assembler import assemble
from aqa32.render import render
from time import sleep 
import aqa32.emulator

import sys
path = sys.argv[1]

with open(path) as f:
    assembler = f.read()

code, sourcemap = assemble(assembler)
e = emulator.build(code)

RESET = "\033[0;0H"

while not e.halted:
    history.append(e.copy())

while True:
    e.step()
    print(RESET + render(e, example, sourcemap))
    sleep(0.1)
