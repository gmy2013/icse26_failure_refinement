## main.py

from collections import Counter
from typing import Dict


class StringReorderer:
    """Class to reorder a string to maximize the number of good pairs.

    Good pairs are maximized by grouping identical characters together.
    """

    @staticmethod
    def reorder_to_maximize_good_pairs(s: str) -> str:
        """Reorders the input string to maximize the number of good pairs.

        Args:
            s (str): The input string.

        Returns:
            str: The reordered string with identical characters grouped together.
        """
        char_count: Dict[str, int] = Counter(s)
        reordered_chars = []
        for char in sorted(char_count.keys()):
            reordered_chars.append(char * char_count[char])
        return ''.join(reordered_chars)


class Main:
    """Main class to handle input/output and process test cases."""

    @staticmethod
    def main() -> None:
        """Reads input, processes each test case, and prints the result."""
        import sys

        input_lines = sys.stdin.read().splitlines()
        if not input_lines:
            return

        t = 0
        try:
            t = int(input_lines[0])
        except (IndexError, ValueError):
            print("Invalid input: first line must be the number of test cases.")
            return

        line_idx = 1
        for _ in range(t):
            if line_idx >= len(input_lines):
                print("Invalid input: missing test case data.")
                return
            try:
                n = int(input_lines[line_idx])
                line_idx += 1
                if line_idx >= len(input_lines):
                    print("Invalid input: missing string for test case.")
                    return
                s = input_lines[line_idx]
                line_idx += 1
            except (IndexError, ValueError):
                print("Invalid input: test case format error.")
                return

            if len(s) != n:
                print(f"Invalid input: string length does not match n (expected {n}, got {len(s)}).")
                return

            result = StringReorderer.reorder_to_maximize_good_pairs(s)
            print(result)


if __name__ == "__main__":
    Main.main()
