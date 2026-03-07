"""
test_basic.py — Unit tests for the mygrep package.

Run with:
    python -m unittest discover -s tests
or simply:
    python -m unittest tests/test_basic.py
"""

import io
import os
import sys
import tempfile
import types
import unittest

# Make sure the project root is on the path so we can import mygrep.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from mygrep.matcher import naive_search, kmp_search, boyer_moore_search, find_match
from mygrep.searcher import search_file, collect_files
from mygrep.output import print_results


def _make_args(
    line_number=False,
    ignore_case=False,
    invert_match=False,
    count=False,
    regex=False,
    recursive=False,
    color="never",
    algorithm="naive",
    pattern="",
):
    """Helper: create a minimal args namespace for tests."""
    return types.SimpleNamespace(
        line_number=line_number,
        ignore_case=ignore_case,
        invert_match=invert_match,
        count=count,
        regex=regex,
        recursive=recursive,
        color=color,
        algorithm=algorithm,
        pattern=pattern,
    )


# ---------------------------------------------------------------------------
# naive_search
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# kmp_search
# ---------------------------------------------------------------------------

class TestKmpSearch(unittest.TestCase):
    """Tests for the kmp_search function in matcher.py."""

    def test_pattern_found(self):
        self.assertTrue(kmp_search("hello world", "world"))

    def test_pattern_not_found(self):
        self.assertFalse(kmp_search("hello world", "python"))

    def test_pattern_at_start(self):
        self.assertTrue(kmp_search("hello world", "hello"))

    def test_pattern_at_end(self):
        self.assertTrue(kmp_search("hello world", "world"))

    def test_empty_pattern(self):
        self.assertTrue(kmp_search("anything", ""))

    def test_empty_text(self):
        self.assertFalse(kmp_search("", "pattern"))

    def test_exact_match(self):
        self.assertTrue(kmp_search("exact", "exact"))

    def test_repeated_characters(self):
        """KMP should handle patterns with repeated characters correctly."""
        self.assertTrue(kmp_search("aababababc", "ababc"))
        self.assertFalse(kmp_search("aababababc", "ababd"))


# ---------------------------------------------------------------------------
# boyer_moore_search
# ---------------------------------------------------------------------------

class TestBoyerMooreSearch(unittest.TestCase):
    """Tests for the boyer_moore_search function in matcher.py."""

    def test_pattern_found(self):
        self.assertTrue(boyer_moore_search("hello world", "world"))

    def test_pattern_not_found(self):
        self.assertFalse(boyer_moore_search("hello world", "python"))

    def test_pattern_at_start(self):
        self.assertTrue(boyer_moore_search("hello world", "hello"))

    def test_pattern_at_end(self):
        self.assertTrue(boyer_moore_search("hello world", "world"))

    def test_empty_pattern(self):
        self.assertTrue(boyer_moore_search("anything", ""))

    def test_empty_text(self):
        self.assertFalse(boyer_moore_search("", "pattern"))

    def test_exact_match(self):
        self.assertTrue(boyer_moore_search("exact", "exact"))

    def test_bad_char_heuristic(self):
        """Boyer-Moore should skip positions efficiently with mismatches."""
        self.assertTrue(boyer_moore_search("HERE IS A SIMPLE EXAMPLE", "EXAMPLE"))
        self.assertFalse(boyer_moore_search("HERE IS A SIMPLE EXAMPLE", "MISSING"))


# ---------------------------------------------------------------------------
# find_match
# ---------------------------------------------------------------------------

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

    def test_regex_mode(self):
        """find_match with use_regex=True should use regex matching."""
        self.assertTrue(find_match("hello world", r"h\w+", use_regex=True))
        self.assertFalse(find_match("hello world", r"^world", use_regex=True))

    def test_regex_ignore_case(self):
        """Regex mode should respect ignore_case."""
        self.assertTrue(find_match("Hello World", r"hello", use_regex=True, ignore_case=True))

    def test_kmp_algorithm(self):
        """find_match with algorithm='kmp' should use KMP."""
        self.assertTrue(find_match("hello world", "world", algorithm="kmp"))
        self.assertFalse(find_match("hello world", "python", algorithm="kmp"))

    def test_boyer_moore_algorithm(self):
        """find_match with algorithm='boyer-moore' should use Boyer-Moore."""
        self.assertTrue(find_match("hello world", "world", algorithm="boyer-moore"))
        self.assertFalse(find_match("hello world", "python", algorithm="boyer-moore"))

    def test_all_algorithms_agree(self):
        """All three algorithms should return the same results."""
        cases = [
            ("hello world", "world"),
            ("hello world", "python"),
            ("abcabc", "abc"),
            ("", "x"),
            ("x", ""),
        ]
        for text, pattern in cases:
            naive = find_match(text, pattern, algorithm="naive")
            kmp = find_match(text, pattern, algorithm="kmp")
            bm = find_match(text, pattern, algorithm="boyer-moore")
            self.assertEqual(naive, kmp, f"naive vs kmp for ({text!r}, {pattern!r})")
            self.assertEqual(naive, bm, f"naive vs bm for ({text!r}, {pattern!r})")


