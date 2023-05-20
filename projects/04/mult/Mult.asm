// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.
// Pseudocode:

// int R2 = 0;
// int loop_counter = 0;
// while loop_counter < R0:
//	loop_counter += 1
// 	R2 += R1

	@R2 // A = R2 which is _some_ location in memory figured out by the assembler
	M=0
	@loop_counter // A = loop_counter
	M=0
(LOOP)
	// Conditional check
	@loop_counter
	D=M
	@R0
	D=D-M
	
	@END 
	D;JEQ

	// Increment mult
	@R2 // load multiplication sum so far
	D=M
	@R1
	D=D+M // Add R1 to the mult sum

	// Write back into mult
	@R2
	M=D

	// Increment loop counter
	@loop_counter
	M=M+1

	@LOOP
	0;JMP // Restart loop unconditionally
(END)
	@END // Infinite loop when loop condition isn't met
	0;JMP
