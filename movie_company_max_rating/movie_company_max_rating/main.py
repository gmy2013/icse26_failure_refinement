## main.py

import sys
from typing import List


class MovieCompanyMaxRating:
    """Encapsulates logic to maximize the minimum rating between two movies."""

    @staticmethod
    def max_company_rating(n: int, a: List[int], b: List[int]) -> int:
        """Finds the maximum possible minimum rating between two movies.

        Each viewer can be assigned to review either movie 1 or movie 2.
        The goal is to assign each viewer to one movie such that the minimum
        of the total ratings for the two movies is maximized.

        Args:
            n: Number of viewers.
            a: List of viewer attitudes towards movie 1.
            b: List of viewer attitudes towards movie 2.

        Returns:
            The maximum possible minimum total rating between the two movies.
        """
        # Precompute total sum of all ratings for both movies
        total_a = sum(a)
        total_b = sum(b)

        # The problem reduces to partitioning viewers into two groups,
        # assigning each viewer to either movie 1 or movie 2, such that
        # the minimum of the two total ratings is maximized.

        # For each viewer, we can choose to assign their rating to movie 1 or movie 2.
        # Let S be the set of viewers assigned to movie 1.
        # The total for movie 1: sum(a[i] for i in S)
        # The total for movie 2: sum(b[i] for i not in S)
        # The minimum is min(sum_a, sum_b)
        # We want to maximize this minimum.

        # We can use binary search on the answer.
        # For a candidate value x, can we assign viewers so that both movies get at least x?

        def can_achieve(x: int) -> bool:
            # For each viewer, we have two choices:
            # Assign to movie 1: contributes a[i] to movie 1, 0 to movie 2
            # Assign to movie 2: contributes 0 to movie 1, b[i] to movie 2
            # We need to select a subset S such that:
            #   sum(a[i] for i in S) >= x
            #   sum(b[i] for i not in S) >= x
            # Equivalently:
            #   sum(a[i] for i in S) >= x
            #   total_b - sum(b[i] for i in S) >= x
            #   sum(b[i] for i in S) <= total_b - x
            # So, for all subsets S, is there one such that
            #   sum(a[i] for i in S) >= x and sum(b[i] for i in S) <= total_b - x

            # This is a classic knapsack variant.
            # We can use DP: dp[s] = max sum_a achievable with sum_b <= s
            # But since n <= 2e5, we need a greedy approach.

            # For each viewer, the "cost" of assigning to movie 1 is that we lose b[i] from movie 2.
            # Let's sort viewers by (a[i] + b[i]) descending, and try to assign those with higher a[i] to movie 1.

            # Instead, we can try all possible assignments by sorting by (a[i] - b[i]) descending.
            # Assign top k to movie 1, rest to movie 2.

            # Try all possible k (from 0 to n), and check if min(sum_a, sum_b) >= x

            # To optimize, we can precompute prefix sums.
            ab = list(zip(a, b))
            ab.sort(key=lambda pair: (pair[0] - pair[1]), reverse=True)
            prefix_a = [0] * (n + 1)
            prefix_b = [0] * (n + 1)
            for i in range(n):
                prefix_a[i + 1] = prefix_a[i] + ab[i][0]
                prefix_b[i + 1] = prefix_b[i] + ab[i][1]
            for k in range(n + 1):
                sum_a = prefix_a[k]
                sum_b = total_b - prefix_b[k]
                if sum_a >= x and sum_b >= x:
                    return True
            return False

        # Binary search for the answer
        left = 0
        right = max(sum(a), sum(b))
        answer = 0
        while left <= right:
            mid = (left + right) // 2
            if can_achieve(mid):
                answer = mid
                left = mid + 1
            else:
                right = mid - 1
        return answer


class CLI:
    """Handles command-line interface for the MovieCompanyMaxRating problem."""

    def run(self) -> None:
        """Reads input, processes test cases, and prints results."""
        input_lines = sys.stdin.read().splitlines()
        t = int(input_lines[0])
        idx = 1
        for _ in range(t):
            n = int(input_lines[idx])
            idx += 1
            a = list(map(int, input_lines[idx].split()))
            idx += 1
            b = list(map(int, input_lines[idx].split()))
            idx += 1
            result = MovieCompanyMaxRating.max_company_rating(n, a, b)
            print(result)


if __name__ == "__main__":
    CLI().run()
