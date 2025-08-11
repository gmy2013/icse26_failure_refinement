## main.py

from typing import List, Tuple


class InputParser:
    """Handles parsing of input data for the visit overlap optimizer."""

    @staticmethod
    def parse_input() -> Tuple[int, List[Tuple[int, int, int, List[Tuple[int, int]]]]]:
        """
        Parses the input from standard input.

        Returns:
            Tuple containing:
                - t: Number of test cases.
                - test_cases: List of tuples, each containing:
                    - n: Number of days.
                    - k: Number of jobs.
                    - d: Length of the visit window.
                    - jobs: List of (l, r) tuples for each job.
        """
        import sys

        input_lines = sys.stdin.read().splitlines()
        idx = 0
        t = int(input_lines[idx])
        idx += 1
        test_cases = []
        for _ in range(t):
            n_k_d = input_lines[idx].split()
            n = int(n_k_d[0])
            k = int(n_k_d[1])
            d = int(n_k_d[2])
            idx += 1
            jobs = []
            for _ in range(k):
                l_r = input_lines[idx].split()
                l = int(l_r[0])
                r = int(l_r[1])
                jobs.append((l, r))
                idx += 1
            test_cases.append((n, k, d, jobs))
        return t, test_cases


class VisitOverlapOptimizer:
    """Core logic for finding optimal visit start days for maximum and minimum job overlap."""

    @staticmethod
    def process_test_case(
        n: int, d: int, jobs: List[Tuple[int, int]]
    ) -> Tuple[int, int]:
        """
        Processes a single test case to find the optimal start days.

        Args:
            n: Number of days.
            d: Length of the visit window.
            jobs: List of (l, r) tuples for each job.

        Returns:
            Tuple containing:
                - brother_start: Start day for maximum overlap.
                - mother_start: Start day for minimum overlap.
        """
        return VisitOverlapOptimizer.find_optimal_start_days(n, d, jobs)

    @staticmethod
    def find_optimal_start_days(
        n: int, d: int, jobs: List[Tuple[int, int]]
    ) -> Tuple[int, int]:
        """
        Finds the start days for maximum and minimum job overlap in a d-day window.

        Args:
            n: Number of days.
            d: Length of the visit window.
            jobs: List of (l, r) tuples for each job.

        Returns:
            Tuple containing:
                - brother_start: Start day for maximum overlap.
                - mother_start: Start day for minimum overlap.
        """
        # The possible start days for the d-day window are from 1 to n-d+1
        window_count = n - d + 1
        if window_count <= 0:
            # If d > n, no valid window
            return (1, 1)

        # Use a difference array to efficiently count overlaps for each window start
        diff = [0] * (window_count + 2)  # 1-based indexing

        for l, r in jobs:
            # The job [l, r] overlaps with window starting at s if:
            # [s, s+d-1] and [l, r] overlap
            # That is, s+d-1 >= l and s <= r
            # => s >= l - d + 1 and s <= r
            start = max(1, l - d + 1)
            end = min(window_count, r)
            if start > end:
                continue
            diff[start] += 1
            diff[end + 1] -= 1

        # Compute prefix sum to get the number of overlapping jobs for each window start
        overlap = [0] * (window_count + 2)  # 1-based indexing
        for i in range(1, window_count + 1):
            overlap[i] = overlap[i - 1] + diff[i]

        # Find the start day(s) with maximum and minimum overlap
        max_overlap = -1
        min_overlap = float('inf')
        brother_start = 1
        mother_start = 1
        for i in range(1, window_count + 1):
            if overlap[i] > max_overlap:
                max_overlap = overlap[i]
                brother_start = i
            if overlap[i] < min_overlap:
                min_overlap = overlap[i]
                mother_start = i

        return (brother_start, mother_start)


class OutputFormatter:
    """Handles formatting and output of results."""

    @staticmethod
    def format_output(results: List[Tuple[int, int]]) -> None:
        """
        Outputs the results for all test cases.

        Args:
            results: List of tuples (brother_start, mother_start) for each test case.
        """
        for brother_start, mother_start in results:
            print(f"{brother_start} {mother_start}")


class Main:
    """Main class to orchestrate the program flow."""

    @staticmethod
    def main() -> None:
        """
        Main entry point for the program.
        """
        t, test_cases = InputParser.parse_input()
        results: List[Tuple[int, int]] = []
        for test_case in test_cases:
            n, k, d, jobs = test_case
            result = VisitOverlapOptimizer.process_test_case(n, d, jobs)
            results.append(result)
        OutputFormatter.format_output(results)


if __name__ == "__main__":
    Main.main()
