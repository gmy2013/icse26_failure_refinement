## main.py

from typing import Tuple
from berland_card_game import BerlandCardGame
from combinatorics import Combinatorics

class Main:
    """Main class to handle input parsing, game setup, and output."""

    @staticmethod
    def parse_input() -> Tuple[int, int]:
        """Parses input for the Berland card game.

        Returns:
            Tuple[int, int]: A tuple containing n (number of distinct card values) and m (number of cards per player).
        """
        try:
            # Read two integers from input
            input_line = input("Enter n (number of distinct card values) and m (number of cards per player), separated by space: ")
            n_str, m_str = input_line.strip().split()
            n = int(n_str)
            m = int(m_str)
            return n, m
        except Exception as e:
            print(f"Invalid input format: {e}")
            raise

    @staticmethod
    def main() -> None:
        """Main execution function."""
        # Parse input
        n, m = Main.parse_input()

        # Set up combinatorics with a safe upper bound for factorials
        max_n = max(2 * n, 2 * m, 1000)
        mod = 10 ** 9 + 7
        combinatorics = Combinatorics(max_n=max_n, mod=mod)

        # Set up the game
        game = BerlandCardGame(n=n, m=m, combinatorics=combinatorics)

        # Compute and print the result
        result = game.count_valid_distributions()
        print(result)


if __name__ == "__main__":
    Main.main()
