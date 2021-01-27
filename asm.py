import time


# Opcodes
LDR  = 'LDR'
STR  = 'STR'
ADD  = 'ADD'
SUB  = 'SUB'
MOV  = 'MOV'
CMP  = 'CMP'
B    = 'B'
BEQ  = 'BEQ'
BNE  = 'BNE'
BGT  = 'BGT'
BLT  = 'BLT'
AND  = 'AND'
ORR  = 'ORR'
EOR  = 'EOR'
MVN  = 'MVN'
LSL  = 'LSL'
LSR  = 'LSR'
HALT = 'HALT'
INP  = 'INP'
OUT  = 'OUT'
NOOP = 'NOOP'

OPCODES = [
        LDR, STR, ADD, SUB, MOV, CMP, B, BEQ, BNE, BGT, BLT, AND, ORR, EOR,
        MVN, LSL, LSR, HALT, INP, OUT, NOOP,
        ]

# Output devices
DEV_UINT = 4
DEV_INT = 5
DEV_HEX = 6
DEV_CHAR = 7

# Registers
R0 = 'R0'
R1 = 'R1'
R2 = 'R2'
R3 = 'R3'
R4 = 'R4'
R5 = 'R5'
R6 = 'R6'
R7 = 'R7'
R8 = 'R8'
R9 = 'R9'
R10 = 'R10'
R11 = 'R11'
R12 = 'R12'
PC = 'PC'

REGISTERS = [R0, R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, PC]

# Address Modes
AM_IMMEDIATE = 1
AM_DIRECT = 0
# TODO Support ARM indirect, and indexed?

def parse(text):
    assembly = []

    label = None
    for line in text.splitlines():
        tokens = []
        for token in line.split(' '):
            if token == '':
                continue
            if token[0:2] == '//':
                break
            if token[-1] == ',':
                token = token[:-1]
            tokens.append(token)

        # Blank line (except for the comment)
        if tokens == []:
            continue

        # The first token is a label if it ends in ':'
        if tokens[0][-1] == ':':
            label = tokens[0][:-1]
            tokens = tokens[1:]

        # Move on (but keep a note of the label)
        if tokens == []:
            continue

        if tokens[-1][0] == '#':
            text = tokens[-1][1:]
            tokens[-1] = int(text, 0)

        assembly.append([label, *tokens])
        label = None

    return assembly

def assemble(code):
    result = []

    # Step 1: parse for labels, which always refer to the *next* address
    labels = {}
    for address, instruction in enumerate(code):
        label = instruction[0]
        if label in labels:
            raise Exception(f'label {label} is already defined')
        if label is not None:
            labels[label] = address

    for i, (label, opcode, *args) in enumerate(code):
        rd, rn, op2 = None, None, 0

        try:
            if opcode in {LDR, STR}:
                rd, op2 = args
            elif opcode in {ADD, SUB, AND, ORR, EOR, LSL, LSR}:
                rd, rn, op2 = args
            elif opcode in {MOV, MVN}:
                rd, op2 = args
            elif opcode in {CMP}:
                rn, op2 = args
            elif opcode in {B, BEQ, BNE, BGT, BLT}:
                op2 = args[0]
            elif opcode in {HALT, NOOP}:
                pass
            elif opcode in {INP, OUT}:
                rn, op2 = args
            else:
                raise Exception(f'unknown opcode {opcode}')
        except Exception as ex:
            raise Exception(f'{i}: {ex}')

        if op2 in REGISTERS:
            address_mode = AM_DIRECT
            op2 = REGISTERS.index(op2)
        elif op2 in labels:
            address_mode = AM_IMMEDIATE
            op2 = labels[op2]
        elif type(op2) == int:
            address_mode = AM_IMMEDIATE

        # 32    27   23   19   16
        # |     |    |    |    |
        # ..... .... .... .. . ........ ........
        # |___/ |__/ |__/ |/ | |_______________/
        # |     |    |    |  | |
        # |     Rn   Rd   |  | op2
        # opcode          |  <spare>
        #                 address_mode
        word = (OPCODES.index(opcode) << 27) | (address_mode << 16) | op2
        if rn is not None:
            word = word | (REGISTERS.index(rn) << 23)
        if rd is not None:
            word = word | (REGISTERS.index(rd) << 19)
        result.append(word)
    return result




