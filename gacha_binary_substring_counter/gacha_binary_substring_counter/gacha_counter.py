## gacha_counter.py

"""Module for counting balanced binary substrings in all subranges.

This module provides the GachaBinarySubstringCounter class, which efficiently
counts, for every possible subrange (l, r) in a binary string, the number of
substrings with equal numbers of 0s and 1s. The implementation leverages prefix
sums and combinatorial mathematics for optimal performance.

Dependencies:
    - numpy>=1.18.0
"""

from typing import Dict
import numpy as np
from collections import Counter


class GachaBinarySubstringCounter:
    """Class for counting balanced binary substrings in all subranges."""

    @staticmethod
    def count_balanced_substrings_all_ranges(s: str) -> int:
        """Count the total number of balanced substrings in all subranges.

        For every possible subrange (l, r) in the binary string s, counts the
        number of substrings within s[l..r] that have equal numbers of 0s and 1s.

        Args:
            s: A binary string consisting of characters '0' and '1'.

        Returns:
            The total count of balanced substrings over all subranges.
        """
        n: int = len(s)
        total: int = 0

        # Precompute prefix sums for the entire string.
        # Map '0' to -1, '1' to +1.
        arr: np.ndarray = np.fromiter(
            ((-1 if ch == '0' else 1) for ch in s), dtype=np.int64, count=n
        )
        prefix_sum: np.ndarray = np.zeros(n + 1, dtype=np.int64)
        prefix_sum[1:] = np.cumsum(arr)

        # For each possible subrange (l, r), we want to count the number of
        # substrings with equal number of 0s and 1s.
        # Instead of O(n^3), we use the following trick:
        # For each starting index l, we maintain a Counter of prefix sums
        # and for each r >= l, we update the Counter and count the number of
        # pairs with the same prefix sum difference.

        # To optimize, we process all possible starting indices.
        for l in range(n):
            # For substring s[l..], we need to count the number of substrings
            # with equal 0s and 1s starting at l.
            # We use a Counter to count prefix sums.
            counter: Counter = Counter()
            counter[0] = 1  # The empty prefix
            curr_sum: int = 0
            for r in range(l, n):
                curr_sum += arr[r]
                total += counter[curr_sum]
                counter[curr_sum] += 1

        return total

    @staticmethod
    def _count_balanced_substrings(s: str) -> int:
        """Count the number of balanced substrings in the given string.

        This is a helper function that counts the number of substrings in s
        with equal numbers of 0s and 1s.

        Args:
            s: A binary string.

        Returns:
            The count of balanced substrings in s.
        """
        n: int = len(s)
        arr: np.ndarray = np.fromiter(
            ((-1 if ch == '0' else 1) for ch in s), dtype=np.int64, count=n
        )
        prefix_sum: np.ndarray = np.zeros(n + 1, dtype=np.int64)
        prefix_sum[1:] = np.cumsum(arr)

        counter: Counter = Counter()
        counter[0] = 1
        total: int = 0
        for i in range(1, n + 1):
            total += counter[prefix_sum[i]]
            counter[prefix_sum[i]] += 1
        return total
