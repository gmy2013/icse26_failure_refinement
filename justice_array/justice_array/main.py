## main.py
import sys
from typing import List, Tuple


class InputParser:
    """Parses input from stdin for the JusticeArraySolver."""

    @staticmethod
    def parse_input() -> List[Tuple[int, List[int]]]:
        """Reads input from stdin and returns a list of test cases.

        Returns:
            List[Tuple[int, List[int]]]: Each tuple contains the number of elements and the array.
        """
        input_lines = sys.stdin.read().splitlines()
        test_cases: List[Tuple[int, List[int]]] = []
        idx: int = 0
        t: int = int(input_lines[idx])
        idx += 1
        for _ in range(t):
            n: int = int(input_lines[idx])
            idx += 1
            a: List[int] = list(map(int, input_lines[idx].split()))
            idx += 1
            test_cases.append((n, a))
        return test_cases


class JusticeArraySolver:
    """Solves the minimum acts of justice required to make arrays non-decreasing."""

    def solve(self, test_cases: List[Tuple[int, List[int]]]) -> List[int]:
        """Solves all test cases.

        Args:
            test_cases (List[Tuple[int, List[int]]]): List of test cases.

        Returns:
            List[int]: List of results for each test case.
        """
        results: List[int] = []
        for _, a in test_cases:
            result = self._min_acts_for_case(a)
            results.append(result)
        return results

    def _min_acts_for_case(self, a: List[int]) -> int:
        """Computes the minimum number of acts of justice for a single array.

        Args:
            a (List[int]): The input array.

        Returns:
            int: The minimum number of acts, or -1 if impossible.
        """
        n: int = len(a)
        acts: int = 0
        # We process from right to left, so that after fixing a[i+1], a[i] can be compared to the new value.
        b: List[int] = a[:]
        for i in range(n - 2, -1, -1):
            if b[i] <= b[i + 1]:
                continue
            # Try to square b[i+1] until it is >= b[i], or until it stops changing (0 or 1)
            current: int = b[i + 1]
            count: int = 0
            # If current is 0 or 1, squaring does not help
            while current < b[i] and current > 1:
                current = current * current
                count += 1
                # To avoid infinite loop, if current exceeds a reasonable bound, break
                # But in Python, int is unbounded, so we only break if current >= b[i]
            if current >= b[i]:
                b[i + 1] = current
                acts += count
                continue
            # If b[i+1] cannot be made >= b[i], try to square b[i] until it is <= b[i+1]
            current = b[i]
            count = 0
            while current > b[i + 1] and current > 1:
                current = current * current
                count += 1
            if current <= b[i + 1]:
                b[i] = current
                acts += count
                continue
            # If neither is possible, return -1
            return -1
        return acts


class OutputFormatter:
    """Formats and prints the output."""

    @staticmethod
    def format_output(results: List[int]) -> None:
        """Prints the results, one per line.

        Args:
            results (List[int]): List of results to print.
        """
        for res in results:
            print(res)


def main() -> None:
    """Main function to orchestrate input, solving, and output."""
    parser = InputParser()
    test_cases = parser.parse_input()
    solver = JusticeArraySolver()
    results = solver.solve(test_cases)
    OutputFormatter.format_output(results)


if __name__ == "__main__":
    main()
