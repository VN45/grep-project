"""
output.py — Output formatting for mygrep results.

This module is responsible for printing matching lines in the correct
format, following the same conventions as real grep:

  - Basic:              matching line here
  - With -n:            4:matching line here
  - Multiple files:     filename:matching line here
  - Both:               filename:4:matching line here
"""


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
        Parsed command-line arguments.  Currently used attributes:
        - line_number (bool): if True, prefix each line with its number.
    multiple_files : bool
        If True, prefix each output line with the filename.
    """
    for line_number, line_text in results:
        # Build the output prefix piece by piece.
        prefix = ""

        if multiple_files:
            # Real grep always shows the filename when searching > 1 file.
            prefix += f"{filename}:"

        if args.line_number:
            # -n flag: show the 1-based line number.
            prefix += f"{line_number}:"

        print(f"{prefix}{line_text}")
