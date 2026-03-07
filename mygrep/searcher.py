"""
searcher.py — Core search engine.

This module handles opening files and finding lines that match a pattern.
It uses matcher.py to check each line and returns results as a list of
(line_number, line_text) tuples.  When the -r / --recursive flag is used,
directories are traversed with os.walk() and every file inside is searched.
"""

import os
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
        Parsed command-line arguments.  Attributes used:
        - ignore_case (bool): passed through to find_match.
        - invert_match (bool): if True, collect non-matching lines.
        - count (bool): used by output.py, not by this function.
        - line_number (bool): used by output.py, not by this function.
        - regex (bool): if True, treat pattern as a regular expression.
        - algorithm (str): "naive", "kmp", or "boyer-moore".

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
                matched = find_match(
                    line,
                    pattern,
                    ignore_case=args.ignore_case,
                    use_regex=args.regex,
                    algorithm=args.algorithm,
                )

                # -v flag: collect non-matching lines instead.
                if matched != args.invert_match:
                    results.append((line_number, line))

    except FileNotFoundError:
        # Print a helpful error message instead of crashing.
        print(f"mygrep: {filepath}: No such file or directory", file=sys.stderr)
        return None

    except UnicodeDecodeError:
        # Skip binary files silently (like grep's default behaviour).
        return []

    return results


def collect_files(paths, recursive):
    """
    Expand a list of file and/or directory paths into a flat list of files.

    When `recursive` is True, directories are traversed with os.walk().
    Non-directory paths are included as-is (existence is checked later by
    search_file so the standard error message is printed).

    Parameters
    ----------
    paths : list of str
        File or directory paths provided on the command line.
    recursive : bool
        Whether to recurse into directories.

    Returns
    -------
    list of str
        Flat list of file paths to search.
    """
    files = []
    for path in paths:
        if os.path.isdir(path):
            if recursive:
                # Walk the directory tree, collecting every file.
                for dirpath, _dirnames, filenames in os.walk(path):
                    for filename in sorted(filenames):
                        files.append(os.path.join(dirpath, filename))
            else:
                print(
                    f"mygrep: {path}: Is a directory",
                    file=sys.stderr,
                )
        else:
            files.append(path)
    return files
