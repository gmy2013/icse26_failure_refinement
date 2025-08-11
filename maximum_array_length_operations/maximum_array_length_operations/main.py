## main.py

from typing import List, Tuple


class ArrayLengthMaximizer:
    """Class to maximize the length of an array by simulating allowed operations."""

    def process_test_case(self, n: int, a: List[int]) -> int:
        """Process a single test case to compute the maximum possible array length.

        Args:
            n: The initial length of the array.
            a: The initial array as a list of integers.

        Returns:
            The maximum possible length of the array after performing allowed operations.
        """
        current_length: int = n
        # We process from right to left, greedily applying the operation at the rightmost valid position.
        i: int = n
        while i >= 2:
            # The operation is allowed at position i if a[i-1] == current_length + 1 - i
            if a[i - 1] == current_length + 1 - i:
                # Simulate appending (i-1) zeros
                current_length += (i - 1)
            i -= 1
        return current_length

    def process_all_cases(self, test_cases: List[Tuple[int, List[int]]]) -> List[int]:
        """Process all test cases.

        Args:
            test_cases: A list of tuples, each containing (n, a) for a test case.

        Returns:
            A list of results, one for each test case.
        """
        results: List[int] = []
        for n, a in test_cases:
            result = self.process_test_case(n, a)
            results.append(result)
        return results


class CLI:
    """Command-line interface for reading input, processing, and printing output."""

    @staticmethod
    def read_input() -> List[Tuple[int, List[int]]]:
        """Reads input from standard input.

        Returns:
            A list of test cases, each as a tuple (n, a).
        """
        import sys

        test_cases: List[Tuple[int, List[int]]] = []
        input_lines = sys.stdin.read().splitlines()
        line_idx: int = 0

        if line_idx >= len(input_lines):
            return test_cases

        t: int = int(input_lines[line_idx].strip())
        line_idx += 1

        for _ in range(t):
            if line_idx >= len(input_lines):
                break
            n: int = int(input_lines[line_idx].strip())
            line_idx += 1
            if line_idx >= len(input_lines):
                break
            a: List[int] = list(map(int, input_lines[line_idx].strip().split()))
            line_idx += 1
            test_cases.append((n, a))
        return test_cases

    @staticmethod
    def print_output(results: List[int]) -> None:
        """Prints the results to standard output.

        Args:
            results: A list of integers to print, one per line.
        """
        for res in results:
            print(res)

    @staticmethod
    def main() -> None:
        """Main entry point for the program."""
        test_cases = CLI.read_input()
        maximizer = ArrayLengthMaximizer()
        results = maximizer.process_all_cases(test_cases)
        CLI.print_output(results)


if __name__ == "__main__":
    CLI.main()
