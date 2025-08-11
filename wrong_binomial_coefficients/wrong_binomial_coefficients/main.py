## main.py

"""Main CLI for wrong and standard binomial coefficient calculators.

This script parses batch input (from stdin or file), initializes the
WrongBinomialCalculator (and optionally StandardBinomialCalculator),
processes queries, and prints results. Supports a CLI flag for comparison.

Usage:
    python main.py < input.txt
    python main.py --compare < input.txt
    python main.py --input input.txt --compare

Input format:
    Q
    n1 k1
    n2 k2
    ...
    nQ kQ

Output:
    For each query, prints the wrong binomial coefficient.
    If --compare is enabled, also prints the standard binomial coefficient.

Dependencies:
    - numpy (optional, for performance)
"""

import sys
import argparse
from typing import List, Tuple, Optional

from wrong_binomial import WrongBinomialCalculator
from standard_binomial import StandardBinomialCalculator


class Main:
    """Main class for CLI interface and program orchestration."""

    def __init__(self) -> None:
        """Initializes the Main class with default attributes."""
        self.wrong_calc: Optional[WrongBinomialCalculator] = None
        self.std_calc: Optional[StandardBinomialCalculator] = None

    def parse_input(self, file_handle) -> Tuple[int, List[int], List[int]]:
        """Parses input from a file handle.

        Args:
            file_handle: An open file-like object to read input from.

        Returns:
            Tuple containing:
                - Q (int): Number of queries.
                - n_list (List[int]): List of n values.
                - k_list (List[int]): List of k values.
        """
        lines = []
        for line in file_handle:
            line = line.strip()
            if line:
                lines.append(line)
        if not lines:
            raise ValueError("No input provided.")

        Q = int(lines[0])
        n_list: List[int] = []
        k_list: List[int] = []
        for i in range(1, Q + 1):
            n_str, k_str = lines[i].split()
            n_list.append(int(n_str))
            k_list.append(int(k_str))
        return Q, n_list, k_list

    def print_results(
        self,
        results: List[int],
        std_results: Optional[List[int]] = None,
        compare: bool = False
    ) -> None:
        """Prints results to stdout.

        Args:
            results (List[int]): List of wrong binomial coefficients.
            std_results (Optional[List[int]]): List of standard binomial coefficients.
            compare (bool): Whether to print both results.
        """
        for i in range(len(results)):
            if compare and std_results is not None:
                print(f"{results[i]} {std_results[i]}")
            else:
                print(f"{results[i]}")

    def run(self) -> None:
        """Runs the main program: parses args, processes queries, prints results."""
        parser = argparse.ArgumentParser(
            description="Compute wrong and standard binomial coefficients."
        )
        parser.add_argument(
            "--input",
            type=str,
            default=None,
            help="Input file path (default: stdin)."
        )
        parser.add_argument(
            "--compare",
            action="store_true",
            help="Also compute and print standard binomial coefficients."
        )
        args = parser.parse_args()

        # Read input
        if args.input is not None:
            with open(args.input, "r", encoding="utf-8") as f:
                Q, n_list, k_list = self.parse_input(f)
        else:
            Q, n_list, k_list = self.parse_input(sys.stdin)

        # Determine max_n for precomputation
        max_n = max(n_list) if n_list else 0
        mod = 10 ** 9 + 7

        # Initialize calculators
        self.wrong_calc = WrongBinomialCalculator(max_n, mod)
        self.wrong_calc.precompute()

        if args.compare:
            self.std_calc = StandardBinomialCalculator(max_n, mod)
            self.std_calc.precompute()
        else:
            self.std_calc = None

        # Process queries
        results: List[int] = []
        std_results: List[int] = []

        for n, k in zip(n_list, k_list):
            wrong_val = self.wrong_calc.get(n, k)
            results.append(wrong_val)
            if args.compare and self.std_calc is not None:
                std_val = self.std_calc.get(n, k)
                std_results.append(std_val)

        # Print results
        if args.compare:
            self.print_results(results, std_results, compare=True)
        else:
            self.print_results(results, compare=False)


if __name__ == "__main__":
    main = Main()
    main.run()
