"""
matcher.py — String/pattern matching algorithms.

This module provides functions to check whether a pattern exists
inside a line of text. The core algorithm is the naive (brute-force)
character-by-character search that was originally in naive.py.
"""


def naive_search(text, pattern):
    """
    Check whether `pattern` exists anywhere in `text` using a naive
    character-by-character comparison (no built-in `in` operator).

    Parameters
    ----------
    text : str
        The full line of text to search through.
    pattern : str
        The substring to look for.

    Returns
    -------
    bool
        True if the pattern is found in the text, False otherwise.
    """
    n = len(text)
    m = len(pattern)

    # Try every possible starting position in the text.
    for i in range(n - m + 1):
        match = True
        # Compare each character of the pattern against the text.
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            return True

    return False


def find_match(line, pattern, ignore_case=False):
    """
    Determine whether `pattern` is found in `line`.

    This is the main entry point used by the rest of the application.
    It delegates to `naive_search` and supports case-insensitive matching.

    Parameters
    ----------
    line : str
        A single line of text.
    pattern : str
        The pattern to search for.
    ignore_case : bool, optional
        If True, matching is case-insensitive (default is False).

    Returns
    -------
    bool
        True if the pattern is found in the line, False otherwise.
    """
    if ignore_case:
        # Convert both strings to lowercase before comparing.
        return naive_search(line.lower(), pattern.lower())
    return naive_search(line, pattern)
