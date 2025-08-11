## main.py

from typing import List
from game import CakeGame


class Main:
    """Main class to handle CLI input/output and run the cake game simulation."""

    @staticmethod
    def main() -> None:
        """Reads input, processes each test case, and prints results."""
        import sys

        def read_ints() -> List[int]:
            """Reads a line from stdin and returns a list of integers."""
            return list(map(int, sys.stdin.readline().split()))

        # Read number of test cases
        try:
            t_line = ''
            while t_line.strip() == '':
                t_line = sys.stdin.readline()
            t = int(t_line.strip())
        except Exception:
            print("Invalid input for number of test cases.")
            return

        results: List[int] = []

        for _ in range(t):
            # Read number of cakes
            n_line = ''
            while n_line.strip() == '':
                n_line = sys.stdin.readline()
            try:
                n = int(n_line.strip())
            except Exception:
                print("Invalid input for number of cakes.")
                return

            # Read cake sizes
            cakes_line = ''
            while cakes_line.strip() == '':
                cakes_line = sys.stdin.readline()
            try:
                cakes = list(map(int, cakes_line.strip().split()))
                if len(cakes) != n:
                    print("Number of cake sizes does not match n.")
                    return
            except Exception:
                print("Invalid input for cake sizes.")
                return

            # Instantiate CakeGame and compute result
            game = CakeGame(cakes)
            alice_max_cakes = game.compute_alice_max_cakes()
            results.append(alice_max_cakes)

        # Print results
        for res in results:
            print(res)


if __name__ == "__main__":
    Main.main()
