# The Hack computer
This project follows the computer architecture implementation of the [nand2tetris course ](https://www.nand2tetris.org/).
Each chapter has its folder with the relevant project files. Those are described below.

## Chapter 1: Basic logic gates
In a custom Hardware Description Language (HDL), we implement a series of single-bit and 16-bit And, Or, Xor, Not, and several multiplexor and demultiplexor chips.

## Chapter 2: ALU 
Building on the chips we built for CH01, more complex ones are built to fully express the minimum components of a CPU.

## Chapter 3: Memory
Completing the basic components of the von Neumann architecture, we build memory chips of different sizes composed of smaller versions (RAM chips with 8 to 16K registers), as well as smaller clocked RAM components such as basic Bit and multi-Bit Register chips and a Program Counter.

## Chapter 4: Assembly
Before building the computer by connecting all the computers in the architecture, we try out the custom Hack assembly language by writing two programs in assembly, one to perform basic integer multiplication and another for coloring a screen when there is nonzero keyboard input

## Chapter 5: Computer Architecture
Now we finally get to piece together all the hardware components into a very simple computer with 3 main parts: a ROM32K chip that is given, a CPU, and a 32KB Memory chip. Implementing the CPU is pretty satisfying once you figure out the jump directive.

## Chapter 6: Assembler
In the first half of this process, we build an assembler using a high-level language. I implemented it in Python because I wanted to focus on the logic of the assembler above any other considerations. There are 3 modules that are used in building an assembler: a C-instruction code translator, a symbol table for variable address values and pseudocommands, and a parser to remove whitespace and sort commands between their respective types.