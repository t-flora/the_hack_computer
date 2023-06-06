
class VMTranslator:

    STACK_LEN = 255-16+1
    
    def __init__(self):
        self.stack = []
    
    def pop(self, num: int) -> list:
        if num > len(self.stack):
            raise ValueError("Stack underflow: there are fewer items in the stack than are being popped")
        vals = self.stack[-num:] # There must be a smarter way of doing this, but this will do for now
        del(self.stack[-num:]) # Side effect of modifying the stack in-place
        return vals

    def push(self, val: bool | int):
        if len(self.stack) + 1 > VMTranslator.STACK_LEN:
            raise ValueError("Stack overflow: pushing items to address higher than maximum allowed")
        self.stack.append(val)

class Command(Enum):
    """Command enum for identifying VM commands
    """
    C_ARITHMETIC = auto()
    C_PUSH = auto()
    C_POP = auto()
    C_LABEL = auto()
    C_GOTO = auto()
    C_IF = auto()
    C_FUNCTION = auto()
    C_RETURN = auto()
    C_CALL = auto()

class Parser:

    def __init__(self, input_file: str) -> None:
        """Opens the input file and gets ready to parse it

        Args:
            input_file (str): assembly file path
        """
        self.line = 0
        self.commands = []

        with open(input_file, "r") as asm:
            for cmd in asm:
                assert(cmd is not None)
                cmd_no_ws = cmd.strip()
                cmd_no_comment, _, _ = cmd_no_ws.partition("//")
                if len( cmd_no_comment ) > 0:
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
        self.line += 1 # I am extremely dumb
        if self.has_more_commands():
            self.current_cmd = self.commands[self.line]

    def command_type(self) -> Command:
        """Returns teh type of the current command
            
            Returns:
                Command: Command type of current command from enum definition
        """
        pass

    def arg1(self) -> str:
        pass
    
    def arg2(self) -> int:
        pass

class CodeWriter:
    
    def __init__(self, output_file: str | None = None):
        pass

    def write_arithmetic(self, cmd: str) -> None:
        pass
    
    def write_push_pop(self, cmd: Command.C_PUSH | Command.C_POP, segment: str, idx = int) -> None:
        pass
    