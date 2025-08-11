## main.py

import sys
from typing import List, Tuple
import numpy as np

from grundy import GrundyCalculator


class GameEngine:
    """Game engine to determine the winner of the GCD-restricted Nim game."""

    def __init__(self, grundy_calculator: 'GrundyCalculator') -> None:
        """
        Initializes the GameEngine with a GrundyCalculator.

        Args:
            grundy_calculator (GrundyCalculator): The GrundyCalculator instance to use.
        """
        self.grundy_calculator: GrundyCalculator = grundy_calculator

    def determine_winner(self, piles: List[int]) -> str:
        """
        Determines the winner for a given list of piles.

        Args:
            piles (List[int]): List of pile sizes.

        Returns:
            str: "Alice" if Alice wins, "Bob" otherwise.
        """
        xor_sum: int = 0
        for pile in piles:
            xor_sum ^= self.grundy_calculator.get_grundy(pile)
        return "Alice" if xor_sum != 0 else "Bob"


class Main:
    """Main class to handle CLI, input parsing, and output."""

    def __init__(self) -> None:
        """
        Initializes the Main class, sets up the GrundyCalculator and GameEngine.
        """
        # Set the maximum pile size for precomputation.
        self._max_pile_size: int = 10_000_000
        self.game_engine: GameEngine = GameEngine(
            GrundyCalculator(self._max_pile_size)
        )

    def parse_input(self) -> Tuple[int, List[List[int]]]:
        """
        Parses input from stdin.

        Returns:
            Tuple[int, List[List[int]]]: Number of test cases and list of pile lists.
        """
        input_lines = sys.stdin.read().splitlines()
        idx: int = 0
        t: int = int(input_lines[idx])
        idx += 1
        test_cases: List[List[int]] = []
        for _ in range(t):
            n: int = int(input_lines[idx])
            idx += 1
            piles: List[int] = list(map(int, input_lines[idx].split()))
            idx += 1
            test_cases.append(piles)
        return t, test_cases

    def print_results(self, results: List[str]) -> None:
        """
        Prints the results for each test case.

        Args:
            results (List[str]): List of winner names ("Alice" or "Bob").
        """
        for result in results:
            print(result)

    def main(self) -> None:
        """
        Main entry point: parses input, processes test cases, and prints results.
        """
        t, test_cases = self.parse_input()
        results: List[str] = []
        for piles in test_cases:
            winner = self.game_engine.determine_winner(piles)
            results.append(winner)
        self.print_results(results)


if __name__ == "__main__":
    Main().main()