# ---------------------------------------------------------------------------
# search_file — Phase 1 basics
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# search_file — Phase 2: -i, -v, -c
# ---------------------------------------------------------------------------

class TestSearchFilePhase2(unittest.TestCase):
    """Tests for -i, -v, -c flags in search_file."""

    SAMPLE = os.path.join(os.path.dirname(__file__), "..", "sample.txt")

    def test_ignore_case(self):
        """search_file with ignore_case should match regardless of case."""
        args = _make_args(ignore_case=True)
        results = search_file(self.SAMPLE, "HELLO", args)
        self.assertIsNotNone(results)
        # "hello everybody" and "hello again"
        self.assertEqual(len(results), 2)

    def test_invert_match(self):
        """search_file with invert_match should return non-matching lines."""
        args = _make_args(invert_match=True)
        results_normal = search_file(self.SAMPLE, "hello", _make_args())
        results_invert = search_file(self.SAMPLE, "hello", args)
        # The two result sets should be disjoint in line numbers.
        normal_nums = {r[0] for r in results_normal}
        invert_nums = {r[0] for r in results_invert}
        self.assertEqual(normal_nums & invert_nums, set())

    def test_invert_match_count(self):
        """Inverted results + normal results should equal all lines."""
        args_normal = _make_args()
        args_invert = _make_args(invert_match=True)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("apple\nbanana\napricot\ncherry\n")
            fname = f.name
        try:
            normal = search_file(fname, "a", args_normal)
            invert = search_file(fname, "a", args_invert)
            self.assertEqual(len(normal) + len(invert), 4)
        finally:
            os.unlink(fname)

    def test_ignore_case_and_invert(self):
        """-i and -v combined should invert case-insensitive matches."""
        args = _make_args(ignore_case=True, invert_match=True)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Hello\nworld\nHELLO\n")
            fname = f.name
        try:
            results = search_file(fname, "hello", args)
            texts = [r[1] for r in results]
            # Only "world" should survive (doesn't match "hello" case-insensitively)
            self.assertEqual(texts, ["world"])
        finally:
            os.unlink(fname)


# ---------------------------------------------------------------------------
# search_file — Phase 3: -E regex
# ---------------------------------------------------------------------------

class TestSearchFileRegex(unittest.TestCase):
    """Tests for -E regex mode in search_file."""

    def _tmpfile(self, content):
        f = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
        f.write(content)
        f.close()
        return f.name

    def test_regex_basic(self):
        """Regex mode should match patterns using re syntax."""
        fname = self._tmpfile("cat\ndog\ncup\nfox\n")
        args = _make_args(regex=True, pattern=r"c\w+")
        results = search_file(fname, r"c\w+", args)
        os.unlink(fname)
        texts = [r[1] for r in results]
        self.assertIn("cat", texts)
        self.assertIn("cup", texts)
        self.assertNotIn("dog", texts)
        self.assertNotIn("fox", texts)

    def test_regex_anchors(self):
        """Regex mode should support anchors."""
        fname = self._tmpfile("hello world\nworld hello\n")
        args = _make_args(regex=True, pattern=r"^world")
        results = search_file(fname, r"^world", args)
        os.unlink(fname)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "world hello")

    def test_regex_ignore_case(self):
        """Regex mode combined with -i should be case-insensitive."""
        fname = self._tmpfile("Hello\nhello\nHELLO\nworld\n")
        args = _make_args(regex=True, ignore_case=True, pattern=r"hello")
        results = search_file(fname, r"hello", args)
        os.unlink(fname)
        self.assertEqual(len(results), 3)


# ---------------------------------------------------------------------------
# search_file — Phase 4: --algorithm
# ---------------------------------------------------------------------------

