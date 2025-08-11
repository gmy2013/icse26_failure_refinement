## main.py

import sys
from typing import List

from game import BettingGame


class BettingGameCLI:
    """Command-line interface for the BettingGame."""

    def __init__(self) -> None:
        """Initialize the CLI."""
        self.game = BettingGame()

    def run(self) -> None:
        """
        Run the CLI: read input, process test cases, and print output.

        Input format:
            t
            n1
            k_1_1 k_1_2 ... k_1_n1
            n2
            k_2_1 k_2_2 ... k_2_n2
            ...

        Output:
            For each test case, print -1 if impossible, else print n integers (the bets).
        """
        input_lines = sys.stdin.read().splitlines()
        ptr = 0

        if ptr < len(input_lines):
            try:
                t = int(input_lines[ptr].strip())
            except ValueError:
                print("Invalid input for number of test cases.")
                return
            ptr += 1
        else:
            print("No input provided.")
            return

        for _ in range(t):
            if ptr >= len(input_lines):
                print("Insufficient input for test cases.")
                break
            try:
                n = int(input_lines[ptr].strip())
            except ValueError:
                print("Invalid input for number of outcomes.")
                return
            ptr += 1

            if ptr >= len(input_lines):
                print("Insufficient input for multipliers.")
                break
            try:
                multipliers = list(map(int, input_lines[ptr].strip().split()))
            except ValueError:
                print("Invalid input for multipliers.")
                return
            if len(multipliers) != n:
                print("Mismatch between number of outcomes and multipliers.")
                return
            ptr += 1

            result = self.game.find_bet_distribution(n, multipliers)
            if result == -1:
                print(-1)
            else:
                print(' '.join(str(x) for x in result))


if __name__ == "__main__":
    cli = BettingGameCLI()
    cli.run()
