## olympiad_dp.py

from typing import List, Optional

class OlympiadDP:
    """Dynamic Programming solution for the Olympiad navigation problem."""

    def __init__(self, a: List[int], b: List[int]) -> None:
        """
        Initializes the OlympiadDP instance.

        Args:
            a: List of integers, the score for submitting each problem.
            b: List of integers, the jump parameter for each problem.
        """
        self._a: List[int] = a
        self._b: List[int] = b
        self._n: int = len(a)
        self._dp: List[Optional[int]] = [None] * (self._n + 1)
        self._next_unvisited: List[int] = [self._n] * self._n  # Default to n (out of bounds)
        self._compute_next_unvisited()

    def compute_max_score(self) -> int:
        """
        Computes the maximum achievable score using DP.

        Returns:
            The maximum score as an integer.
        """
        return self._solve(0)

    def _compute_next_unvisited(self) -> None:
        """
        Precomputes the next unvisited index for each problem if skipped.

        For each index i, _next_unvisited[i] = i + 1.
        """
        for i in range(self._n):
            self._next_unvisited[i] = i + 1

    def _solve(self, idx: int) -> int:
        """
        Recursively computes the maximum score starting from index idx.

        Args:
            idx: The current problem index.

        Returns:
            The maximum score achievable from idx.
        """
        if idx >= self._n:
            return 0
        if self._dp[idx] is not None:
            return self._dp[idx]

        # Option 1: Skip this problem, go to next unvisited
        skip_idx = self._next_unvisited[idx]
        skip_score = self._solve(skip_idx)

        # Option 2: Submit this problem, jump by b[idx]
        submit_idx = idx + self._b[idx]
        submit_score = self._a[idx]
        if submit_idx < self._n:
            submit_score += self._solve(submit_idx)
        # else, out of bounds, just take a[idx]

        max_score = max(skip_score, submit_score)
        self._dp[idx] = max_score
        return max_score
