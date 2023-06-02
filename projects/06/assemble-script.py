import sys
from assembler import Assembler 

def main(input_file: str, output_file: str | None = None):
    assembler = Assembler(input_file)
    assembler.assemble(output_file=output_file)

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("Usage: python assemble-script.py <input_file> <output_file>")
        sys.exit(1)
    if len(sys.argv) == 2:
        main(sys.argv[1])
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
