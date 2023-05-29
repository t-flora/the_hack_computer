from enum import Enum
from typing import TextIO

class Assembler: 
    
    def __init__(self, file: TextIO):
        self.file = file
        self.parser = Parser(file)
        self.symbol_table = SymbolTable()

    def first_pass(self):
        pass

    def second_pass(self):
        pass # haha


class Command(Enum):
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2

class Block(Enum):
    DEST = 0
    COMP = 1
    JUMP = 2

class Parser:

    def __init__(self, input_file: str) -> None:
        self.line = 0
        self.commands = []

        with open(input_file, "r") as asm:
            for cmd in asm:
                if len(cmd) == 0:
                    continue
                cmd_no_ws = cmd.replace(" ", "")
                cmd_no_comment, _, _ = cmd_no_ws.partition("//")
                self.commands.append(cmd_no_comment)

    def __str__(self):
        return self.commands

    def has_more_commands(self) -> bool:
        pass

    def advance(self) -> None:
        if self.has_more_commands():
            self.line += 1
        else:
            pass

    def command_type(self, line: str) -> Command:
        if line[0] == "@":
            return Command.A_COMMAND
        # parse command chars and return command type
        pass

    def symbol(self) -> str:
        pass

    def dest(self) -> str:
        pass

    def comp(self) -> str:
        pass

    def jump(self) -> str:
        pass

class Code:

    def __init__(self):
        pass

    def dest(self, cmd: str) -> str:
        pass

    def comp(self, cmd: str) -> str:
        pass

    def jump(self, cmd: str) -> str:
        pass

class SymbolTable:

    def __init__(self):
        pass

    def add_entry(self, symbol: str, addr: int) -> None:
        pass

    def contains(self, symbol: str) -> bool:
        pass

    def get_addr(self, symbol: str) -> int:
        pass
