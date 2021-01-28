from aqa32.assembler import assemble
import aqa32.emulator as emulator
from aqa32.render import render
from time import sleep

RESET = "\033[0;0H"

def emulate(assembly):
    code, sourcemap = assemble(assembly)
    em = emulator.build(code)
    while not em.halted:
        s = render(em, assembly, sourcemap)
        print(RESET + s)
        sleep(0.1)
        em.step()

    s = render(em, assembly, sourcemap)
    print(RESET + s)
