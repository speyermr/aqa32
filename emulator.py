from instructions import *

MEMORY_SIZE = 256

class Emulator():
    def __init__(self):
        self.registers = [0] * 13
        self.pc = 0
        self.memory = [0] * MEMORY_SIZE
        self.cmp = 0
        self.screen = ''
        self.halted = False

    def load(self, code):
        for i, b in enumerate(code):
            self.memory[i] = b

    def step(self):
        r = self.registers
        word = self.memory[pc]
        pc += 1

        opcode = (word >> 27) & 0b11111
        rn = (word >> 23) & 0b1111
        rd = (word >> 19) & 0b1111
        address_mode = (word >> 16) & 0b111
        op2 = word & 0xff

        instruction = INSTRUCTIONS[opcode]
        if address_mode == AM_DIRECT:
            op2 = reg

        if instruction == HALT:
            self.halted = True
        elif instruction == NOOP:
            pass
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
