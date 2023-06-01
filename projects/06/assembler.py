from enum import Enum, auto
import re

class Assembler:
    
    def __init__(self, file: str) -> None:
        self.filename, _, _ = file.partition('\.')
        self.parser = Parser(file)
        self.symbol_table = SymbolTable()
        self.curr_ROM_addr = 0
        self.binaries = [0 * (2*15)] # ROM

    def first_pass(self):
        while self.parser.has_more_commands():
            match self.parser.command_type:
                case Command.A_COMMAND:
                    self.binaries[self.curr_ROM_addr] = bin(int(self.parser.current_cmd)).zfill(16)

                case Command.C_COMMAND:
                    c_mnem = self.parser.comp()
                    dest_mnem = self.parser.dest()
                    jump_mnem = self.parser.jump()
                    c_bin = "111" + ( Code.comp(c_mnem) + Code.dest(dest_mnem) + Code.jump(jump_mnem) )
                    assert(len(c_bin) == 16)
                    self.binaries[self.curr_ROM_addr] = ( c_bin )

                case Command.L_COMMAND:
                    self.symbol_table.add_entry(self.parser.current_cmd, self.curr_ROM_addr)
                    
            self.curr_ROM_addr += 1
            self.parser.advance()

    def second_pass(self):
        pass
    #         Now go again through the entire program, and parse each line. Each
    # time a symbolic A-instruction is encountered, namely, @Xxx where Xxx is a symbol
    # and not a number, look up Xxx in the symbol table. If the symbol is found in the
    # table, replace it with its numeric meaning and complete the command’s translation.
    # If the symbol is not found in the table, then it must represent a new variable. To
    # handle it, add the pair (Xxx, n) to the symbol table, where n is the next available
    # RAM address, and complete the command’s translation. The allocated RAM
    # addresses are consecutive numbers, starting at address 16 ( just after the addresses
    # allocated to the predefined symbols).
        # if self.parser.command_type() == Command.A_COMMAND:
        #     symb = self.parser.symbol()
        #     try:
        #         instruction = bin(int(symb))[2:].zfill(16)
        #     except ValueError:
        #         if not self.symbol_table.contains(symb):
        #             self.symbol_table.add_entry(symb, 0)

        # Check if command is A-instruction
            # If symbol, look it up in symbol table
                # If in table, replace it with numeric meaning and translate
                # If not in table, new variable -> add new pair to symbol table, where addr is the next available RAM address, and translate
            # If number, convert to binary and left-pad

        
        while self.parser.has_more_commands():
            pass # haha

    def assemble(self):
        self.first_pass()
        # get list of commands
        binaries = []
        with open(self.filename + ".hack", "w") as f:
            for cmd in binaries:
                f.write(cmd + '\n')


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

        Args:
            input_file (str): assembly file path
        """
        self.line = 0
        self.commands = []

        with open(input_file, "r") as asm:
            for cmd in asm:
                cmd_no_ws = cmd.replace(" ", "")
                cmd_no_comment, _, _ = cmd_no_ws.partition("//")
                if len( cmd_no_comment ) > 0:
                    self.commands.append(cmd_no_comment)

        try:
            self.current_cmd = self.commands[0]
        except IndexError:
            raise IndexError("Command list has length 0")

    def __str__(self):
        return self.commands

    def has_more_commands(self) -> bool:
        """Boolean for whether there are more commands in the input

            Returns:
                bool: comparison between current line and length of commands
        """
        return len(self.commands) > self.line

    def advance(self) -> None:
        """Reads the next comand from the input and makes it the current command 
        """
        if self.has_more_commands():
            self.line += 1
            self.current_cmd = self.commands[self.line-1]

    def command_type(self) -> Command:
        """Returns teh type of the current command
            
            Returns:
                Command[.A_COMMAND, C_COMMAND, L_COMMAND]: Command type of current command
        """
        if self.current_cmd[0] == "@":
            return Command.A_COMMAND
        elif self.current_cmd[0] == "(":
            return Command.L_COMMAND
        else:
            return Command.C_COMMAND

    def symbol(self) -> str:
        """Returns the symbol or decimal value of a current A or L command.

            Returns:
                str: symbol used to access A register value
        """
        if self.command_type() == Command.A_COMMAND:
            return self.current_cmd[1:]
        elif self.command_type() == Command.L_COMMAND:
            return re.match(r'\((.*?)\)', self.current_cmd).group(1)

    def dest(self) -> str | None:
        """Returns the dest mnemonic in the current C-command

            Returns:
                str | None: dest mnemonic string of C command
        """
        if '=' in self.current_cmd and self.command_type() == Command.C_COMMAND:
            return self.current_cmd.split('=')[0].strip()
        else:
            return None

    def comp(self) -> str:
        """Returns the comp mnemonic in the current C-command

            Returns:
                str | None: comp mnemonic string of C command
        """
        if self.command_type() == Command.C_COMMAND:
            if self.dest() is not None:
                return self.current_cmd.split('=')[1].strip()
            elif self.jump() is not None:
                return self.current_cmd.split(';')[0].strip()
            else:
                return self.current_cmd
            
    def jump(self) -> str | None:
        """Returns the jump mnemonic in the current C-command

            Returns:
                str | None: jump mnemonic string of C command
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

    # def __init__(self):
    #     pass

    def dest(self, cmd: str | None) -> str:
        return Code.DEST[cmd]

    def comp(self, cmd: str) -> str:
        return Code.COMP[cmd]

    def jump(self, cmd: str | None) -> str:
        return Code.JUMP[cmd]

class SymbolTable:

    PREDEF_SYMBOLS = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "LCL": 24576,
        **{k:v for (k,v) in zip(list("R" + str(i) for i in range(0, 16)), range(0,16))} # Happy about this line
    }

    def __init__(self):
        self.table: dict = SymbolTable.PREDEF_SYMBOLS
        self.curr_ram_addr = 16
        
    # def check_R_symbol(self, symbol: str) -> bool:
    #     """Checks if symbol is R symbol

    #     Args:
    #         symbol (str): Symbol to be checked

    #     Returns:
    #         bool: True if symbol is R0-R15, False otherwise
    #     """
    #     return (symbol[0] == "R" and int(symbol[1:]) < 16)

    def add_entry(self, symbol: str, addr: int) -> None:
        """Adds a pair (symbol, addr) to symbol table
        """
        # if self.check_R_symbol(symbol):
        #     self.table[symbol[1:]] = addr
        self.table[symbol] = self.curr_ram_addr + addr
        self.curr_ram_addr += 1

    def contains(self, symbol: str) -> bool:
        """Checks whether symbol is present in symbol table

        Args:
            symbol (str): Symbol for lookup

        Returns:
            bool: True if symbol is in table, False if otherwise
        """
        # return self.check_R_symbol(symbol) or (symbol in self.table)
        return (symbol in self.table)

    def get_addr(self, symbol: str) -> int:
        """Get address of symbol if in table

        Args:
            symbol (str): Symbol for lookup

        Returns:
            int: address symbol represents
        """
        if self.check_R_symbol(symbol):
            return symbol[1:]
        else:
            return self.table[symbol]