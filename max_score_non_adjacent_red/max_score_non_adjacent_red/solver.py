## solver.py

from typing import List, Tuple, Optional


class MaxScoreSolver:
    """Solver for maximizing the score by selecting non-adjacent elements."""

    def solve_case(self, n: int, arr: List[int]) -> int:
        """Solves a single test case.

        Args:
            n: The number of elements in the array.
            arr: The list of integers.

        Returns:
            The maximum score achievable by selecting a subset of non-adjacent elements,
            where the score is defined as max(red) + min(red) + count(red).
        """
        if n == 0 or not arr:
            return 0

        # dp[i] = (score, min_val, max_val, count)
        # dp[i][0]: not pick i
        # dp[i][1]: pick i
        dp: List[List[Optional[Tuple[int, int, int, int]]]] = [
            [None, None] for _ in range(n)
        ]

        # Base cases
        # If we pick the first element
        dp[0][1] = (arr[0] * 2 + 1, arr[0], arr[0], 1)
        # If we don't pick the first element
        dp[0][0] = (0, 0, 0, 0)

        for i in range(1, n):
            # Not pick i: take the best of previous (pick or not pick)
            prev0 = dp[i - 1][0]
            prev1 = dp[i - 1][1]
            if prev0 is not None and prev1 is not None:
                if prev0[0] >= prev1[0]:
                    dp[i][0] = prev0
                else:
                    dp[i][0] = prev1
            elif prev0 is not None:
                dp[i][0] = prev0
            elif prev1 is not None:
                dp[i][0] = prev1
            else:
                dp[i][0] = (0, 0, 0, 0)

            # Pick i: can only pick if i-1 was not picked
            prev_not_pick = dp[i - 1][0]
            if prev_not_pick is not None and prev_not_pick[3] > 0:
                # There is a previous selection
                min_val = min(prev_not_pick[1], arr[i])
                max_val = max(prev_not_pick[2], arr[i])
                count = prev_not_pick[3] + 1
                score = min_val + max_val + count
                dp[i][1] = (score, min_val, max_val, count)
            else:
                # Start a new selection at i
                dp[i][1] = (arr[i] * 2 + 1, arr[i], arr[i], 1)

        # The answer is the best of picking or not picking the last element
        result0 = dp[n - 1][0]
        result1 = dp[n - 1][1]
        max_score = 0
        if result0 is not None:
            max_score = max(max_score, result0[0])
        if result1 is not None:
            max_score = max(max_score, result1[0])
        return max_score

    def solve_all(self, test_cases: List[Tuple[int, List[int]]]) -> List[int]:
        """Solves all test cases.

        Args:
            test_cases: A list of tuples, each containing the number of elements and the array.

        Returns:
            A list of maximum scores for each test case.
        """
        results: List[int] = []
        for n, arr in test_cases:
            score = self.solve_case(n, arr)
            results.append(score)
        return results
