"""
main.py — Entry point for the mygrep command-line tool.

Usage:
    python main.py "pattern" file.txt
    python main.py -n "pattern" file.txt        # show line numbers
    python main.py -i "pattern" file.txt        # case-insensitive
    python main.py -v "pattern" file.txt        # invert match
    python main.py -c "pattern" file.txt        # count matches
    python main.py -E "regex" file.txt          # regular expression
    python main.py -r "pattern" directory/      # recursive search
    python main.py --color always "pat" file.txt  # colour output
    python main.py --algorithm kmp "pat" file.txt # KMP algorithm
    python main.py --help                        # show all options

Exit codes (like real grep):
    0  — at least one match was found
    1  — no matches found
    2  — an error occurred (e.g. file not found)
"""

import sys

from mygrep import cli, searcher, output


def main():
    """Parse arguments, search each file, and print the results."""
    # Parse all command-line flags and positional arguments.
    args = cli.parse_args()

    # Track whether we found any match at all (for the exit code).
    any_match = False
    had_error = False

    # Expand directories (when -r is used) into a flat list of files.
    files = searcher.collect_files(args.files, recursive=args.recursive)

    if not files:
        # All paths were directories without -r, or no paths given.
        sys.exit(2)

    # When searching more than one file, prefix each line with the filename.
    multiple_files = len(files) > 1

    for filepath in files:
        results = searcher.search_file(filepath, args.pattern, args)

        if results is None:
            # search_file already printed an error message.
            had_error = True
            continue

        if results:
            any_match = True

        output.print_results(results, filepath, args, multiple_files)

    # Choose the correct exit code.
    if had_error:
        sys.exit(2)
    elif any_match:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
