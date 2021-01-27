INSTRUCTIONS = [
        'LDR', 'STR', 'ADD', 'SUB', 'MOV', 'CMP', 'B', 'BEQ', 'BNE', 'BGT',
        'BLT', 'AND', 'ORR', 'EOR', 'MVN', 'LSL', 'LSR', 'HALT', 'INP', 'OUT',
        ]

SIZE = 256

class Emulator():
    PC = 13

    def __init__(self):
        self.registers = [0] * 14
        self.memory = [0] * SIZE
        self.cmp = 0
        self.screen = ''
        self.halted = False

    def load(self, code):
        for i, b in enumerate(code):
            self.memory[i] = b

    def step(self):
        r = self.registers
        word = self.memory[r[PC]]
        r[PC] += 1

        opcode = (word >> 27) & 0b11111
        rn = (word >> 23) & 0b1111
        rd = (word >> 19) & 0b1111
        address_mode = (word >> 16) & 0b111
        op2 = word & 0xff

        opcode = INSTRUCTIONS[opcode]
        if address_mode == AM_DIRECT:
            op2 = reg

        if opcode == HALT:
            self.halted = True
        elif opcode == NOOP:
            pass
        elif opcode == LDR:
            r[rd] = self.memory[op2]
        elif opcode == STR: 
            self.memory[op2] = r[rd]
        elif opcode == ADD:
            r[rd] = r[rn] + op2
        elif opcode == SUB:
            r[rd] = r[rn] - op2
        elif opcode == MOV:
            r[rd] = op2
        elif opcode == CMP:
            self.cmp = r[rn] - op2
        elif opcode == B:
            r[PC] = op2
        elif opcode == BEQ:
            if self.cmp == 0:
                r[PC] = op2
        elif opcode == BNE:
            if self.cmp != 0:
                r[PC] = op2
        elif opcode == BGT:
            if self.cmp > 0:
                r[PC] = op2
        elif opcode == BLT:
            if self.cmp < 0:
                r[PC] = op2
        elif opcode == AND:
            r[rd] = r[rn] & op2
        elif opcode == ORR:
            r[rd] = r[rn] & op2
        elif opcode == EOR:
            r[rd] = r[rn] ^ op2
        elif opcode == MVN:
            r[rd] = ~ op2
        elif opcode == LSL:
            r[rd] = r[rn] << op2
        elif opcode == LSR:
            r[rd] = r[rn] >> op2
        elif opcode == INP:
            input()
        elif opcode == OUT:
            if op2 == DEV_UINT:
                self.screen += str(r[rn])
            elif op2 == DEV_CHAR:
                self.screen += chr(r[rn])
            else:
                raise Exception(f'output to dev {op2} not implemented')
            pass
        else:
            raise Exception(f'unknown instruction {opcode}')
