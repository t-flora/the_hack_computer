import sys
from enum import Enum, auto

class VMTranslator:

    # TODO: implement comment generator for debugging
    # TODO: implement terminating infinite loop generator
    # TODO: list order of implementation of tests for guidance
    # TESTS:
    #   1. SimpleAdd: Pushes to constants to the stack and adds them up
    #   2. StackTest: Pushes some constants onto the stack and tests all arithmetic-logical commands
    #   3. BasicTest: Execute push, pop, and arithmetic commands using the memory segments
    #   4. PointerTest: Executed push, pop, and arithmetic commands using segments `pointer`, `this`, and `that`
    #   5. StaticTest: Executes push, pop, and arithmetic commands using constants and the `static` memory segment
    
    # This will have to be rewritten
    VIRTUAL_REGS = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "TEMP": 5,
        **{k:v for (k,v) in zip(list("R" + str(i) for i in range(13, 16)), range(13, 16))}
    }

    # BASE_ADDRS = { # Segment initializations are an issue for chapter 8
    # }

    STACK_LEN = 255-16+1
    
    def __init__(self, input_file: str, output_file: str | None = None):
        self.parser = Parser(input_file=input_file)
        self.code_writer = CodeWriter(output_file=output_file)
    
    def pop(self, num: int) -> list:
        n = len(self.code_writer.stack)
        if num > len(self.code_writer.stack):
            raise ValueError("Stack underflow: there are fewer items in the stack than are being popped")
        vals = self.code_writer.stack[-num:] # There must be a smarter way of doing this, but this will do for now
        del(self.code_writer.stack[-num:]) # Side effect of modifying the stack in-place
        assert(len(self.code_writer.stack) == (n - num))
        return vals

    def push(self, val: bool | int) -> None:
        if len(self.code_writer.stack) + 1 > VMTranslator.STACK_LEN:
            raise ValueError("Stack overflow: pushing items to address higher than maximum allowed")
        self.code_writer.stack.append(val)

    def gen_terminating_loop(self) -> None:
        """Add terminating loop to asm code in CodeWriter output file
        """
        pass

    def translate(self):
        """Loops through commands on Parser object, pass each through CodeWriter methods, and obtain final file
        """
        pass
        

class Command(Enum):
    """Command enum for identifying VM commands
    """
    C_ARITHMETICAL_LOGICAL = auto()
    C_PUSH = auto()
    C_POP = auto()
    C_LABEL = auto()
    C_GOTO = auto()
    C_IF = auto()
    C_FUNCTION = auto()
    C_RETURN = auto()
    C_CALL = auto()

class Parser:

    CMD_SET = {
       'push': Command.C_PUSH,
       'pop': Command.C_POP,
    #    'add': Command.C_ARITHMETICAL_LOGICAL,
    #    'sub': Command.C_ARITHMETICAL_LOGICAL,
    #    'eq': Command.C_ARITHMETICAL_LOGICAL,
    #    'gt': Command.C_ARITHMETICAL_LOGICAL,
    #    'lt': Command.C_ARITHMETICAL_LOGICAL,
    #    'and': Command.C_ARITHMETICAL_LOGICAL,
    #    'or': Command.C_ARITHMETICAL_LOGICAL,
    #    'not': Command.C_ARITHMETICAL_LOGICAL,
       **{k:Command.C_ARITHMETICAL_LOGICAL for k in ['add', 'sub', 'eq', 'gt', 'lt', 'and', 'or', 'not']},
    }

    def __init__(self, input_file: str) -> None:
        """Opens the input file and gets ready to parse it

        Args:
            input_file (str): assembly file path
        """
        # self.line = 0
        # self.commands = []

        with open(input_file, "r") as asm:
            for cmd in asm:
                cmd_no_comment, _, _ = cmd_no_ws.partition("//")
                cmd_no_ws = cmd.split()
                if len( cmd_no_ws ) > 0:
                    self.commands.append(cmd_no_comment)

        self.num_commands = len(self.commands)

        try:
            self.current_cmd = self.commands[self.line]
        except IndexError:
            raise IndexError("Command list has length 0")


    def __str__(self) -> str:
        return str( self.commands )

    def has_more_commands(self) -> bool:
        """Boolean for whether there are more commands in the input

            Returns:
                bool: comparison between current line and length of commands
        """
        return self.line < self.num_commands

    def advance(self) -> None:
        """Reads the next comand from the input and makes it the current command 
        """
        self.line += 1
        if self.has_more_commands():
            self.current_cmd = self.commands[self.line]

    def command_type(self) -> Command:
        """Returns the type of the current command
            
            Returns:
                Command: Command type of current command from enum definition
        """
        return Parser.CMD_SET[self.current_cmd[0]]

    def arg1(self) -> str:
        match self.command_type():
            case Command.C_ARITHMETICAL_LOGICAL:
                return self.current_cmd[0]
            case Command.C_RETURN:
                raise ValueError("arg1 should not be called on a return command")
            case other:
                return self.current_cmd[1]
    
    def arg2(self) -> str:
        if self.command_type() in [Command.C_PUSH, Command.C_POP, Command.C_FUNCTION, Command.C_CALL]:
            return self.current_cmd[2]
        else:
            raise ValueError("arg2 should only be called for push, pop, function and call commands")

