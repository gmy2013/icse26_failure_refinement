## main.py
"""Main module for the conquest problem.


This module provides the entry point for the program, including input parsing,
output formatting, and orchestration of the combinatorial precomputation and
conquest-solving logic.

It uses only the Python standard library and imports the required classes from
combinatorics.py and conquest.py.

Classes:
    Main: Handles the main program flow, input/output, and coordination.

Functions:
    main(): Entry point for the program.
"""

import sys
from typing import List, Tuple

from combinatorics import Combinatorics
from conquest import ConquestSolver


class Main:
    """Main class to orchestrate the conquest problem solution.

    Methods:
        main(): Entry point for the program.
        parse_input(): Parses input from stdin.
        format_output(results): Formats and prints the output.
    """

    @staticmethod
    def parse_input() -> List[Tuple[int, int]]:
        """Parses input from stdin.

        Returns:
            List[Tuple[int, int]]: A list of (n, p) tuples for each test case.
        """
        input_lines = sys.stdin.read().splitlines()
        test_cases: List[Tuple[int, int]] = []
        idx = 0
        while idx < len(input_lines):
            line = input_lines[idx].strip()
            if not line:
                idx += 1
                continue
            if line.isdigit():
                t = int(line)
                idx += 1
                for _ in range(t):
                    if idx >= len(input_lines):
                        break
                    n_p = input_lines[idx].strip().split()
                    if len(n_p) != 2:
                        idx += 1
                        continue
                    n, p = map(int, n_p)
                    test_cases.append((n, p))
                    idx += 1
                break
            else:
                n_p = line.split()
                if len(n_p) == 2:
                    n, p = map(int, n_p)
                    test_cases.append((n, p))
                idx += 1
        return test_cases

    @staticmethod
    def format_output(results: List[List[int]]) -> None:
        """Formats and prints the output for each test case.

        Args:
            results (List[List[int]]): List of results, each a list of integers.
        """
        for res in results:
            print(' '.join(str(x) for x in res))

    @staticmethod
    def main() -> None:
        """Main entry point for the program."""
        # Parse input
        test_cases = Main.parse_input()
        if not test_cases:
            return

        # Determine the maximum n and p for precomputation
        max_n = max(n for n, _ in test_cases)
        max_p = max(p for _, p in test_cases)

        # For each unique modulus, precompute combinatorics up to max_n
        # (If all p are the same, only one instance is needed)
        combinatorics_map = {}
        for _, p in test_cases:
            if p not in combinatorics_map:
                combinatorics_map[p] = Combinatorics(max_n=max_n, p=p)

        results: List[List[int]] = []
        for n, p in test_cases:
            combinatorics = combinatorics_map[p]
            fact = combinatorics.get_fact()
            inv_fact = combinatorics.get_inv_fact()
            solver = ConquestSolver(n=n, p=p, fact=fact, inv_fact=inv_fact)
            res = solver.count_valid_arrays()
            results.append(res)

        Main.format_output(results)


if __name__ == "__main__":
    Main.main()
