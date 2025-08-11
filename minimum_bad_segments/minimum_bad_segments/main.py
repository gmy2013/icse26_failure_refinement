## main.py

from typing import List, Tuple, Dict
import sys
from sympy import factorint


class BadSegmentSolver:
    """Solver for partitioning array into minimum number of 'bad' segments."""

    def __init__(self) -> None:
        """Initializes the BadSegmentSolver."""
        pass

    def min_bad_segments(self, n: int, x: int, a: List[int]) -> int:
        """Returns the minimum number of bad segments for the given array.

        Args:
            n: The number of elements in the array.
            x: The target product to check divisibility.
            a: The list of integers representing the array.

        Returns:
            The minimum number of bad segments.
        """
        if x == 1:
            # Every segment is good, so only one segment is needed.
            return 1

        x_factors = self._prime_factors(x)
        num_segments = 0
        current_exponents = {p: 0 for p in x_factors}
        segment_start = 0

        for i, value in enumerate(a):
            value_exponents = self._get_exponents(value, x_factors)
            for p in x_factors:
                current_exponents[p] += value_exponents[p]

            # Check if current segment can form x as a product of some subset
            if self._can_form_x(current_exponents, x_factors):
                # Start a new segment
                num_segments += 1
                current_exponents = {p: 0 for p in x_factors}
                segment_start = i + 1

        # If there are leftover elements that cannot form x, they form a bad segment
        if segment_start < n:
            num_segments += 1

        return num_segments

    def _prime_factors(self, num: int) -> Dict[int, int]:
        """Returns the prime factorization of num as a dictionary.

        Args:
            num: The integer to factorize.

        Returns:
            A dictionary mapping prime factors to their exponents.
        """
        return factorint(num)

    def _get_exponents(self, a: int, x_factors: Dict[int, int]) -> Dict[int, int]:
        """Returns the exponents of x's prime factors in a.

        Args:
            a: The integer to analyze.
            x_factors: The prime factors of x.

        Returns:
            A dictionary mapping each prime in x_factors to its exponent in a.
        """
        exponents = {}
        for p in x_factors:
            count = 0
            temp = a
            while temp % p == 0 and temp > 0:
                temp //= p
                count += 1
            exponents[p] = count
        return exponents

    def _can_form_x(self, current_exponents: Dict[int, int], x_factors: Dict[int, int]) -> bool:
        """Checks if the current exponents can form x.

        Args:
            current_exponents: The exponents of x's prime factors in the current segment.
            x_factors: The required exponents for x.

        Returns:
            True if all required exponents are met or exceeded, False otherwise.
        """
        for p in x_factors:
            if current_exponents[p] < x_factors[p]:
                return False
        return True


class MainApp:
    """Main application class for CLI and orchestration."""

    def __init__(self) -> None:
        """Initializes the MainApp."""
        self.solver = BadSegmentSolver()

    def run(self) -> None:
        """Runs the main application loop."""
        test_cases = self._parse_input()
        results = []
        for n, x, a in test_cases:
            result = self.solver.min_bad_segments(n, x, a)
            results.append(result)
        self._print_output(results)

    def _parse_input(self) -> List[Tuple[int, int, List[int]]]:
        """Parses input from stdin.

        Returns:
            A list of tuples, each containing (n, x, a) for a test case.
        """
        input_lines = sys.stdin.read().splitlines()
        test_cases = []
        idx = 0
        if not input_lines:
            return test_cases
        t = int(input_lines[idx].strip())
        idx += 1
        for _ in range(t):
            n_x = input_lines[idx].strip().split()
            idx += 1
            n = int(n_x[0])
            x = int(n_x[1])
            a = list(map(int, input_lines[idx].strip().split()))
            idx += 1
            test_cases.append((n, x, a))
        return test_cases

    def _print_output(self, results: List[int]) -> None:
        """Prints the results to stdout.

        Args:
            results: The list of results to print.
        """
        for res in results:
            print(res)


if __name__ == "__main__":
    app = MainApp()
    app.run()
