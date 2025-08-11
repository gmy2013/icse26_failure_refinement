## main.py

from collections import Counter
from typing import List, Tuple


class BeautifulArraySolver:
    """Solver for the 'Beautiful Array' problem.

    Provides methods to compute the minimum number of operations required
    to make an array palindromic (beautiful) by adding k any number of times
    to any element, after shuffling.
    """

    def __init__(self) -> None:
        """Initializes the BeautifulArraySolver."""
        pass

    def min_operations(self, n: int, k: int, arr: List[int]) -> int:
        """Computes the minimum number of operations to make the array beautiful.

        Args:
            n: The length of the array.
            k: The increment value allowed for each operation.
            arr: The list of integers representing the array.

        Returns:
            The minimum number of operations required, or -1 if impossible.
        """
        # Since shuffling is allowed, we can pair elements optimally.
        arr_sorted = sorted(arr)
        total_operations = 0

        # For each pair (i, n-i-1), make them equal by adding k any number of times.
        for i in range(n // 2):
            a = arr_sorted[i]
            b = arr_sorted[n - i - 1]
            diff = abs(a - b)
            if diff % k != 0:
                return -1  # Impossible to make them equal
            total_operations += diff // k

        return total_operations

    def process_test_cases(
        self, test_cases: List[Tuple[int, int, List[int]]]
    ) -> List[int]:
        """Processes multiple test cases.

        Args:
            test_cases: A list of tuples, each containing (n, k, arr).

        Returns:
            A list of results, one for each test case.
        """
        results: List[int] = []
        for n, k, arr in test_cases:
            result = self.min_operations(n, k, arr)
            results.append(result)
        return results


class InputHandler:
    """Handles input and output for the Beautiful Array problem."""

    def __init__(self) -> None:
        """Initializes the InputHandler."""
        pass

    def read_input(self) -> List[Tuple[int, int, List[int]]]:
        """Reads input from standard input.

        Returns:
            A list of test cases, each as a tuple (n, k, arr).
        """
        import sys

        input_lines = sys.stdin.read().splitlines()
        test_cases: List[Tuple[int, int, List[int]]] = []
        idx = 0
        t = int(input_lines[idx].strip())
        idx += 1
        for _ in range(t):
            n_k = input_lines[idx].strip().split()
            idx += 1
            n = int(n_k[0])
            k = int(n_k[1])
            arr = list(map(int, input_lines[idx].strip().split()))
            idx += 1
            test_cases.append((n, k, arr))
        return test_cases

    def write_output(self, results: List[int]) -> None:
        """Writes the results to standard output.

        Args:
            results: A list of integers, each the result for a test case.
        """
        for res in results:
            print(res)


class Main:
    """Main class to run the Beautiful Array solution."""

    @staticmethod
    def main() -> None:
        """Main entry point."""
        input_handler = InputHandler()
        test_cases = input_handler.read_input()
        solver = BeautifulArraySolver()
        results = solver.process_test_cases(test_cases)
        input_handler.write_output(results)


if __name__ == "__main__":
    Main.main()
