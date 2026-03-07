"""
searcher.py — Core search engine.

This module handles opening files and finding lines that match a pattern.
It uses matcher.py to check each line and returns results as a list of
(line_number, line_text) tuples.
"""

import sys

from mygrep.matcher import find_match


def search_file(filepath, pattern, args):
    """
    Search a single file for lines that match `pattern`.

    Opens `filepath` line by line, uses `find_match` from matcher.py
    to test each line, and collects the results.

    Parameters
    ----------
    filepath : str
        Path to the file to search.
    pattern : str
        The pattern to look for in each line.
    args : argparse.Namespace
        Parsed command-line arguments.  Attributes present on the namespace:
        - ignore_case (bool): passed through to find_match.
        - line_number (bool): used by output.py, not by this function.
        - invert_match (bool): accepted but not yet used (Phase 2).
        - count (bool): accepted but not yet used (Phase 2).

    Returns
    -------
    list of (int, str)
        Each tuple is (1-based line number, line text without newline).
        Returns an empty list if no matches are found.
        Returns None if the file could not be opened.
    """
    results = []

    try:
        with open(filepath, "r") as file:
            # Enumerate starting at 1 so line numbers are human-friendly.
            for line_number, line in enumerate(file, start=1):
                # Remove the trailing newline character before matching.
                line = line.rstrip("\n")

                # Check whether the line matches the pattern.
                if find_match(line, pattern, ignore_case=args.ignore_case):
                    results.append((line_number, line))

    except FileNotFoundError:
        # Print a helpful error message instead of crashing.
        print(f"mygrep: {filepath}: No such file or directory", file=sys.stderr)
        return None

    return results
