def render(emulator, assembly, sourcemap):
    row = lambda: [' '] * 80
    frame = [row() for _ in range(24)]

    def draw(x, y, s):
        for i, c in enumerate(s):
            frame[y][x + i] = c

    for n, b in enumerate(emulator.memory):
        cx = n % 8
        cy = n // 8
        fx = 1 + (cx * 9)
        fy = 7 + (cy)
        s = f'{b:08x}'
        #draw(fx, fy, s)

    for i, v in enumerate(emulator.registers):
        cx = i % 8
        cy = i // 8
        fx = 0 + (cx * 5)
        fy = 0 + (cy * 2)
        draw(fx, fy+0, f'R{i}')
        draw(fx, fy+1, f'{v:04x}')

    draw(35, 2, 'CMP')
    draw(35, 3, '{:04x}'.format(emulator.cmp))
    draw(2, 5, '>' + emulator.screen)

    lines = assembly.splitlines()
    for i, line in enumerate(lines):
        ln = i + 1
        mk = '>' if emulator.pc == ln else ' '
        if 7 + ln < 24:
            draw(2, 7 + ln, f'{mk} {ln} {line}')

    return "\n".join(''.join(row) for row in frame)
