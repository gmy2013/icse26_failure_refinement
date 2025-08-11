## main.py

from typing import List
import sys

class ArrayPair:
    """Data structure to hold a pair of integers and its original index."""

    def __init__(self, first: int, second: int, index: int) -> None:
        self.first: int = first
        self.second: int = second
        self.index: int = index

class InversionMinimizer:
    """Implements the greedy sorting algorithm to minimize inversions."""

    def minimize_inversions(self, pairs: List[ArrayPair]) -> List[int]:
        """
        Sorts the array pairs by their first element, then by second element,
        and concatenates them to minimize inversions.

        Args:
            pairs: List of ArrayPair objects.

        Returns:
            List[int]: Concatenated array after minimizing inversions.
        """
        # Sort by first, then by second element
        sorted_pairs = sorted(pairs, key=lambda p: (p.first, p.second))
        result: List[int] = []
        for pair in sorted_pairs:
            result.append(pair.first)
            result.append(pair.second)
        return result

class TestCaseHandler:
    """Handles input parsing, test case processing, and output."""

    def read_input(self) -> List[List[ArrayPair]]:
        """
        Reads input from stdin and parses it into test cases.

        Returns:
            List[List[ArrayPair]]: List of test cases, each a list of ArrayPair.
        """
        input_lines = sys.stdin.read().splitlines()
        test_cases: List[List[ArrayPair]] = []
        line_idx: int = 0

        if not input_lines:
            return test_cases

        t = int(input_lines[line_idx].strip())
        line_idx += 1

        for _ in range(t):
            n = int(input_lines[line_idx].strip())
            line_idx += 1
            pairs: List[ArrayPair] = []
            for i in range(n):
                first_str, second_str = input_lines[line_idx].strip().split()
                first = int(first_str)
                second = int(second_str)
                pairs.append(ArrayPair(first, second, i))
                line_idx += 1
            test_cases.append(pairs)
        return test_cases

    def process_test_cases(self, test_cases: List[List[ArrayPair]]) -> List[List[int]]:
        """
        Processes all test cases using InversionMinimizer.

        Args:
            test_cases: List of test cases, each a list of ArrayPair.

        Returns:
            List[List[int]]: List of results, each a concatenated array.
        """
        minimizer = InversionMinimizer()
        results: List[List[int]] = []
        for pairs in test_cases:
            result = minimizer.minimize_inversions(pairs)
            results.append(result)
        return results

    def output_results(self, results: List[List[int]]) -> None:
        """
        Outputs the results to stdout.

        Args:
            results: List of results, each a concatenated array.
        """
        for result in results:
            print(' '.join(map(str, result)))

class Main:
    """Entry point for the program."""

    def main(self) -> None:
        """
        Main function to orchestrate reading input, processing, and output.
        """
        handler = TestCaseHandler()
        test_cases = handler.read_input()
        results = handler.process_test_cases(test_cases)
        handler.output_results(results)

if __name__ == "__main__":
    Main().main()
