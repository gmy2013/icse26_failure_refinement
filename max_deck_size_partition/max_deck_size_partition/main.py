## main.py


from typing import List, Tuple
from max_deck import MaxDeckSolver


class InputParser:
    """Handles input parsing for the deck partitioning problem."""

    @staticmethod
    def parse_input() -> List[Tuple[int, int, List[int]]]:
        """Parses input from standard input.

        Returns:
            A list of test cases, each as a tuple (n, k, a),
            where n is the number of card types,
            k is the number of cards that can be purchased,
            and a is the list of counts of each card type.
        """
        import sys

        test_cases: List[Tuple[int, int, List[int]]] = []
        input_lines = sys.stdin.read().splitlines()
        line_idx: int = 0

        if not input_lines:
            return test_cases

        t: int = int(input_lines[line_idx].strip())
        line_idx += 1

        for _ in range(t):
            if line_idx >= len(input_lines):
                break
            n_k = input_lines[line_idx].strip().split()
            line_idx += 1
            if len(n_k) != 2:
                continue
            n, k = map(int, n_k)
            if line_idx >= len(input_lines):
                break
            a = list(map(int, input_lines[line_idx].strip().split()))
            line_idx += 1
            if len(a) != n:
                continue
            test_cases.append((n, k, a))
        return test_cases


class OutputFormatter:
    """Handles formatting and outputting the results."""

    @staticmethod
    def format_output(results: List[int]) -> None:
        """Prints the results, one per line.

        Args:
            results: List of integers to print.
        """
        for res in results:
            print(res)


class Main:
    """Main class to orchestrate the program."""

    @staticmethod
    def main() -> None:
        """Main entry point for the program."""
        parser = InputParser()
        solver = MaxDeckSolver()
        formatter = OutputFormatter()

        test_cases = parser.parse_input()
        results = solver.solve(test_cases)
        formatter.format_output(results)


if __name__ == "__main__":
    Main.main()
