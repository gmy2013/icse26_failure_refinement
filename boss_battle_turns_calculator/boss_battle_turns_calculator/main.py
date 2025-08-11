## main.py

"""Main module for the boss battle turn calculator CLI.

This module provides the Main class, which orchestrates the input parsing,
core calculation, and output formatting for batch boss battle test cases.

Classes:
    Main: Entry point for the CLI application.
"""

from typing import List, Tuple
from battle_calculator import BattleCalculator
from input_parser import InputParser
from output_formatter import OutputFormatter


class Main:
    """Main entry point for the boss battle calculator CLI.

    Methods:
        run(): Runs the CLI application.
    """

    def __init__(self) -> None:
        """Initializes the Main class and its dependencies."""
        self.input_parser: InputParser = InputParser()
        self.battle_calculator: BattleCalculator = BattleCalculator()
        self.output_formatter: OutputFormatter = OutputFormatter()

    def run(self) -> None:
        """Runs the CLI application for batch boss battle calculation.

        Reads input, processes each test case, and prints the results.
        """
        # Parse input
        t: int
        test_cases: List[Tuple[int, int, List[int], List[int]]]
        t, test_cases = self.input_parser.parse_input()

        results: List[int] = []

        for idx in range(t):
            n: int
            h: int
            damages: List[int]
            cooldowns: List[int]
            n, h, damages, cooldowns = test_cases[idx]
            # Calculate minimum turns to defeat the boss
            min_turns: int = self.battle_calculator.min_turns_to_defeat(
                h, damages, cooldowns
            )
            results.append(min_turns)

        # Format and print output
        output_str: str = self.output_formatter.format_output(results)
        print(output_str)


if __name__ == "__main__":
    main_app: Main = Main()
    main_app.run()
