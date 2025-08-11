## main.py

from typing import List
from casino import Game, CasinoMaxExpectedValue


class CLI:
    """Command-line interface for the CasinoMaxExpectedValue program."""

    def run(self) -> None:
        """Runs the CLI: parses input, computes result, and displays output."""
        games: List[Game] = self.parse_input()
        solver = CasinoMaxExpectedValue(games)
        max_ev: float = solver.max_expected_value()
        self.display_output(max_ev)

    def parse_input(self) -> List[Game]:
        """Parses user input from stdin to create a list of Game instances.

        Input format:
            n
            p1 w1
            p2 w2
            ...
            pn wn

        Returns:
            List[Game]: List of parsed Game instances.
        """
        try:
            n_line = input().strip()
            while n_line == '':
                n_line = input().strip()
            n: int = int(n_line)
        except Exception:
            print("Invalid input: expected number of games.")
            exit(1)

        games: List[Game] = []
        for i in range(n):
            while True:
                try:
                    line = input().strip()
                    if line == '':
                        continue
                    p_str, w_str = line.split()
                    p = int(p_str)
                    w = int(w_str)
                    if not (1 <= p <= 100):
                        print(f"Invalid probability at line {i+2}: {p}")
                        exit(1)
                    games.append(Game(p, w))
                    break
                except ValueError:
                    print(f"Invalid input at line {i+2}: expected two integers.")
                except Exception:
                    print(f"Unexpected error at line {i+2}.")
                    exit(1)
        return games

    def display_output(self, value: float) -> None:
        """Displays the output (maximum expected value) to stdout.

        Args:
            value (float): The maximum expected value to display.
        """
        # Output with 10 decimal places, as per typical precision requirements
        print(f"{value:.10f}")


if __name__ == "__main__":
    cli = CLI()
    cli.run()
