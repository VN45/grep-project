"""
cli.py — Command-line interface definition using argparse.

This module defines all the flags and arguments accepted by mygrep.
Run `python main.py --help` to see the generated help message.
"""

import argparse


def parse_args():
    """
    Parse and return the command-line arguments for mygrep.

    Supported arguments
    -------------------
    pattern : str (positional)
        The search pattern (string or regex to look for).
    files : list[str] (positional)
        One or more files or directories to search in.
    -n / --line-number : bool
        Prefix each output line with its 1-based line number.
    -i / --ignore-case : bool
        Case-insensitive matching.
    -v / --invert-match : bool
        Select non-matching lines.
    -c / --count : bool
        Print only a count of matching lines per file.
    -E / --regex : bool
        Treat the pattern as a regular expression.
    -r / --recursive : bool
        Recursively search directories.
    --color : str
        Highlight matching text (auto, always, never).
    --algorithm : str
        String matching algorithm to use (naive, kmp, boyer-moore).

    Returns
    -------
    argparse.Namespace
        An object whose attributes correspond to the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog="mygrep",
        description="A Python implementation of the grep command",
    )

    # Positional: the pattern to search for.
    parser.add_argument(
        "pattern",
        help="The search pattern (string or regular expression)",
    )

    # Positional: one or more file paths.
    parser.add_argument(
        "files",
        nargs="+",
        help="One or more files or directories to search in",
    )

    # Optional flags.
    parser.add_argument(
        "-n", "--line-number",
        action="store_true",
        help="Prefix each output line with its line number",
    )
    parser.add_argument(
        "-i", "--ignore-case",
        action="store_true",
        help="Case-insensitive matching",
    )
    parser.add_argument(
        "-v", "--invert-match",
        action="store_true",
        help="Select non-matching lines",
    )
    parser.add_argument(
        "-c", "--count",
        action="store_true",
        help="Print only a count of matching lines per file",
    )
    parser.add_argument(
        "-E", "--regex",
        action="store_true",
        help="Treat the pattern as a regular expression",
    )
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Recursively search directories",
    )
    parser.add_argument(
        "--color",
        choices=["auto", "always", "never"],
        default="auto",
        help="Highlight matching text: auto (default), always, or never",
    )
    parser.add_argument(
        "--algorithm",
        choices=["naive", "kmp", "boyer-moore"],
        default="naive",
        help="String matching algorithm: naive (default), kmp, or boyer-moore",
    )

    return parser.parse_args()
