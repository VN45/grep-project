"""
output.py — Output formatting for mygrep results.

This module is responsible for printing matching lines in the correct
format, following the same conventions as real grep:

  - Basic:              matching line here
  - With -n:            4:matching line here
  - Multiple files:     filename:matching line here
  - Both:               filename:4:matching line here
  - With -c:            filename:3  (or just 3 for a single file)
  - With --color:       matched substring highlighted in bold red
"""

import re
import sys

# ANSI escape codes for bold-red highlighting.
_COLOR_START = "\033[1;31m"
_COLOR_END = "\033[0m"


def _use_color(args):
    """
    Determine whether color output should be used.

    Parameters
    ----------
    args : argparse.Namespace

    Returns
    -------
    bool
    """
    color = getattr(args, "color", "auto")
    if color == "always":
        return True
    if color == "never":
        return False
    # "auto": use colour only when stdout is a TTY.
    return sys.stdout.isatty()


def _highlight(line_text, pattern, args):
    """
    Return `line_text` with every occurrence of `pattern` wrapped in
    ANSI bold-red escape codes.

    When -E / --regex is active, `pattern` is used as-is for re.sub.
    Otherwise it is treated as a literal string (re.escape'd).

    Parameters
    ----------
    line_text : str
    pattern : str
    args : argparse.Namespace

    Returns
    -------
    str
    """
    use_regex = getattr(args, "regex", False)
    ignore_case = getattr(args, "ignore_case", False)
    flags = re.IGNORECASE if ignore_case else 0

    regex_pattern = pattern if use_regex else re.escape(pattern)
    return re.sub(
        regex_pattern,
        lambda m: f"{_COLOR_START}{m.group()}{_COLOR_END}",
        line_text,
        flags=flags,
    )


def print_results(results, filename, args, multiple_files):
    """
    Print the matching lines stored in `results`.

    Parameters
    ----------
    results : list of (int, str)
        Each tuple is (line_number, line_text) as returned by searcher.py.
    filename : str
        The name of the file being searched (used as prefix when
        searching multiple files).
    args : argparse.Namespace
        Parsed command-line arguments.  Used attributes:
        - line_number (bool): if True, prefix each line with its number.
        - count (bool): if True, print only the count of matching lines.
        - color (str): "auto", "always", or "never".
        - regex (bool): whether pattern is a regex (for highlighting).
        - ignore_case (bool): used for case-insensitive highlighting.
    multiple_files : bool
        If True, prefix each output line with the filename.
    """
    if args.count:
    # -c mode: print count of matching lines (prefixed with filename for multiple files).
        count = len(results)
        if multiple_files:
            print(f"{filename}:{count}")
        else:
            print(count)
        return

    color = _use_color(args)

    for line_number, line_text in results:
        # Build the output prefix piece by piece.
        prefix = ""

        if multiple_files:
            # Real grep always shows the filename when searching > 1 file.
            prefix += f"{filename}:"

        if args.line_number:
            # -n flag: show the 1-based line number.
            prefix += f"{line_number}:"

        # Optionally highlight the matched portion.
        if color:
            line_text = _highlight(line_text, args.pattern, args)

        print(f"{prefix}{line_text}")
