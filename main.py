import sys
from naive import naive_search


def grep(pattern, filename):
    try:
        with open(filename, "r") as file:
            line_number = 1
            for line in file:
                line = line.rstrip("\n")

                if naive_search(line, pattern):
                    print(f"{line_number}: {line}")

                line_number += 1

    except FileNotFoundError:
        print("File not found.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <pattern> <filename>")
    else:
        pattern = sys.argv[1]
        filename = sys.argv[2]
        grep(pattern, filename)
