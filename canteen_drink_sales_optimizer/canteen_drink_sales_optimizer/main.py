## main.py

import sys
from typing import List, Tuple
import numpy as np
from collections import defaultdict

class InputParser:
    """Parses input from stdin for the canteen drink sales optimization problem."""

    def __init__(self) -> None:
        pass

    def parse_input(self) -> List[Tuple[int, int, List[List[int]]]]:
        """
        Parses the input from stdin.

        Returns:
            List[Tuple[int, int, List[List[int]]]]: A list of test cases, each as (n, m, grid).
        """
        input_lines = sys.stdin.read().splitlines()
        idx = 0
        t = int(input_lines[idx])
        idx += 1
        test_cases = []
        for _ in range(t):
            n, m = map(int, input_lines[idx].split())
            idx += 1
            grid = []
            for _ in range(n):
                row = list(map(int, input_lines[idx].split()))
                idx += 1
                grid.append(row)
            test_cases.append((n, m, grid))
        return test_cases


class DrinkSalesOptimizer:
    """
    Optimizes the canteen drink sales for maximum profit using dynamic programming.
    """

    def __init__(self) -> None:
        pass

    def maximize_profit(self, test_cases: List[Tuple[int, int, List[List[int]]]]) -> List[int]:
        """
        For each test case, computes the maximum profit.

        Args:
            test_cases (List[Tuple[int, int, List[List[int]]]]): List of test cases.

        Returns:
            List[int]: List of maximum profits for each test case.
        """
        results = []
        for n, m, grid in test_cases:
            result = self._max_profit_single_case(n, m, grid)
            results.append(result)
        return results

    def _max_profit_single_case(self, n: int, m: int, grid: List[List[int]]) -> int:
        """
        Computes the maximum profit for a single test case.

        Args:
            n (int): Number of days.
            m (int): Number of drink types.
            grid (List[List[int]]): Profit grid.

        Returns:
            int: Maximum profit.
        """
        # Precompute all subarray sums for each row
        subarray_sums_per_row = []
        for row in grid:
            subarray_sums = self._get_subarray_sums(row)
            subarray_sums_per_row.append(subarray_sums)

        # DP: For each day, for each subarray (l, r), store the best profit ending at (l, r)
        # State: dp_prev[(l, r)] = max profit up to previous day, ending with subarray (l, r)
        dp_prev = dict()
        # Initialize for day 0
        for l, r, s in subarray_sums_per_row[0]:
            dp_prev[(l, r)] = s

        for day in range(1, n):
            subarrays = subarray_sums_per_row[day]
            # For fast lookup, build for previous day:
            # For each possible (l, r), store the best profit
            # To efficiently find overlapping subarrays, for each possible length, build prefix max arrays
            # But since m is up to 2e5/n, we can process all pairs

            # For each subarray in current day, find the best overlapping subarray from previous day
            # Overlap: [l1, r1] and [l2, r2] overlap if not disjoint and not identical
            # i.e., max(l1, l2) <= min(r1, r2) and (l1 != l2 or r1 != r2)

            # For fast lookup, for each possible (l, r), store all previous subarrays that overlap
            # Since m is not too large, we can process all pairs

            # Build for previous day: for each possible (l, r), store in a list by length
            prev_by_length = defaultdict(list)
            for (l1, r1), profit in dp_prev.items():
                prev_by_length[r1 - l1 + 1].append((l1, r1, profit))

            # For current day, for each subarray, find the best overlapping previous subarray
            dp_curr = dict()
            for l2, r2, s2 in subarrays:
                best_prev = None
                for (l1, r1), profit in dp_prev.items():
                    # Check overlap
                    if max(l1, l2) <= min(r1, r2):
                        if l1 != l2 or r1 != r2:
                            if best_prev is None or profit > best_prev:
                                best_prev = profit
                if best_prev is not None:
                    dp_curr[(l2, r2)] = best_prev + s2
                # If no overlap, do not update (invalid transition)
            dp_prev = dp_curr

        # The answer is the maximum value in dp_prev
        if not dp_prev:
            return 0
        return max(dp_prev.values())

    def _get_subarray_sums(self, row: List[int]) -> List[Tuple[int, int, int]]:
        """
        Computes all contiguous subarray sums for a given row.

        Args:
            row (List[int]): The row of profits.

        Returns:
            List[Tuple[int, int, int]]: List of (l, r, sum) for all subarrays.
        """
        m = len(row)
        prefix = np.zeros(m + 1, dtype=np.int64)
        prefix[1:] = np.cumsum(row)
        subarrays = []
        for l in range(m):
            for r in range(l, m):
                s = int(prefix[r + 1] - prefix[l])
                subarrays.append((l, r, s))
        return subarrays


class OutputFormatter:
    """Formats and prints the output for the canteen drink sales optimization problem."""

    def __init__(self) -> None:
        pass

    def format_output(self, results: List[int]) -> None:
        """
        Prints the results, one per line.

        Args:
            results (List[int]): List of results to print.
        """
        for res in results:
            print(res)


class Main:
    """Main entry point for the canteen drink sales optimization tool."""

    @staticmethod
    def main() -> None:
        """
        Orchestrates input parsing, optimization, and output formatting.
        """
        parser = InputParser()
        test_cases = parser.parse_input()
        optimizer = DrinkSalesOptimizer()
        results = optimizer.maximize_profit(test_cases)
        formatter = OutputFormatter()
        formatter.format_output(results)


if __name__ == "__main__":
    Main.main()
