main:   MOV  R5, #5     // Inline label
        MOV  R6, PC
        ADD  R6, R6, #2
        B  factorial
        OUT  R4, 4
        HALT

        // R0 = R1 * R2; return to address in memory @R3
multiply:
        MOV  R0, #0
multiple_inner:
        ADD  R0, R0, R1
        SUB  R2, R2, #1
        CMP  R2, #0
        BNE  multiple_inner
        MOV  PC, R3

        // R4 = R5!; return to address in @R6
factorial:
        MOV R4, #1
factorial_inner:
        OUT R5, 4
        CMP R5, #1
        BEQ factorial_return
        MOV R9, #0x2a
        OUT R9, 7
        // R4 = R4 * R5
        // R5--
        MOV R1, R4
        MOV R2, R5
        MOV R3, PC
        ADD R3, R3, #2
        B multiply
        MOV R4, R0
        SUB R5, R5, #1
        B factorial_inner
factorial_return:
        MOV R9, #0x3D
        OUT R9, 7
        MOV PC, R6

0xedededed
0xedededed
0xedededed