class CodeWriter:

    VIRTUAL_REGS = {
        "local": "LCL",
        "argument": "ARG",
        "this": "THIS",
        "that": "THAT",
        "pointer": {
                0: "THIS",
                1: "THAT",
            },
        "temp": "TEMP",
        # "": **{k:v for (k,v) in zip(list("R" + str(i) for i in range(13, 16)), range(13, 16))}
    }
    
    def __init__(self, output_file: str | None = None) -> None:
        if output_file:
            self.filename, _, self.ext = output_file.rpartition('.')
        else:
            self.filename, self.ext = "output-translator", "asm"
        self.output_file = self.filename + "." + self.ext
        self.f = open(self.output_file, "w", encoding='ascii')
        self.n = 0 # Iteration of a given assembly block label
        self.stack = [] # What do you do with this stack? Is it so that every time you have a push or pop command and you 
        # Read a value from the segment address specified and append or you pop it and set the segment address to the value popped
        # This is the role of that D register right? Since you are storing values that you need to write
        # But don't the references to @SP do that automatically? Like why do I need this list
        
        # Okay so the stack would do what? Especially if the pop and push commands are in the Translator class and not in the 
        # CodeWriter?

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback) -> None:
        self.f.close()

    def concat_asm_commands(cmd_list: list[str]) -> str:
        return '\n'.join() + '\n'

    def write_arithmetic(self, cmd: str) -> None:
        self.f.write("//" + str(cmd) + "\n") # write command as comment for debugging
        match cmd:
            case "add":
                # Pop from stack => write_push_pop(Command.C_POP, segment [SOMETHING THAT TRANSLATES TO stackBase], )
                # Pop from stack => write_push_pop(Command.C_POP, segment [SOMETHING THAT TRANSLATES TO stackBase], @SP)
                # Push to stack addition of both => write_push_pop(Command.C_PUSH, segment stackBase, @SP)
                self.write_push_pop(Command.C_POP, "pointer", 0) # Pop into THIS
                self.write_push_pop(Command.C_POP, "pointer", 1) # Pop into THAT
                """
                @THIS
                D=M
                @THAT
                A=M
                M=D+A // Store result in THAT
                
                @PUSH_OP
                """
                commands = CodeWriter.concat_asm_commands(["@THIS", "D=M", "@THAT", "A=M", "M=D+A"])
                self.f.write(commands + "\n") # write translated command
                self.write_push_pop(Command.C_PUSH, "pointer", 1)
            case "sub":
                self.write_push_pop(Command.C_POP, "pointer", 0) # Pop into THIS
                self.write_push_pop(Command.C_POP, "pointer", 1) # Pop into THAT
                """
                @THIS
                D=M
                @THAT
                A=M
                M=A-D // Store result in THAT
                
                @PUSH_OP
                """
                commands = CodeWriter.concat_asm_commands(["@THIS", "D=M", "@THAT", "A=M", "M=A-D"])
                self.f.write(commands + "\n") # write translated command
                self.write_push_pop(Command.C_PUSH, "pointer", 1)
            case "eq":
                self.write_push_pop(Command.C_POP, "pointer", 0) # Pop into THIS
                self.write_push_pop(Command.C_POP, "pointer", 1) # Pop into THAT
                f"""
                @THIS
                D=M
                @THAT
                A=M
                D=D-A 

                @PUSH_TRUE<{self.n}>
                D;JEQ
                
                @PUSH_FALSE<{self.n}>
                D;JNE

                (PUSH_TRUE<{self.n}>) // global counter for each type of label
                    @THAT
                    M=1
                    @CONTINUE_EXE<{self.n}>
                    0;JMP
                (PUSH_FALSE<{self.n}>)
                    @THAT
                    M=0
                    @CONTINUE_EXE<{self.n}>
                    0;JMP
                (CONTINUE_EXE<{self.n}>)
                """
                commands = CodeWriter.concat_asm_commands(["@THIS", "D=M", "@THAT", "A=M",
                                                           "D=D-A", f"@PUSH_TRUE<{self.n}>", "D;JEQ",
                                                           f"@PUSH_FALSE<{self.n}>", "D;JNE",
                                                           f"(PUSH_TRUE<{self.n}>)", "@THAT", "M=1", f"@CONTINUE_EXE<{self.n}>", "0;JMP",
                                                           f"(PUSH_FALSE<{self.n}>)", "@THAT", "M=0", f"@CONTINUE_EXE<{self.n}>", "0;JMP",
                                                           f"(CONTINUE_EXE<{self.n}>)"
                                                           ])
                self.f.write(commands + "\n") # write translated command
                self.write_push_pop(Command.C_PUSH, "pointer", 1)
                self.n += 1
            case "gt":
                self.write_push_pop(Command.C_POP, "pointer", 0) # Pop into THIS
                self.write_push_pop(Command.C_POP, "pointer", 1) # Pop into THAT
                f"""
                @THIS
                D=M
                @THAT
                A=M
                D=D-A 

                @PUSH_TRUE<{self.n}>
                D;JGT
                
                @PUSH_FALSE<{self.n}>
                D;JLE

                (PUSH_TRUE<{self.n}>)
                    @THAT
                    M=1
                    @CONTINUE_EXE<{self.n}>
                    0;JMP
                (PUSH_FALSE<{self.n}>)
                    @THAT
                    M=0
                    @CONTINUE_EXE<{self.n}>
                    0;JMP
                (CONTINUE_EXE<{self.n}>)
                """
                commands = CodeWriter.concat_asm_commands(["@THIS", "D=M", "@THAT", "A=M",
                                                           "D=D-A", f"@PUSH_TRUE<{self.n}>", "D;JGT",
                                                           f"@PUSH_FALSE<{self.n}>", "D;JLE",
                                                           f"(PUSH_TRUE<{self.n}>)", "@THAT", "M=1", f"@CONTINUE_EXE<{self.n}>", "0;JMP",
                                                           f"(PUSH_FALSE<{self.n}>)", "@THAT", "M=0", f"@CONTINUE_EXE<{self.n}>", "0;JMP",
                                                           f"(CONTINUE_EXE<{self.n}>)"
                                                           ])
                self.f.write(commands + "\n") # write translated command
                self.write_push_pop(Command.C_PUSH, "pointer", 1)
                self.n += 1
            case "lt":
                self.write_push_pop(Command.C_POP, "pointer", 0) # Pop into THIS
                self.write_push_pop(Command.C_POP, "pointer", 1) # Pop into THAT
                f"""
                @THIS
                D=M
                @THAT
                A=M
                D=D-A 

                @PUSH_TRUE<{self.n}>
                D;JLT
                
                @PUSH_FALSE<{self.n}>
                D;JGE

                (PUSH_TRUE<{self.n}>)
                    @THAT
                    M=1
                    @CONTINUE_EXE<{self.n}>
                    0;JMP
                (PUSH_FALSE<{self.n}>)
                    @THAT
                    M=0
                    @CONTINUE_EXE<{self.n}>
                    0;JMP
                (CONTINUE_EXE<{self.n}>)
                """
                commands = CodeWriter.concat_asm_commands(["@THIS", "D=M", "@THAT", "A=M",
                                                           "D=D-A", f"@PUSH_TRUE<{self.n}>", "D;JLT",
                                                           f"@PUSH_FALSE<{self.n}>", "D;JGE",
                                                           f"(PUSH_TRUE<{self.n}>)", "@THAT", "M=1", f"@CONTINUE_EXE<{self.n}>", "0;JMP",
                                                           f"(PUSH_FALSE<{self.n}>)", "@THAT", "M=0", f"@CONTINUE_EXE<{self.n}>", "0;JMP",
                                                           f"(CONTINUE_EXE<{self.n}>)"
                                                           ])
                self.f.write(commands + "\n") # write translated command
                self.write_push_pop(Command.C_PUSH, "pointer", 1)
                self.n += 1
            case "and":
                self.write_push_pop(Command.C_POP, "pointer", 0) # Pop into THIS
                self.write_push_pop(Command.C_POP, "pointer", 1) # Pop into THAT
                f"""
                @THIS
                D=M
                @THAT
                A=M
                D=D&A 
                @THAT
                M=D
                """
                commands = CodeWriter.concat_asm_commands(["@THIS", "D=M", "@THAT", "A=M", "D=D&A", "@THAT", "M=D"])
                self.f.write(commands + "\n") # write translated command
                self.write_push_pop(Command.C_PUSH, "pointer", 1)
            case "or":
                self.write_push_pop(Command.C_POP, "pointer", 0) # Pop into THIS
                self.write_push_pop(Command.C_POP, "pointer", 1) # Pop into THAT
                f"""
                @THIS
                D=M
                @THAT
                A=M
                D=D|A 
                @THAT
                M=D
                """
                commands = CodeWriter.concat_asm_commands(["@THIS", "D=M", "@THAT", "A=M", "D=D|A", "@THAT", "M=D"])
                self.f.write(commands + "\n") # write translated command
                self.write_push_pop(Command.C_PUSH, "pointer", 1)
            case "not":
                self.write_push_pop(Command.C_POP, "pointer", 1) # Pop into THAT
                f"""
                @THAT
                D=M
                D=!D
                @THAT
                M=D
                """
                commands = CodeWriter.concat_asm_commands(["@THAT", "D=M", "D=!D", "@THAT", "M=D"])
                self.f.write(commands + "\n") # write translated command
                self.write_push_pop(Command.C_PUSH, "pointer", 1)
            case other:
                raise ValueError("Invalid VM command passed to arithmetic writer")
    
    def write_push_pop(self, cmd: Command.C_PUSH | Command.C_POP, segment: str, idx = int) -> None:
        # Push: stack[SP++] = x -> @SP; A=M; M=D; @SP; M=M+1
        # Pop: x = stack[SP--] -> @SP; A=M; D=M; @SP; M=M-1
        segment_asm = "@" + CodeWriter.VIRTUAL_REGS[segment][idx] if (segment=="pointer") else "@" + CodeWriter.VIRTUAL_REGS[segment]
        segment_is_constant = False
        idx_asm = f"@{idx}"
        match segment:
            case "static":
                idx_asm = "@Foo." + idx
            case "constant":
                segment_is_constant = True
        if cmd == Command.C_PUSH:
            """
                @segment
                D=M
                @idx
                A=D+A
                D=M // set the value of D to contents of RAM[segmentBaseAddr + idx]

                @SP
                A=M
                M=D // add value in D to top of stack
                @SP
                M=M+1 // increment stack pointer address to next available address
            """
            if segment_is_constant:
                """
                    @idx
                    D=A
                """
                commands = CodeWriter.concat_asm_commands([ idx_asm, "A=D+A", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1" ])
            else:
                commands = CodeWriter.concat_asm_commands([ segment_asm, "D=M", idx_asm, "A=D+A", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1" ])
        elif cmd == Command.C_POP: # The lesson for the pop operation is to definitely consider the full range of `comp` functions available
            """
            @segment
            D=M // get base address
            @idx
            D=D+A // add index to base
            
            @SP
            M=M-1 // SP--
            A=M+1 // go to original SP address
            M=D // store address being popped to
            
            @SP
            D=M //
            A=A+1 // Return to where we stored address
            A=M // Go to address stored in previous stack pointer address
            M=D // write address
            """
            cmds = [ segment_asm, "D=M", f"@{idx}", "D=D+A", "@SP", "M=M-1", "A=M+1", "M=D", "@SP", "D=M", "A=A+1", "A=M", "M=D" ]
            commands = CodeWriter.concat_asm_commands(cmds)

        self.f.write("//" + str(cmd) + "\n") # write command as comment for debugging
        self.f.write(commands + "\n") # write translated command

    def close(self) -> None:
        self.f.close()

def main(input_file: str, output_file: str | None = None):
    translator = VMTranslator(input_file, output_file=output_file)
    translator.translate()

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("Usage: python3 VMTranslator.py <input_file> <output_file>")
        sys.exit(1)
    if len(sys.argv) == 2:
        main(sys.argv[1])
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])