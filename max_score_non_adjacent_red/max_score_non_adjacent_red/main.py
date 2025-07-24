## main.py

import argparse
import sys
from typing import List, Tuple

from solver import MaxScoreSolver


class Main:
    """Main class for handling input, output, and program flow."""

    def run(self) -> None:
        """Runs the main program logic."""
        test_cases = self.parse_input()
        solver = MaxScoreSolver()
        results = solver.solve_all(test_cases)
        self.print_output(results)

    def parse_input(self) -> List[Tuple[int, List[int]]]:
        """Parses command-line input for test cases.

        Returns:
            A list of tuples, each containing the number of elements and the array.
        """
        parser = argparse.ArgumentParser(
            description="Maximize score by selecting non-adjacent elements."
        )
        parser.add_argument(
            "--input",
            type=str,
            default=None,
            help="Input file path. If not provided, reads from stdin.",
        )
        args = parser.parse_args()

        input_lines: List[str]
        if args.input:
            try:
                with open(args.input, "r", encoding="utf-8") as f:
                    input_lines = [line.strip() for line in f if line.strip()]
            except (OSError, IOError) as e:
                print(f"Error reading input file: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            input_lines = [line.strip() for line in sys.stdin if line.strip()]

        if not input_lines:
            print("No input provided.", file=sys.stderr)
            sys.exit(1)

        try:
            t = int(input_lines[0])
        except ValueError:
            print("First line must be the number of test cases.", file=sys.stderr)
            sys.exit(1)

        test_cases: List[Tuple[int, List[int]]] = []
        idx = 1
        for case_num in range(t):
            if idx >= len(input_lines):
                print(
                    f"Insufficient input for test case {case_num + 1}.",
                    file=sys.stderr,
                )
                sys.exit(1)
            try:
                n = int(input_lines[idx])
            except ValueError:
                print(
                    f"Invalid number of elements for test case {case_num + 1}.",
                    file=sys.stderr,
                )
                sys.exit(1)
            idx += 1
            if idx >= len(input_lines):
                print(
                    f"Missing array for test case {case_num + 1}.",
                    file=sys.stderr,
                )
                sys.exit(1)
            arr_strs = input_lines[idx].split()
            if len(arr_strs) != n:
                print(
                    f"Array length mismatch for test case {case_num + 1}: expected {n}, got {len(arr_strs)}.",
                    file=sys.stderr,
                )
                sys.exit(1)
            try:
                arr = [int(x) for x in arr_strs]
            except ValueError:
                print(
                    f"Invalid integer in array for test case {case_num + 1}.",
                    file=sys.stderr,
                )
                sys.exit(1)
            test_cases.append((n, arr))
            idx += 1

        return test_cases

    def print_output(self, results: List[int]) -> None:
        """Prints the results for all test cases.

        Args:
            results: List of maximum scores for each test case.
        """
        for score in results:
            print(score)


if __name__ == "__main__":
    main = Main()
    main.run()
