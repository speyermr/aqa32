from aqa32.instructions import *

DIRECT = 0
IMMEDIATE = 1

def assemble(text):
    exe = []
    lines = text.splitlines()
    assembly, labels, sourcemap = parse(lines)
    for tokens in assembly:
        head = tokens[0]
        if head in INSTRUCTIONS:
            try:
                word = encode(labels, *tokens)
            except Exception as ex:
                address = len(exe)
                ii = sourcemap[address]
                line = lines[ii].strip()
                raise Exception(f'in instruction {ii} "{line}": {ex}')
        else:
            word = int(head, 0)
        exe.append(word)
    return exe, sourcemap

def encode(labels, instruction, *args):
    rd, rn = None, None
    am, op2 = 0, 0

    # <address>
    if instruction in {'B', 'BEQ', 'BNE', 'BGT', 'BLT'}:
        assert len(args) == 1, f'{instruction} <address>'
        op2 = to_address(labels, args[0])

    # Rd, <address>
    if instruction in {'LDR', 'STR', 'INP', 'OUT'}:
        assert len(args) == 2, f'{instruction} {Rd} {address}'
        rd, token = args
        op2 = to_address(labels, token)

    # Rd, op2
    if instruction in {'MOV', 'MVN'}:
        rd, token = args
        am, op2 = to_operand(token)

    # Rd, Rn, op2
    if instruction in {'ADD', 'SUB', 'AND', 'ORR', 'EOR', 'LSL', 'LSR'}:
        rd, rn, token = args
        am, op2 = to_operand(token)

    # Rn, op2
    if instruction in {'CMP'}:
        pass

    # none
    if instruction in {'HALT'}:
        pass
    
    opcode = INSTRUCTIONS.index(instruction)
    rd = to_register(rd) if rd else 0
    rn = to_register(rn) if rn else 0
    flags = am

    #    27   23   19  16                 0
    # ..... .... .... ... ........ ........
    #     |    |    |   |                 |
    #    op   rn   rd  am          operand2
    return (opcode << 27 | rn << 23 | rd << 19 | flags << 16 | op2)

def to_address(labels, token):
    if token in labels:
        return labels[token]
    else:
        return int(token, 0)

def to_operand(token):
    return 0, 0
    
def to_register(name):
    if name[0] == 'R':
        return int(name[1:])
    elif name == 'PC':
        return 13
    else:
        raise Exception(f'unknown register "{name}"')

def parse(lines):
    assembly = []
    labels = {}
    sourcemap = {}
    label = None
    for ii, line in enumerate(lines):
        tokens = tokenize(line)
        if tokens == []:
            continue # Empty line
        # The first token is a label if it ends in ':'
        if tokens[0][-1] == ':':
            label = tokens[0][:-1]
            tokens = tokens[1:]
        if tokens == []:
            continue # Empty line (with label)
        address = len(assembly)
        if label:
            labels[label] = address
        assembly.append(tokens)
        sourcemap[address] = ii
        label = None
    return assembly, labels, sourcemap


def tokenize(line):
    r = []
    for token in line.split(' '):
        if token == '':
            continue
        if token[0:2] == '//':
            break
        if token[-1] == ',':
            token = token[:-1]
        r.append(token)
    return r



if __name__ == '__main__':
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

    code = assemble(example)
    print(code)
