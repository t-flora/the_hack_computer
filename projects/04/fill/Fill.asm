// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
// Pseudocode:
// while true:
	// let bool key_is_pressed;
	// let bool last_iter_kp;
	// int i = RAM[SCREEN]; // start index from first screen register address
	// int last_pixel = RAM[KBD]-1
	//
	// key_is_pressed = is_key_pressed();
	// if last_iter_kp == key_is_pressed:
	//	continue // goto while
	// 
	// if key_is_pressed:
	//	while i < num_words:
	//		i += 1
	//	 	screen[i] = -1
	// if !key_is_pressed:
	//	while i < num_words:
	//		i += 1
	// 		screen[i] = 0
	// 
	// last_iter_kp = key_is_pressed;

	// Keep track of whether key was pressed last time around
	// @last_iter_kbd
	// M=0
	// Set screen size to address before KBD register
	@KBD
	D=A
	@screen_size
	M=D-1

// Main loop
(LOOP)
	// reset screen_reg_addr
	@SCREEN
	D=A
	@screen_reg_addr // TODO: This is not being set to the screen addr for some reason
	M=D
	// Check if key is pressed and go to correct loop
	@KBD
	D=M
	@BLACKEN_PIXEL // If key is pressed, blacken screen
	D;JNE
	@CLEAR_PIXEL // If key is inactive, clear screen
	D;JEQ

(BLACKEN_PIXEL)
	// Paint pixel
	@screen_reg_addr // go to current reg address
	A=M // Set A register to address in RAM[screen_reg_addr]. I tried doing @M or D=M then @D, but for some reason this wouldn't work.
	M=-1 // Set RAM[RAM[screen_reg_addr]] to -1

	// Increase reg counter
	@screen_reg_addr
	M=M+1
	D=M

	// Check conditional and jump back into KEY_PRESSED or BLACKEN_PIXEL
	@screen_size
	D=D-M
	@BLACKEN_PIXEL
	D;JLE
	@LOOP
	D;JGT

(CLEAR_PIXEL)
	// Paint pixel
	@screen_reg_addr
	A=M
	M=0

	// Increase reg addr
	@screen_reg_addr
	M=M+1
	D=M

	// Check conditional and jump back into KEY_PRESSED or BLACKEN_PIXEL
	@screen_size
	D=D-M
	@CLEAR_PIXEL
	D;JLE
	@LOOP
	D;JGT
