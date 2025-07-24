## main.py

import sys
from typing import List

from connect_the_dots_game import ConnectTheDotsGame

class Main:
    """Main class to handle input/output and orchestrate the Connect The Dots game."""

    @staticmethod
    def main() -> None:
        """Main entry point for the program. Reads input, processes test cases, and outputs results."""
        input_lines = sys.stdin.read().splitlines()
        line_idx: int = 0
        t: int = int(input_lines[line_idx].strip())
        line_idx += 1
        results: List[int] = []

        for _ in range(t):
            # Read n (number of points) and m (number of operations)
            n_m = input_lines[line_idx].strip().split()
            n: int = int(n_m[0])
            m: int = int(n_m[1])
            line_idx += 1

            game = ConnectTheDotsGame(n, m)

            for _ in range(m):
                a_d_k = input_lines[line_idx].strip().split()
                a: int = int(a_d_k[0])
                d: int = int(a_d_k[1])
                k: int = int(a_d_k[2])
                line_idx += 1

                game.process_operation(a, d, k)

            components: int = game.get_connected_components()
            results.append(components)

        for res in results:
            print(res)

if __name__ == "__main__":
    Main.main()
