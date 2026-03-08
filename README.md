# mygrep — A Python grep implementation

A beginner-friendly, from-scratch Python implementation of the classic Unix
`grep` command. Built to learn how string searching works under the hood.

---

## What is this?

`mygrep` searches through text files for lines that match a given pattern and
prints them to the terminal — just like the real `grep` command. The core
search algorithm is implemented manually (no built-in `str.find` or `in`
operator) so you can see exactly how pattern matching works.

---

## Installation

No external packages needed — only the Python standard library is used.

```bash
git clone https://github.com/VN45/grep-project.git
cd grep-project
```

---

## Usage

```bash
# Basic search — print all lines that contain "hello"
python main.py "hello" sample.txt

# Or run as a Python module (works the same way)
python -m mygrep "hello" sample.txt

# Show line numbers with -n
python main.py -n "pattern" sample.txt

# Case-insensitive search with -i
python main.py -i "Hello" sample.txt

# Invert match (show non-matching lines) with -v
python main.py -v "hello" sample.txt

# Count matching lines with -c
python main.py -c "hello" sample.txt

# Regex search with -E
python main.py -E "hel+o" sample.txt

# Recursive directory search with -r
python main.py -r "pattern" src/

# Color output
python main.py --color always "hello" sample.txt

# Search multiple files at once
python main.py "hello" file1.txt file2.txt

# Use KMP or Boyer-Moore algorithm
python main.py --algorithm kmp "pattern" sample.txt
python main.py --algorithm boyer-moore "pattern" sample.txt

# Show all available options
python main.py --help
```

### All options

```
positional arguments:
  pattern               The search pattern (string or regular expression)
  files                 One or more files or directories to search in

optional arguments:
  -h, --help            Show this help message and exit
  -n, --line-number     Prefix each output line with its line number
  -i, --ignore-case     Case-insensitive matching
  -v, --invert-match    Select non-matching lines
  -c, --count           Print only a count of matching lines per file
  -E, --regex           Treat the pattern as a regular expression
  -r, --recursive       Recursively search directories
  --color {auto,always,never}
                        Highlight matching text (default: auto)
  --algorithm {naive,kmp,boyer-moore}
                        String matching algorithm (default: naive)
```

---

## Project structure

```
grep-project/
├── mygrep/
│   ├── __init__.py      # Makes mygrep a Python package
│   ├── __main__.py      # Allows running as: python -m mygrep
│   ├── cli.py           # Argument parsing with argparse
│   ├── matcher.py       # Naive, KMP, and Boyer-Moore matching algorithms
│   ├── searcher.py      # Opens files, collects matching lines, recursive search
│   └── output.py        # Formats and prints results (count mode, color)
├── tests/
│   ├── __init__.py
│   └── test_basic.py    # Unit tests (Python unittest)
├── main.py              # Entry point — run this to use mygrep
├── naive.py             # Legacy file (kept for backward compatibility)
├── sample.txt           # Example file for testing
├── requirements.txt     # No external dependencies
└── README.md
```

---

## Running the tests

```bash
python -m unittest discover -s tests
```

---

## Exit codes

| Code | Meaning                    |
|------|----------------------------|
| 0    | At least one match found   |
| 1    | No matches found           |
| 2    | Error (e.g. file not found)|

---

## Roadmap

- **Phase 1 (complete):** Basic search, `-n` line numbers, argparse CLI
- **Phase 2 (complete):** `-i` case-insensitive, `-v` invert match, `-c` count mode
- **Phase 3 (complete):** `-E` regex support, `-r` recursive directory search, `--color` output
- **Phase 4 (complete):** Performance — KMP and Boyer-Moore algorithms, `--algorithm` flag

---

> This is a learning project. The goal is to understand how grep works by
> building it from scratch in Python, one feature at a time.

