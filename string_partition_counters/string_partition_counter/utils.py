## utils.py

"""Utility functions for string partitioning problem.

This module provides utility functions for:
- Extracting candidate substrings t from s (excluding 'a')
- Partitioning s into substrings of t and 'a'
- Checking if s consists only of 'a'
- Validating input string s

Dependencies:
    - regex (for efficient substring search)
"""

import regex
from typing import Set, List


def get_candidate_t(s: str) -> Set[str]:
    """Extract all unique nonempty substrings of s that are not 'a'.

    Args:
        s (str): The input string.

    Returns:
        Set[str]: Set of candidate substrings t (t != 'a').
    """
    candidates: Set[str] = set()
    n: int = len(s)
    for i in range(n):
        for j in range(i + 1, n + 1):
            substr = s[i:j]
            if substr != 'a':
                candidates.add(substr)
    return candidates


def partition_string(s: str, t: str) -> List[str]:
    """Partition s into substrings, each being either t or 'a', in order.

    Args:
        s (str): The input string.
        t (str): The candidate substring t (t != 'a').

    Returns:
        List[str]: List of substrings in the partition if possible, else empty list.

    Note:
        - Partitioning is greedy and non-overlapping, left to right.
        - At each position, try to match t first, then 'a'.
        - If neither matches, partitioning fails.
    """
    result: List[str] = []
    i: int = 0
    len_s: int = len(s)
    len_t: int = len(t)
    while i < len_s:
        # Try to match t at current position
        if s.startswith(t, i):
            result.append(t)
            i += len_t
        elif s.startswith('a', i):
            result.append('a')
            i += 1
        else:
            # Cannot partition at this position
            return []
    return result


def is_all_a(s: str) -> bool:
    """Check if the string s consists only of 'a' characters.

    Args:
        s (str): The input string.

    Returns:
        bool: True if s is all 'a', False otherwise.
    """
    return all(ch == 'a' for ch in s)


def is_valid_input(s: str) -> bool:
    """Validate that s is a nonempty string of lowercase Latin letters.

    Args:
        s (str): The input string.

    Returns:
        bool: True if valid, False otherwise.
    """
    if not isinstance(s, str):
        return False
    if not s:
        return False
    return regex.fullmatch(r'[a-z]+', s) is not None
