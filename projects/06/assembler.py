from enum import Enum, auto
from typing import TextIO
import re

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
    A_COMMAND = auto()
    C_COMMAND = auto()
    L_COMMAND = auto()

class Block(Enum):
    DEST = 0
    COMP = 1
    JUMP = 2

class Parser:

    def __init__(self, input_file: str) -> None:
        """Opens the input file and gets ready to parse it

            input_file (str): assembly file path
        """
        self.line = 0
        self.commands = []
        self.symb_table = SymbolTable()

        with open(input_file, "r") as asm:
            for cmd in asm:
                if len(cmd) == 0:
                    continue
                cmd_no_ws = cmd.replace(" ", "")
                cmd_no_comment, _, _ = cmd_no_ws.partition("//")
                self.commands.append(cmd_no_comment)

        self.current_cmd = self.commands[0]

    def __str__(self):
        return self.commands

    def has_more_commands(self) -> bool:
        """Boolean for whether there are more commands in the input

            returns bool: comparison between current line and length of commands
        """
        return len(self.commands) > self.line

    def advance(self) -> None:
        """Reads the next comand from the input and makes it the current command 

            returns None
        """
        if self.has_more_commands():
            self.line += 1
            self.current_cmd = self.commands[self.line-1]

    def command_type(self) -> Command:
        """Returns teh type of the current command
            
            returns Command[.A_COMMAND, C_COMMAND, L_COMMAND]: Command type of current command
        """
        if self.current_cmd[0] == "@":
            return Command.A_COMMAND
        elif self.current_cmd[0] == "(":
            return Command.L_COMMAND
        else:
            return Command.C_COMMAND

    def symbol(self) -> str:
        """Returns the symbol or decimal value of a current A or L command.

            returns str: symbol used to access A register value
        """
        if self.command_type() == Command.A_COMMAND:
            return self.current_cmd[1:]
        elif self.command_type() == Command.L_COMMAND:
            return re.match(r'\((.*?)\)', self.current_cmd).group(1)

    def dest(self) -> str | None:
        """Returns the dest mnemonic in the current C-command

            returns str | None: dest mnemonic string of C command
        """
        if '=' in self.current_cmd and self.command_type() == Command.C_COMMAND:
            return self.current_cmd.split('=')[0].strip()
        else:
            return None

    def comp(self) -> str:
        """Returns the comp mnemonic in the current C-command

            returns str | None: comp mnemonic string of C command
        """
        if self.command_type() == Command.C_COMMAND:
            if self.dest() is not None:
                return self.current_cmd.split('=')[1].strip()
            elif self.jump() is not None:
                return self.current_cmd.split(';')[0].strip()
            
    def jump(self) -> str | None:
        """Returns the jump mnemonic in the current C-command

            returns str | None: jump mnemonic string of C command
        """
        if ';' in self.current_cmd and self.command_type() == Command.C_COMMAND:
            return self.current_cmd.split(';')[1].strip()
        else:
            return None

class Code:
    DEST = {
        None: '000',
        'M': '001',
        'D': '010',
        'MD': '011',
        'A': '100',
        'AM': '101',
        'AD': '110',
        'AMD': '111',
    }

    JUMP = {
        None: '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111',
    }

    COMP = {
        '0': '0101010',
        '1': '0111111',
        '-1': '0111010',
        'D': '0001100',
        'A': '0110000',
        '!D': '0001101',
        '!A': '0110001',
        '-D': '0001111',
        '-A': '0110011',
        'D+1': '0011111',
        'A+1': '0110111',
        'D-1': '0001110',
        'A-1': '0110010',
        'D+A': '0000010',
        'D-A': '0010011',
        'A-D': '0000111',
        'D&A': '0000000',
        'D|A': '0010101',
        'M': '1110000',
        '!M': '1110001',
        '-M': '1110011',
        'M+1': '1110111',
        'M-1': '1110010',
        'D+M': '1000010',
        'D-M': '1010011',
        'M-D': '1000111',
        'D&M': '1000000',
        'D|M': '1010101',
    }

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
        self.table: dict = {}

    def add_entry(self, symbol: str, addr: int) -> None:
        self.table[symbol] = addr

    def contains(self, symbol: str) -> bool:
        return self.table.get(symbol, 0) != 0

    def get_addr(self, symbol: str) -> int:
        return self.table[symbol]
