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
