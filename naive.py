# DEPRECATED: The naive_search function has moved to mygrep/matcher.py.
# This file is kept for backward compatibility only.
# Please use `from mygrep.matcher import naive_search` in new code.

from mygrep.matcher import naive_search  # re-export from new location

__all__ = ["naive_search"]

