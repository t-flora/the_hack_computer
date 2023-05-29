import sys
import Assembler from assembler

def main(input_file: str, output_file: str = input_file):
    assembler = Assembler(input_file)
    pass

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("Usage: python assemble-script.py <input_file> <output_file>")
        sys.exit(1)
    if len(sys.argv) == 2:
        main(sys.argv[1])
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
