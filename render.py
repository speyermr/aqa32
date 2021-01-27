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
