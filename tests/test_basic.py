"""
test_basic.py — Basic unit tests for the mygrep package.

Run with:
    python -m unittest discover -s tests
or simply:
    python -m unittest tests/test_basic.py
"""

import os
import sys
import types
import unittest

# Make sure the project root is on the path so we can import mygrep.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from mygrep.matcher import naive_search, find_match
from mygrep.searcher import search_file


def _make_args(line_number=False, ignore_case=False, invert_match=False, count=False):
    """Helper: create a minimal args namespace for tests."""
    args = types.SimpleNamespace(
        line_number=line_number,
        ignore_case=ignore_case,
        invert_match=invert_match,
        count=count,
    )
    return args


class TestNaiveSearch(unittest.TestCase):
    """Tests for the naive_search function in matcher.py."""

    def test_pattern_found(self):
        """naive_search should return True when the pattern is present."""
        self.assertTrue(naive_search("hello world", "world"))

    def test_pattern_not_found(self):
        """naive_search should return False when the pattern is absent."""
        self.assertFalse(naive_search("hello world", "python"))

    def test_pattern_at_start(self):
        """naive_search should find a pattern at the very beginning."""
        self.assertTrue(naive_search("hello world", "hello"))

    def test_pattern_at_end(self):
        """naive_search should find a pattern at the very end."""
        self.assertTrue(naive_search("hello world", "world"))

    def test_empty_pattern(self):
        """An empty pattern should always match (as in real grep)."""
        self.assertTrue(naive_search("anything", ""))

    def test_empty_text(self):
        """A non-empty pattern should not match an empty string."""
        self.assertFalse(naive_search("", "pattern"))

    def test_exact_match(self):
        """The pattern equals the entire text — should match."""
        self.assertTrue(naive_search("exact", "exact"))


class TestFindMatch(unittest.TestCase):
    """Tests for the find_match function in matcher.py."""

    def test_case_sensitive_match(self):
        """find_match with ignore_case=False should be case-sensitive."""
        self.assertTrue(find_match("Hello World", "Hello"))
        self.assertFalse(find_match("Hello World", "hello"))

    def test_case_insensitive_match(self):
        """find_match with ignore_case=True should ignore case."""
        self.assertTrue(find_match("Hello World", "hello", ignore_case=True))
        self.assertTrue(find_match("PYTHON", "python", ignore_case=True))

    def test_no_match(self):
        """find_match should return False when the pattern is absent."""
        self.assertFalse(find_match("hello world", "python"))


class TestSearchFile(unittest.TestCase):
    """Tests for search_file in searcher.py."""

    # Path to the sample file bundled with the project.
    SAMPLE = os.path.join(os.path.dirname(__file__), "..", "sample.txt")

    def test_finds_matching_lines(self):
        """search_file should return tuples for each matching line."""
        args = _make_args()
        results = search_file(self.SAMPLE, "hello", args)
        # sample.txt has two lines containing "hello".
        self.assertIsNotNone(results)
        self.assertEqual(len(results), 2)

    def test_returns_correct_line_numbers(self):
        """search_file should return the correct 1-based line numbers."""
        args = _make_args()
        results = search_file(self.SAMPLE, "hello", args)
        line_numbers = [r[0] for r in results]
        self.assertIn(1, line_numbers)  # "hello everybody" is line 1
        self.assertIn(3, line_numbers)  # "hello again" is line 3

    def test_no_matches(self):
        """search_file should return an empty list when nothing matches."""
        args = _make_args()
        results = search_file(self.SAMPLE, "zzznomatch", args)
        self.assertEqual(results, [])

    def test_file_not_found(self):
        """search_file should return None for a missing file."""
        args = _make_args()
        results = search_file("/nonexistent/path/file.txt", "hello", args)
        self.assertIsNone(results)


if __name__ == "__main__":
    unittest.main()
