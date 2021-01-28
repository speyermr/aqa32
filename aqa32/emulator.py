from aqa32.constants import *
from aqa32.instructions import *

MEMORY_SIZE = 256

def build(code):
    memory = [0] * MEMORY_SIZE
    for i, b in enumerate(code):
        memory[i] = b
    registers = [0] * 13
    return Emulator(registers, memory, 0, 0, '', False)

class Emulator():
    def __init__(self, registers, memory, pc, cmp, screen, halted):
        self.registers = registers
        self.memory = memory
        self.pc = pc
        self.cmp = cmp
        self.screen = screen
        self.halted = halted

    def copy(self):
        return Emulator(
                self.registers[:],
                self.memory[:],
                self.pc,
                self.cmp,
                self.screen,
                self.halted)

    def step(self):
        r = self.registers
        word = self.memory[self.pc]
        self.pc += 1

        opcode = (word >> 27) & 0b11111
        rn = (word >> 23) & 0b1111
        rd = (word >> 19) & 0b1111
        address_mode = (word >> 16) & 0b111
        op2 = word & 0xff

        instruction = INSTRUCTIONS[opcode]
        if address_mode == ADDRESS_MODE_DIRECT:
            op2 = r[op2]

        if instruction == HALT:
            self.halted = True
        elif instruction == LDR:
            r[rd] = self.memory[op2]
        elif instruction == STR: 
            self.memory[op2] = r[rd]
        elif instruction == ADD:
            r[rd] = r[rn] + op2
        elif instruction == SUB:
            r[rd] = r[rn] - op2
        elif instruction == MOV:
            r[rd] = op2
        elif instruction == CMP:
            self.cmp = r[rn] - op2
        elif instruction == B:
            pc = op2
        elif instruction == BEQ:
            if self.cmp == 0:
                pc = op2
        elif instruction == BNE:
            if self.cmp != 0:
                pc = op2
        elif instruction == BGT:
            if self.cmp > 0:
                pc = op2
        elif instruction == BLT:
            if self.cmp < 0:
                pc = op2
        elif instruction == AND:
            r[rd] = r[rn] & op2
        elif instruction == ORR:
            r[rd] = r[rn] & op2
        elif instruction == EOR:
            r[rd] = r[rn] ^ op2
        elif instruction == MVN:
            r[rd] = ~ op2
        elif instruction == LSL:
            r[rd] = r[rn] << op2
        elif instruction == LSR:
            r[rd] = r[rn] >> op2
        elif instruction == INP:
            input()
        elif instruction == OUT:
            if op2 == DEV_UINT:
                self.screen += str(r[rn])
            elif op2 == DEV_CHAR:
                self.screen += chr(r[rn])
            else:
                raise Exception(f'output to dev {op2} not implemented')
            pass
        else:
            raise Exception(f'unknown instruction {opcode}')
