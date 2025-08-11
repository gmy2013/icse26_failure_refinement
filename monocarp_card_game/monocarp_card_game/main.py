## main.py

from typing import List, Tuple
from sys import stdin
from game import GameManager


class Main:
    """Handles the command-line interface for the card game."""

    @staticmethod
    def main() -> None:
        """Reads input, processes test cases, and prints results."""
        test_cases: List[Tuple[int, int, List[int]]] = []

        # Read number of test cases
        try:
            t_line: str = ''
            while t_line.strip() == '':
                t_line = stdin.readline()
            t: int = int(t_line.strip())
        except Exception:
            print("Invalid input for number of test cases.")
            return

        # Read each test case
        for _ in range(t):
            # Read n and k
            while True:
                nk_line: str = stdin.readline()
                if nk_line == '':
                    continue
                nk_line = nk_line.strip()
                if nk_line:
                    break
            try:
                n_str, k_str = nk_line.split()
                n: int = int(n_str)
                k: int = int(k_str)
            except Exception:
                print("Invalid input for n and k.")
                return

            # Read cards
            cards: List[int] = []
            while len(cards) < n:
                cards_line: str = stdin.readline()
                if cards_line == '':
                    continue
                cards_line = cards_line.strip()
                if not cards_line:
                    continue
                cards_split: List[str] = cards_line.split()
                cards.extend([int(card) for card in cards_split])
            test_cases.append((n, k, cards))

        # Process test cases
        manager: GameManager = GameManager()
        results: List[int] = manager.process_test_cases(test_cases)

        # Print results
        for result in results:
            print(result)


if __name__ == "__main__":
    Main.main()
