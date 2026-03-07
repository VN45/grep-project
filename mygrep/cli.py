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
        The search pattern (string to look for).
    files : list[str] (positional)
        One or more files to search in.
    -n / --line-number : bool
        Prefix each output line with its 1-based line number.
    -i / --ignore-case : bool
        Accepted by the parser but not yet functional (Phase 2).
    -v / --invert-match : bool
        Accepted by the parser but not yet functional (Phase 2).
    -c / --count : bool
        Accepted by the parser but not yet functional (Phase 2).

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
        help="The search pattern (string to search for)",
    )

    # Positional: one or more file paths.
    parser.add_argument(
        "files",
        nargs="+",
        help="One or more files to search in",
    )

    # Optional flags — only -n is fully implemented in Phase 1.
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

    return parser.parse_args()