class TestSearchFileAlgorithms(unittest.TestCase):
    """Tests that all algorithms produce identical results via search_file."""

    SAMPLE = os.path.join(os.path.dirname(__file__), "..", "sample.txt")

    def _results_with_algo(self, algo):
        args = _make_args(algorithm=algo, pattern="hello")
        return search_file(self.SAMPLE, "hello", args)

    def test_kmp_same_as_naive(self):
        self.assertEqual(
            self._results_with_algo("naive"),
            self._results_with_algo("kmp"),
        )

    def test_bm_same_as_naive(self):
        self.assertEqual(
            self._results_with_algo("naive"),
            self._results_with_algo("boyer-moore"),
        )


# ---------------------------------------------------------------------------
# collect_files — Phase 3: -r recursive
# ---------------------------------------------------------------------------

class TestCollectFiles(unittest.TestCase):
    """Tests for collect_files in searcher.py."""

    def setUp(self):
        """Create a temporary directory tree for recursive tests."""
        self.tmpdir = tempfile.mkdtemp()
        # Create files at root level
        open(os.path.join(self.tmpdir, "a.txt"), "w").close()
        open(os.path.join(self.tmpdir, "b.txt"), "w").close()
        # Create a sub-directory with files
        subdir = os.path.join(self.tmpdir, "sub")
        os.makedirs(subdir)
        open(os.path.join(subdir, "c.txt"), "w").close()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir)

    def test_plain_files_pass_through(self):
        """collect_files should return plain files unchanged."""
        a = os.path.join(self.tmpdir, "a.txt")
        b = os.path.join(self.tmpdir, "b.txt")
        result = collect_files([a, b], recursive=False)
        self.assertEqual(result, [a, b])

    def test_recursive_finds_all_files(self):
        """With recursive=True, directories are expanded."""
        result = collect_files([self.tmpdir], recursive=True)
        basenames = sorted(os.path.basename(p) for p in result)
        self.assertEqual(basenames, ["a.txt", "b.txt", "c.txt"])

    def test_non_recursive_directory_excluded(self):
        """Without -r, directories produce no file entries."""
        result = collect_files([self.tmpdir], recursive=False)
        self.assertEqual(result, [])


# ---------------------------------------------------------------------------
# print_results — Phase 2: -c count mode
# ---------------------------------------------------------------------------

class TestPrintResultsCount(unittest.TestCase):
    """Tests for -c count output in print_results."""

    RESULTS = [(1, "hello everybody"), (3, "hello again")]

    def _capture(self, results, filename, args, multiple_files):
        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        try:
            print_results(results, filename, args, multiple_files)
        finally:
            sys.stdout = old_stdout
        return buf.getvalue()

    def test_count_single_file(self):
        """With -c and a single file, just print the count."""
        args = _make_args(count=True)
        out = self._capture(self.RESULTS, "sample.txt", args, False)
        self.assertEqual(out.strip(), "2")

    def test_count_multiple_files(self):
        """With -c and multiple files, print filename:count."""
        args = _make_args(count=True)
        out = self._capture(self.RESULTS, "sample.txt", args, True)
        self.assertEqual(out.strip(), "sample.txt:2")

    def test_count_zero(self):
        """With -c and no matches, print 0."""
        args = _make_args(count=True)
        out = self._capture([], "sample.txt", args, False)
        self.assertEqual(out.strip(), "0")


# ---------------------------------------------------------------------------
# print_results — Phase 3: --color highlighting
# ---------------------------------------------------------------------------

class TestPrintResultsColor(unittest.TestCase):
    """Tests for --color highlighting in print_results."""

    def _capture(self, results, filename, args, multiple_files):
        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        try:
            print_results(results, filename, args, multiple_files)
        finally:
            sys.stdout = old_stdout
        return buf.getvalue()

    def test_color_always_highlights(self):
        """With --color=always, the match should be wrapped in ANSI codes."""
        args = _make_args(color="always", pattern="hello")
        results = [(1, "hello world")]
        out = self._capture(results, "f.txt", args, False)
        self.assertIn("\033[1;31m", out)
        self.assertIn("\033[0m", out)
        self.assertIn("hello", out)

    def test_color_never_no_ansi(self):
        """With --color=never, no ANSI codes should appear."""
        args = _make_args(color="never", pattern="hello")
        results = [(1, "hello world")]
        out = self._capture(results, "f.txt", args, False)
        self.assertNotIn("\033[", out)
        self.assertIn("hello world", out)


if __name__ == "__main__":
    unittest.main()

