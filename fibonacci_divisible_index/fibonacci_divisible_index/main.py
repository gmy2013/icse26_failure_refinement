## main.py

from typing import List, Tuple
from pisano import PisanoPeriodCalculator
from fibonacci_divisible import FibonacciDivisibleIndexFinder
from utils import Utils


class InputHandler:
    """Handles reading input for the Fibonacci divisible index problem."""

    @staticmethod
    def read_input() -> List[Tuple[int, int]]:
        """Reads input from standard input.

        Expects each line to contain two integers n and k, separated by whitespace.
        Reading stops at EOF.

        Returns:
            A list of tuples, each containing (n, k) for a test case.
        """
        import sys

        test_cases: List[Tuple[int, int]] = []
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 2:
                continue  # Ignore malformed lines
            try:
                n = int(parts[0])
                k = int(parts[1])
                test_cases.append((n, k))
            except ValueError:
                continue  # Ignore lines with non-integer values
        return test_cases


class OutputHandler:
    """Handles writing output for the Fibonacci divisible index problem."""

    @staticmethod
    def write_output(results: List[int]) -> None:
        """Writes the results to standard output, one per line.

        Args:
            results: A list of integer results to output.
        """
        for res in results:
            print(res)


def main() -> None:
    """Main entry point for the Fibonacci divisible index finder program."""
    # Read input
    input_handler = InputHandler()
    test_cases = input_handler.read_input()

    # Initialize calculators
    pisano_calculator = PisanoPeriodCalculator()
    fib_div_finder = FibonacciDivisibleIndexFinder(pisano_calculator)
    results: List[int] = []

    for n, k in test_cases:
        try:
            idx = fib_div_finder.get_nth_divisible_index(n, k)
            mod_idx = Utils.modular_index(idx, 10**9 + 7)
            results.append(mod_idx)
        except ValueError as e:
            # If there is no such Fibonacci number, output -1 (or handle as needed)
            results.append(-1)

    OutputHandler.write_output(results)


if __name__ == "__main__":
    main()
