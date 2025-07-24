## main.py

import sys
from typing import List, Tuple
from game import Game

class Main:
    """Handles input/output and test case management for the chip-cutting game."""

    @staticmethod
    def main() -> None:
        """
        Reads input, processes all test cases, and outputs results.
        """
        input_lines: List[str] = sys.stdin.read().splitlines()
        line_idx: int = 0
        results: List[Tuple[int, int]] = []

        # Read number of test cases
        t: int = 0
        while line_idx < len(input_lines):
            line = input_lines[line_idx].strip()
            if line == '':
                line_idx += 1
                continue
            t = int(line)
            line_idx += 1
            break

        for _ in range(t):
            # Read a, b, n, m
            while line_idx < len(input_lines) and input_lines[line_idx].strip() == '':
                line_idx += 1
            if line_idx >= len(input_lines):
                break
            a_b_n_m = input_lines[line_idx].strip().split()
            while len(a_b_n_m) < 4:
                line_idx += 1
                a_b_n_m += input_lines[line_idx].strip().split()
            a, b, n, m = map(int, a_b_n_m)
            line_idx += 1

            # Read n lines of chips
            chips: List[Tuple[int, int]] = []
            chips_read: int = 0
            while chips_read < n and line_idx < len(input_lines):
                line = input_lines[line_idx].strip()
                if line == '':
                    line_idx += 1
                    continue
                chip_pos = list(map(int, line.split()))
                while len(chip_pos) < 2:
                    line_idx += 1
                    chip_pos += list(map(int, input_lines[line_idx].strip().split()))
                chips.append((chip_pos[0], chip_pos[1]))
                chips_read += 1
                line_idx += 1

            # Read m lines of moves
            moves: List[Tuple[str, int]] = []
            moves_read: int = 0
            while moves_read < m and line_idx < len(input_lines):
                line = input_lines[line_idx].strip()
                if line == '':
                    line_idx += 1
                    continue
                move_parts = line.split()
                while len(move_parts) < 2:
                    line_idx += 1
                    move_parts += input_lines[line_idx].strip().split()
                direction = move_parts[0]
                index = int(move_parts[1])
                moves.append((direction, index))
                moves_read += 1
                line_idx += 1

            # Instantiate Game and process moves
            game = Game(a, b, n, m, chips, moves)
            alice_score, bob_score = game.process_moves()
            results.append((alice_score, bob_score))

        # Output all results
        for alice_score, bob_score in results:
            print(f"{alice_score} {bob_score}")

if __name__ == "__main__":
    Main.main()
