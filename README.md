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

# Show line numbers with -n
python main.py -n "pattern" sample.txt

# Search multiple files at once
python main.py "hello" file1.txt file2.txt

# Show all available options
python main.py --help
```

### All options

```
positional arguments:
  pattern              The search pattern (string to search for)
  files                One or more files to search in

optional arguments:
  -h, --help           Show this help message and exit
  -n, --line-number    Prefix each output line with its line number
  -i, --ignore-case    Case-insensitive matching (Phase 2)
  -v, --invert-match   Select non-matching lines (Phase 2)
  -c, --count          Print only a count of matching lines per file (Phase 2)
```

---

## Project structure

```
grep-project/
├── mygrep/
│   ├── __init__.py      # Makes mygrep a Python package
│   ├── cli.py           # Argument parsing with argparse
│   ├── matcher.py       # Naive string matching algorithm
│   ├── searcher.py      # Opens files and collects matching lines
│   └── output.py        # Formats and prints results
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

- **Phase 1 (current):** Basic search, `-n` line numbers, argparse CLI
- **Phase 2:** `-i` case-insensitive, `-v` invert match, `-c` count mode
- **Phase 3:** Regex support, recursive directory search (`-r`), colour output
- **Phase 4:** Performance — KMP / Boyer-Moore algorithms

---

> This is a learning project. The goal is to understand how grep works by
> building it from scratch in Python, one feature at a time.

