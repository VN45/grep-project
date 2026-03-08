# Allow running mygrep as a module: python -m mygrep "pattern" file.txt

from mygrep import cli, searcher, output
import sys


def main():
    """Parse arguments, search each file, and print the results."""
    args = cli.parse_args()

    any_match = False
    had_error = False

    files = searcher.collect_files(args.files, recursive=args.recursive)

    if not files:
        sys.exit(2)

    multiple_files = len(files) > 1

    for filepath in files:
        results = searcher.search_file(filepath, args.pattern, args)

        if results is None:
            had_error = True
            continue

        if results:
            any_match = True

        output.print_results(results, filepath, args, multiple_files)

    if had_error:
        sys.exit(2)
    elif any_match:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
