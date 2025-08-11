## main.py

import sys
from typing import List, Tuple


class MinimizeArrayRangeSolver:
    """Solver for minimizing the range of an array with allowed rightward moves.

    Attributes:
        verbose (bool): If True, provides step-by-step explanation.
    """

    def __init__(self, verbose: bool = False) -> None:
        """Initializes the solver.

        Args:
            verbose (bool, optional): Enable verbose explanation. Defaults to False.
        """
        self.verbose = verbose

    def solve(self, test_cases: List[Tuple[int, List[int]]]) -> List[int]:
        """Solves all test cases.

        Args:
            test_cases (List[Tuple[int, List[int]]]): List of test cases, each as (n, a).

        Returns:
            List[int]: List of minimized ranges for each test case.
        """
        results = []
        for n, a in test_cases:
            total = sum(a)
            avg = total // n
            # The allowed operation can only move values to the right,
            # so the minimum possible difference is determined by the
            # maximum absolute value of prefix sum deviation from the average.
            prefix_sum = 0
            max_diff = 0
            for i in range(n - 1):
                prefix_sum += a[i] - avg
                max_diff = max(max_diff, abs(prefix_sum))
            results.append(max_diff)
            if self.verbose:
                self._explain(n, a, max_diff)
        return results

    def _explain(self, n: int, a: List[int], result: int) -> None:
        """Prints a step-by-step explanation for a single test case.

        Args:
            n (int): Number of elements.
            a (List[int]): The array.
            result (int): The computed minimized range.
        """
        print(f"Explanation for array: {a}")
        total = sum(a)
        avg = total // n
        print(f"Total sum: {total}, Average (floor division): {avg}")
        prefix_sum = 0
        print("Prefix sum deviations from average:")
        for i in range(n - 1):
            prefix_sum += a[i] - avg
            print(f"  After index {i}: prefix_sum = {prefix_sum}")
        print(f"Minimum possible range: {result}\n")


class CLI:
    """Command-line interface for the MinimizeArrayRangeSolver."""

    def parse_input(self) -> Tuple[List[Tuple[int, List[int]]], bool]:
        """Parses input from stdin.

        Returns:
            Tuple[List[Tuple[int, List[int]]], bool]: List of test cases and verbose flag.
        """
        args = sys.argv[1:]
        verbose = False
        if '--verbose' in args:
            verbose = True
            args.remove('--verbose')

        # Read all input at once for speed
        data = sys.stdin.read().split()
        idx = 0
        t = int(data[idx])
        idx += 1
        test_cases = []
        for _ in range(t):
            n = int(data[idx])
            idx += 1
            a = [int(data[idx + i]) for i in range(n)]
            idx += n
            test_cases.append((n, a))
        return test_cases, verbose

    def print_output(self, results: List[int]) -> None:
        """Prints the results to stdout.

        Args:
            results (List[int]): List of results to print.
        """
        for res in results:
            print(res)

    def main(self) -> None:
        """Main entry point for the CLI."""
        test_cases, verbose = self.parse_input()
        solver = MinimizeArrayRangeSolver(verbose=verbose)
        results = solver.solve(test_cases)
        self.print_output(results)


if __name__ == "__main__":
    CLI().main()