class Machine():
    def __init__(self, memory_size=512):
        self.registers = dict((reg, 0) for reg in REGISTERS)
        self.memory = [0] * (memory_size // 4)  # 4 bytes per cell
        self.cmp = 0
        self.screen = ''
        self.halted = False
        self.ticks = 0
        self.time_split = time.time()
        self.cpu_freq = 0

    def load(self, code):
        for i, b in enumerate(code):
            self.memory[i] = b

    def tick(self):
        n = 20
        self.ticks += 1
        if self.ticks % n == 0:
            t0 = self.time_split
            t1 = time.time()
            self.cpu_freq = self.ticks / (t1 - t0)

    def step(self):
        self.tick()
        r = self.registers

        program_counter = self.registers[PC]
        r[PC] += 1
        
        word = self.memory[program_counter]

        opcode = (word >> 27) & 0b11111
        rn = (word >> 23) & 0b1111
        rd = (word >> 19) & 0b1111
        address_mode = (word >> 16) & 0b11
        op2 = word & 0xff

        opcode = OPCODES[opcode]
        rn = REGISTERS[rn]
        rd = REGISTERS[rd]

        #print(f'opcode={opcode} rd={rd} rn={rn} am={address_mode} op2={op2}')

        if address_mode == AM_DIRECT:
            reg = REGISTERS[op2]
            op2 = r[reg]
        elif address_mode == AM_IMMEDIATE:
            # It's the literal number
            pass

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


def render(machine, assembly):
    # ffff|ffff|ffff|ffff| ... ffff|ffff|ffff|ffff| = 16 cells * 32 = 512 = 80 chars
    row = lambda: [' '] * 80
    frame = [row() for _ in range(24)]

    def draw(x, y, s):
        for i, c in enumerate(s):
            frame[y][x + i] = c

    for n, b in enumerate(machine.memory):
        cx = n % 8
        cy = n // 8
        fx = 1 + (cx * 9)
        fy = 7 + (cy)
        s = f'{b:08x}'
        draw(fx, fy, s)

    for i, reg in enumerate(REGISTERS):
        cx = i % 8
        cy = i // 8
        fx = 0 + (cx * 5)
        fy = 0 + (cy * 2)
        v = machine.registers[reg]
        draw(fx, fy+0, reg)
        draw(fx, fy+1, f'{v:04x}')

    draw(35, 2, 'CMP')
    draw(35, 3, '{:04x}'.format(machine.cmp))

    pc = machine.registers[PC]
    la = assembly[pc - 1] if pc > 0 else ''
    lb = assembly[pc]
    lc = assembly[pc + 1] if pc < len(assembly) - 1 else ''
    draw(40, 1, f'  {pc - 1}: {la}')
    draw(40, 2, f'> {pc}: {lb}')
    draw(40, 3, f'  {pc + 1}: {lc}')

    draw(2, 5, '>' + machine.screen)
    draw(2, 6, f'{machine.cpu_freq:.2f}Hz')

    return "\n".join(''.join(row) for row in frame)


assembly = (
        (None, MOV, R5, 5),  # <-- what is x! ?

        (None, MOV, R6, PC),
        (None, ADD, R6, R6, 2),
        (None, B, 'factorial'),
        (None, OUT, R4, DEV_UINT),

        (None, HALT),

        # R0 = R1 * R2; return to address in memory @R3
        ('multiply', NOOP),
        (None, MOV, R0, 0),
        ('multiply_inner', NOOP),
        (None, ADD, R0, R0, R1),
        (None, SUB, R2, R2, 1),
        (None, CMP, R2, 0),
        (None, BNE, 'multiply_inner'),
        (None, MOV, PC, R3),

        # R4 = R5!; return to address in @R6
        ('factorial', NOOP),

        (None, MOV, R4, 1),

        ('factorial_inner', NOOP),

        (None, OUT, R5, DEV_UINT),
        #(None, OUT, DEV_UINT, R1),
        #(None, OUT, DEV_CHAR, ord('=')),

        (None, CMP, R5, 1),
        (None, BEQ, 'factorial_return'),

        (None, MOV, R9, ord('*')),
        (None, OUT, R9, DEV_CHAR),

        # R4 = R4 * R5
        # R5--
        (None, MOV, R1, R4),
        (None, MOV, R2, R5),
        #(None, INP),
        (None, MOV, R3, PC),
        (None, ADD, R3, R3, 2),
        (None, B, 'multiply'),
        #(None, INP),
        (None, MOV, R4, R0),
        (None, SUB, R5, R5, 1),
        (None, B, 'factorial_inner'),
        
        ('factorial_return', NOOP),
        (None, MOV, R9, ord('=')),
        (None, OUT, R9, DEV_CHAR),
        (None, MOV, PC, R6)


        )

with open('fact.asm') as f:
    code = f.read()
    code = parse(code)
    print(code)

machine_code = assemble(assembly)

m = Machine()
m.load(machine_code)

print(render(m, assembly))

while not m.halted:
    print("\033[0;0H")
    print(render(m, assembly))
    time.sleep(0.01)
    m.step()
