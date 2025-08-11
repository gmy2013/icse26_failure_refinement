## hidden_array_solver.py

"""Core logic for the hidden array solver.

This module provides the HiddenArraySolver class, which implements the
algorithm to count the number of valid replacements for '?' in the string s,
such that there exists an integer array a (with elements in [-m, m]) satisfying
the prefix sum constraints given by b.

Classes:
    HiddenArraySolver: Encapsulates the DP/memoization logic for the problem.
"""

from typing import List, Dict, Tuple
import itertools


class HiddenArraySolver:
    """Solves the hidden array replacement problem.

    Given n, m, b, and s, counts the number of valid replacements for '?'
    in s such that there exists an integer array a (with elements in [-m, m])
    matching s and satisfying the prefix sum constraints in b.

    Attributes:
        n (int): Length of the array and string.
        m (int): Maximum absolute value for elements in a.
        b (List[int]): List of prefix sum constraints.
        s (str): String with digits and '?'.
    """

    def __init__(self, n: int, m: int, b: List[int], s: str) -> None:
        """Initializes the solver with problem parameters.

        Args:
            n (int): Length of the array and string.
            m (int): Maximum absolute value for elements in a.
            b (List[int]): List of prefix sum constraints.
            s (str): String with digits and '?'.
        """
        self.n: int = n
        self.m: int = m
        self.b: List[int] = b
        self.s: str = s

        # Precompute positions of '?'
        self.q_indices: List[int] = [i for i, ch in enumerate(s) if ch == '?']
        self.q_count: int = len(self.q_indices)

        # For each '?', allowed digits are all integers in [-m, m]
        self.q_allowed_digits: List[List[int]] = [
            list(range(-m, m + 1)) for _ in self.q_indices
        ]

    def count_valid_replacements(self) -> int:
        """Counts the number of valid replacements for '?' in s.

        Returns:
            int: The number of valid replacements.
        """
        memo: Dict[Tuple[str, ...], bool] = {}

        if self.q_count == 0:
            # No '?', just check if s itself is valid
            if self._is_valid_assignment(list(self.s), memo):
                return 1
            return 0

        # If too many '?', warn and return 0 (intractable)
        if self.q_count > 12:
            print(
                f"Warning: Too many '?' ({self.q_count}); "
                "combinatorial explosion, returning 0."
            )
            return 0

        return self._enumerate_replacements(0, list(self.s), memo)

    def _enumerate_replacements(
        self, idx: int, current_s: List[str], memo: Dict[Tuple[str, ...], bool]
    ) -> int:
        """Recursively enumerates all possible replacements for '?'.

        Args:
            idx (int): Current index in the list of '?'-positions.
            current_s (List[str]): Current state of the string s.
            memo (Dict[Tuple[str, ...], bool]): Memoization dictionary.

        Returns:
            int: Number of valid replacements from this state.
        """
        if idx == self.q_count:
            return int(self._is_valid_assignment(current_s, memo))

        total = 0
        pos = self.q_indices[idx]
        for digit in self.q_allowed_digits[idx]:
            current_s[pos] = str(digit)
            total += self._enumerate_replacements(idx + 1, current_s, memo)
        # Restore for backtracking
        current_s[pos] = '?'
        return total

    def _is_valid_assignment(
        self, s_variant: List[str], memo: Dict[Tuple[str, ...], bool]
    ) -> bool:
        """Checks if a given assignment to s is valid.

        Args:
            s_variant (List[str]): The string s with '?' replaced by digits.
            memo (Dict[Tuple[str, ...], bool]): Memoization dictionary.

        Returns:
            bool: True if the assignment is valid, False otherwise.
        """
        key = tuple(s_variant)
        if key in memo:
            return memo[key]
        feasible = self._check_feasibility(s_variant)
        memo[key] = feasible
        return feasible

    def _check_feasibility(self, s_variant: List[str]) -> bool:
        """Checks if there exists an array a matching s_variant and constraints.

        Args:
            s_variant (List[str]): The string s with '?' replaced by digits.

        Returns:
            bool: True if feasible, False otherwise.
        """
        try:
            a: List[int] = [int(ch) for ch in s_variant]
        except ValueError:
            # Non-integer character found (should not happen)
            return False

        # Check that all a_i are in [-m, m]
        for idx, val in enumerate(a):
            if val < -self.m or val > self.m:
                return False

        # Check prefix sums
        prefix_sum: int = 0
        for i in range(self.n):
            prefix_sum += a[i]
            if prefix_sum != self.b[i]:
                return False

        return True
