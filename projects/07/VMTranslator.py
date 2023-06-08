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

    def gen_terminating_loop():
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
    
    def arg2(self) -> int:
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
        # "pointer": "THIS",
        # "pointer": "THAT",
        "temp": "TEMP",
        # "": **{k:v for (k,v) in zip(list("R" + str(i) for i in range(13, 16)), range(13, 16))}
    }
    
    def __init__(self, output_file: str | None = None) -> None:
        self.filename, _, self.ext = output_file.rpartition('.')
        self.output_file = output_file if self.ext == "asm" else output_file + ".asm"
        self.f = open(self.output_file, "w", encoding='ascii')
        self.stack = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback) -> None:
        self.f.close()

    def concat_asm_commands(cmd_list: list[str]) -> str:
        return '\n'.join() + '\n'

    def write_arithmetic(self, cmd: str) -> None:
        # 'add', 'sub', 'eq', 'gt', 'lt', 'and', 'or', 'not'
        self.f.write("//" + str(cmd) + "\n") # write command as comment for debugging
        match cmd:
            case "add":
                # Pop from stack => write_push_pop(Command.C_POP, segment [SOMETHING THAT TRANSLATES TO stackBase], @SP)
                # Pop from stack => write_push_pop(Command.C_POP, segment [SOMETHING THAT TRANSLATES TO stackBase], @SP)
                # Push to stack addition of both => write_push_pop(Command.C_PUSH, segment stackBase, @SP)
                pass
            case "sub":
                pass
            case "eq":
                pass
            case "gt":
                pass
            case "lt":
                pass
            case "and":
                pass
            case "or":
                pass
            case "not":
                pass
    
    def write_push_pop(self, cmd: Command.C_PUSH | Command.C_POP, segment: str, idx = int) -> None:
        # Segment + idx -> D
        # Modify address to baseAddr + idx => @segment; D=M; A=idx; D=D+A; || from here things get a bit weird: A=D; M=D;
        # Push: stack[SP++] = x -> @SP; A=M; M=D; @SP; M=M+1
        # Pop: x = stack[SP--] -> @SP; A=M; D=M; @SP; M=M-1
        segment_asm = "@" + CodeWriter.VIRTUAL_REGS[segment]
        D_setter_cmds = [ segment_asm, "D=M", f"A={idx}", "D=D+A" ] # After this, we have in D the address of the value we want within segment[index]
        if cmd == Command.C_PUSH:
            cmds = D_setter_cmds + ["@SP", "A=M", "M=D", "@SP", "M=M+1"]
            command = CodeWriter.concat_asm_commands(cmds)
        elif cmd == Command.C_POP:
            cmds = ["@SP", "A=M", "D=M", "@SP", "M=M-1"] # + D_setter_cmds // this is very incorrect. The value at segment[idx] needs
            # to be updated to D (popped stack value)
            command = CodeWriter.concat_asm_commands(cmds)
        self.f.write("//" + str(cmd) + "\n") # write command as comment for debugging
        self.f.write(command + "\n") # write command as comment for debugging

    def close(self) -> None:
        self.f.close()

def main(input_file: str, output_file: str | None = None):
    translator = VMTranslator(input_file)
    translator.translate()

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("Usage: python3 VMTranslator.py <input_file> <output_file>")
        sys.exit(1)
    if len(sys.argv) == 2:
        main(sys.argv[1])
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])