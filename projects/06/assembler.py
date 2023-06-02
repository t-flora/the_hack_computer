from enum import Enum, auto
import re

class Assembler:
    
    def __init__(self, file: str) -> None:
        self.filename, _, self.ext = file.rpartition('.')
        self.parser = Parser(file)
        self.symbol_table = SymbolTable()
        self.curr_ROM_addr = 0
        self.num_commands = self.parser.num_commands
        self.binaries = [0 for _ in range(self.num_commands)] # ROM
        self.symbol_line_table: dict = {}

    def convert_to_bin(arg: int) -> str:
        """Convert integer to 16-bit binary string

        Args:
            arg (int): integer to be converted

        Returns:
            str: 16-bit binary representation of input integer
        """
        return bin(arg)[2:].zfill(16)

    def first_pass(self) -> None:
        """Performs the first pass of the assembler on the target asm code.
        In the first pass:
            - All C commands are converted to binary according to the 'Code' module.
            - A commands have constant memory addresses converted to binary, and variable addresses added to binaries file as their labels
            - Pseudocommands have their symbols added to the symbol table
        """
        while self.parser.has_more_commands():
            match self.parser.command_type():
                case Command.A_COMMAND:
                    cmd = self.parser.current_cmd.partition('@')[2]
                    try:
                        const_addr = int(cmd)
                        self.binaries[self.curr_ROM_addr] = Assembler.convert_to_bin(const_addr)
                    except:
                        # This leaves all A commands with variables and labels as strings within the binaries list, which on the second pass will
                        # be looked up on the symbol table
                        self.binaries[self.curr_ROM_addr] = str(cmd) 
                    self.curr_ROM_addr += 1

                case Command.C_COMMAND:
                    c_mnem = self.parser.comp()
                    dest_mnem = self.parser.dest()
                    jump_mnem = self.parser.jump()
                    c_bin = "111" + ( Code.comp(c_mnem) + Code.dest(dest_mnem) + Code.jump(jump_mnem) )
                    self.binaries[self.curr_ROM_addr] = ( c_bin )
                    self.curr_ROM_addr += 1

                case Command.L_COMMAND:
                    cmd = re.match(r'\((.*?)\)', self.parser.current_cmd).group(1)
                    self.symbol_table.add_entry( cmd, addr=self.curr_ROM_addr )
                    
            self.parser.advance()

    def second_pass(self) -> None:
        """Performs the second pass of the assembler on the target asm code
        In the second pass:
            - All non-binary values, i.e. references to variable labels and pseudocommand labels, are looked up on the symbol table
            and added if not present
            - All addresses on the symbol table are converted to binary values and placed in the original labels' lines
            - The list of binary commands is shortened to exclude lines assigned to pseudocommands
        """
        is_bin = lambda cmd: all(char in '01' for char in str( cmd )) and (len(str( cmd ))==16)
        for i in range( len( self.binaries ) ):
            if not is_bin(self.binaries[i]): # If line isn't binary, it must be an A-command pointing to a label
                if self.symbol_table.contains(self.binaries[i]): # If the table contains the label, it should point to a ROM address with a label
                    self.binaries[i] = Assembler.convert_to_bin(self.symbol_table.get_addr(self.binaries[i]))
                else: # if the table doesn't contain the label, it should assign the lowest available addr in memory to the variable
                    self.symbol_table.add_entry(self.binaries[i])
                    self.binaries[i] = Assembler.convert_to_bin(self.symbol_table.get_addr(self.binaries[i]))

        self.binaries = self.binaries[:self.curr_ROM_addr] # Drop unnecessary lines for pseudocommands

    def assemble(self, output_file: str | None = None) -> None:
        self.first_pass()
        self.second_pass()
        op = output_file if output_file else self.filename
        
        with open(op + ".hack", "w") as f:
            for cmd in self.binaries:
                f.write(str(cmd) + '\n')

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
                assert(cmd is not None)
                cmd_no_ws = cmd.strip()
                cmd_no_comment, _, _ = cmd_no_ws.partition("//")
                if len( cmd_no_comment ) > 0:
                    self.commands.append(cmd_no_comment)

        self.num_commands = len(self.commands)

        # self.advance() # initializes parser line to 0 and 
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

    def dest(cmd: str | None) -> str:
        return Code.DEST[cmd]

    def comp(cmd: str) -> str:
        return Code.COMP[cmd]

    def jump(cmd: str | None) -> str:
        return Code.JUMP[cmd]

class SymbolTable:

    PREDEF_SYMBOLS = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576,
        **{k:v for (k,v) in zip(list("R" + str(i) for i in range(0, 16)), range(0,16))} # Happy about this line
    }

    def __init__(self):
        self.table: dict = SymbolTable.PREDEF_SYMBOLS
        self.curr_ram_addr = 16
        
    def add_entry(self, symbol: str, addr: int | None = None) -> None:
        """Adds a pair (symbol, addr) to symbol table
        """
        if addr:
            self.table[symbol] = addr
        else:
            self.table[symbol] = self.curr_ram_addr
            self.curr_ram_addr += 1

    def contains(self, symbol: str) -> bool:
        """Checks whether symbol is present in symbol table

        Args:
            symbol (str): Symbol for lookup

        Returns:
            bool: True if symbol is in table, False if otherwise
        """
        return (symbol in self.table)

    def get_addr(self, symbol: str) -> int:
        """Get address of symbol if in table

        Args:
            symbol (str): Symbol for lookup

        Returns:
            int: address symbol represents
        """
        return self.table[symbol]