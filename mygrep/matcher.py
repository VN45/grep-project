"""
matcher.py — String/pattern matching algorithms.

This module provides functions to check whether a pattern exists
inside a line of text. Algorithms available:
  - naive  : brute-force character-by-character search
  - kmp    : Knuth-Morris-Pratt with failure-function preprocessing
  - boyer-moore : Boyer-Moore bad-character heuristic
  - regex  : Python re module (when -E flag is used)
"""

import re


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

    # An empty pattern always matches.
    if m == 0:
        return True

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


def _build_failure_table(pattern):
    """
    Build the KMP failure (partial-match) table for `pattern`.

    The failure table records the length of the longest proper prefix
    of each prefix of `pattern` that is also a suffix.

    Parameters
    ----------
    pattern : str
        The search pattern.

    Returns
    -------
    list of int
        Failure table of the same length as `pattern`.
    """
    m = len(pattern)
    table = [0] * m
    length = 0  # length of previous longest prefix-suffix
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            table[i] = length
            i += 1
        else:
            if length != 0:
                length = table[length - 1]
            else:
                table[i] = 0
                i += 1

    return table


def kmp_search(text, pattern):
    """
    Check whether `pattern` exists anywhere in `text` using the
    Knuth-Morris-Pratt algorithm.

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

    if m == 0:
        return True
    if n == 0:
        return False

    table = _build_failure_table(pattern)

    i = 0  # index into text
    j = 0  # index into pattern

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                return True  # found a match
        else:
            if j != 0:
                j = table[j - 1]
            else:
                i += 1

    return False


def _build_bad_char_table(pattern):
    """
    Build the bad-character shift table for the Boyer-Moore algorithm.

    For each character, the table stores the index of its rightmost
    occurrence in the pattern (excluding the last position, per the
    standard formulation).

    Parameters
    ----------
    pattern : str
        The search pattern.

    Returns
    -------
    dict
        Maps each character to the index of its last occurrence in the
        pattern (or -1 if not present, implicitly via .get default).
    """
    table = {}
    for i, ch in enumerate(pattern):
        table[ch] = i
    return table


def boyer_moore_search(text, pattern):
    """
    Check whether `pattern` exists anywhere in `text` using the
    Boyer-Moore algorithm with the bad-character heuristic.

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

    if m == 0:
        return True
    if n == 0:
        return False

    bad_char = _build_bad_char_table(pattern)

    s = 0  # shift of the pattern with respect to text
    while s <= n - m:
        j = m - 1

        # Move j left while characters match.
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            return True  # pattern found at shift s

        # Shift using bad-character heuristic.
        # bad_char.get returns the rightmost occurrence in pattern;
        # if the character is not in the pattern, shift by j+1.
        shift = j - bad_char.get(text[s + j], -1)
        s += max(1, shift)

    return False


def regex_search(text, pattern):
    """
    Check whether `pattern` (a regular expression) matches anywhere in
    `text` using Python's `re` module.

    Parameters
    ----------
    text : str
        The full line of text to search through.
    pattern : str
        A regular expression pattern.

    Returns
    -------
    bool
        True if the regex matches anywhere in the text, False otherwise.
    """
    return bool(re.search(pattern, text))


def find_match(line, pattern, ignore_case=False, use_regex=False, algorithm="naive"):
    """
    Determine whether `pattern` is found in `line`.

    This is the main entry point used by the rest of the application.
    It delegates to the selected search function and supports
    case-insensitive matching.

    Parameters
    ----------
    line : str
        A single line of text.
    pattern : str
        The pattern to search for.
    ignore_case : bool, optional
        If True, matching is case-insensitive (default is False).
    use_regex : bool, optional
        If True, treat `pattern` as a regular expression (default is False).
    algorithm : str, optional
        Which algorithm to use: "naive", "kmp", or "boyer-moore"
        (default is "naive").  Ignored when use_regex is True.

    Returns
    -------
    bool
        True if the pattern is found in the line, False otherwise.
    """
    if use_regex:
        flags = re.IGNORECASE if ignore_case else 0
        return bool(re.search(pattern, line, flags))

    # For plain-text algorithms, normalize case on both strings.
    search_line = line.lower() if ignore_case else line
    search_pattern = pattern.lower() if ignore_case else pattern

    if algorithm == "kmp":
        return kmp_search(search_line, search_pattern)
    elif algorithm == "boyer-moore":
        return boyer_moore_search(search_line, search_pattern)
    else:
        # Default: naive
        return naive_search(search_line, search_pattern)
