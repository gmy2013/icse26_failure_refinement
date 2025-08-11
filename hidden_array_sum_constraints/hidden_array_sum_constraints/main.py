## main.py

"""Command-line interface for the hidden array solver.

This module provides the entry point for the hidden array replacement problem.
It parses command-line arguments, validates input, invokes the solver, and
prints the result.

Usage:
    python main.py --n 5 --m 2 --b 1 3 2 0 1 --s "1?0?1"

Dependencies:
    - argparse
    - input_validator.py
    - hidden_array_solver.py
"""

import argparse
import sys
from typing import List

from input_validator import InputValidator
from hidden_array_solver import HiddenArraySolver


def parse_args() -> argparse.Namespace:
    """Parses command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Hidden Array Replacement Solver"
    )
    parser.add_argument(
        "--n",
        type=int,
        required=True,
        help="Length of the array and string (positive integer).",
    )
    parser.add_argument(
        "--m",
        type=int,
        required=True,
        help="Maximum absolute value for elements in array a (non-negative integer).",
    )
    parser.add_argument(
        "--b",
        type=int,
        nargs="+",
        required=True,
        help="Space-separated list of prefix/suffix sum constraints (length n).",
    )
    parser.add_argument(
        "--s",
        type=str,
        required=True,
        help="String of digits and '?' (length n).",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point for the hidden array solver CLI."""
    args = parse_args()

    n: int = args.n
    m: int = args.m
    b: List[int] = args.b
    s: str = args.s

    # Input validation
    validator = InputValidator()
    try:
        validator.validate(n, m, b, s)
    except ValueError as e:
        print(f"Input validation error: {e}", file=sys.stderr)
        sys.exit(1)

    # Solve
    solver = HiddenArraySolver(n, m, b, s)
    result: int = solver.count_valid_replacements()
    print(result)


if __name__ == "__main__":
    main()
