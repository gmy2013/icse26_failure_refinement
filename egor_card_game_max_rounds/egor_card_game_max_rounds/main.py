## main.py

import sys
from typing import List, Tuple, Dict, Any

from egor_game import EgorGame


class InputHandler:
    """Handles parsing and validation of input for the Egor card game CLI."""

    @staticmethod
    def parse_input() -> Tuple[List[Dict[str, Any]], bool]:
        """Parses input from stdin.

        Returns:
            A tuple containing:
                - A list of test case dictionaries, each with keys: n, l, r, cards.
                - A boolean indicating whether verbose mode is enabled.
        """
        test_cases: List[Dict[str, Any]] = []
        verbose: bool = False

        lines: List[str] = []
        try:
            for line in sys.stdin:
                line = line.strip()
                if line == "":
                    continue
                lines.append(line)
        except Exception as e:
            print(f"Error reading input: {e}", file=sys.stderr)
            sys.exit(1)

        if not lines:
            print("No input provided.", file=sys.stderr)
            sys.exit(1)

        # Check for verbose flag in the first line
        if lines[0].lower() == "--verbose":
            verbose = True
            lines = lines[1:]

        if not lines:
            print("No test cases provided.", file=sys.stderr)
            sys.exit(1)

        try:
            t = int(lines[0])
        except ValueError:
            print("First line must be the number of test cases.", file=sys.stderr)
            sys.exit(1)

        idx = 1
        for case_num in range(t):
            if idx + 1 >= len(lines):
                print(f"Insufficient input for test case {case_num + 1}.", file=sys.stderr)
                sys.exit(1)
            try:
                n_l_r = lines[idx].split()
                n, l, r = map(int, n_l_r)
                cards = list(map(int, lines[idx + 1].split()))
            except Exception:
                print(f"Invalid input format in test case {case_num + 1}.", file=sys.stderr)
                sys.exit(1)
            test_cases.append({
                "n": n,
                "l": l,
                "r": r,
                "cards": cards
            })
            idx += 2

        return test_cases, verbose

    @staticmethod
    def validate_test_case(test_case: Dict[str, Any]) -> bool:
        """Validates a single test case.

        Args:
            test_case: Dictionary with keys n, l, r, cards.

        Returns:
            True if the test case is valid, False otherwise.
        """
        n = test_case.get("n")
        l = test_case.get("l")
        r = test_case.get("r")
        cards = test_case.get("cards")

        if not isinstance(n, int) or not isinstance(l, int) or not isinstance(r, int):
            return False
        if not isinstance(cards, list) or len(cards) != n:
            return False
        if l > r:
            return False
        if any(not isinstance(card, int) for card in cards):
            return False
        return True


class OutputHandler:
    """Handles output and error reporting for the Egor card game CLI."""

    @staticmethod
    def print_results(results: List[int]) -> None:
        """Prints the results for all test cases.

        Args:
            results: List of integers representing the number of rounds won per test case.
        """
        for res in results:
            print(res)

    @staticmethod
    def print_error(message: str) -> None:
        """Prints an error message to stderr.

        Args:
            message: The error message to print.
        """
        print(f"Error: {message}", file=sys.stderr)


class Main:
    """Main class to run the Egor card game CLI."""

    @staticmethod
    def main() -> None:
        """Entry point for the CLI tool."""
        input_handler = InputHandler()
        output_handler = OutputHandler()

        test_cases, verbose = input_handler.parse_input()
        results: List[int] = []

        for idx, test_case in enumerate(test_cases):
            if not input_handler.validate_test_case(test_case):
                output_handler.print_error(
                    f"Invalid test case at index {idx + 1}: {test_case}"
                )
                results.append(0)
                continue
            n = test_case["n"]
            l = test_case["l"]
            r = test_case["r"]
            cards = test_case["cards"]
            rounds = EgorGame.max_winning_rounds(n, l, r, cards, verbose)
            results.append(rounds)

        output_handler.print_results(results)


if __name__ == "__main__":
    Main.main()
