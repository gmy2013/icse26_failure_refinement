## main.py

import sys
from typing import List, Tuple

from game import Game

class Main:
    """Main class to handle input/output and orchestrate the game."""

    @staticmethod
    def parse_input() -> List[Tuple[int, int, List[int]]]:
        """
        Parse input from stdin.

        Returns:
            List of tuples, each containing (n, k, values) for a test case.
        """
        input_lines = sys.stdin.read().splitlines()
        test_cases = []
        idx = 0
        t = int(input_lines[idx].strip())
        idx += 1
        for _ in range(t):
            n_k = input_lines[idx].strip().split()
            n = int(n_k[0])
            k = int(n_k[1])
            idx += 1
            values = list(map(int, input_lines[idx].strip().split()))
            idx += 1
            test_cases.append((n, k, values))
        return test_cases

    @staticmethod
    def output_results(results: List[Tuple[int, int]]) -> None:
        """
        Output results to stdout.

        Args:
            results: List of (alice_score, bob_score) tuples.
        """
        for alice_score, bob_score in results:
            print(f"{alice_score} {bob_score}")

    @staticmethod
    def main() -> None:
        """
        Main entry point for the program.
        """
        test_cases = Main.parse_input()
        results: List[Tuple[int, int]] = []
        for n, k, values in test_cases:
            game = Game(n, k, values)
            alice_score, bob_score = game.expected_scores()
            results.append((alice_score, bob_score))
        Main.output_results(results)


if __name__ == "__main__":
    Main.main()
