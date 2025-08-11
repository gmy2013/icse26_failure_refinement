## main.py
"""Main module for reducing arrays to all zeros using at most 40 operations.

This module defines the ArrayZeroSolver class, which encapsulates the logic
for reducing an array to all zeros using the operation a_i := |a_i - x|, and
a main function that handles input/output for multiple test cases.

No third-party dependencies are required.
"""

import sys
from typing import List, Tuple


class ArrayZeroSolver:
    """Solver for reducing an array to all zeros using at most 40 operations."""

    def solve_case(self, a: List[int]) -> Tuple[int, List[int]]:
        """Reduces the array to all zeros using at most 40 operations.

        Args:
            a: List[int]. The input array.

        Returns:
            Tuple[int, List[int]]: A tuple containing:
                - The number of operations performed (k).
                - The list of x values used in each operation.
        """
        n: int = len(a)
        ops: List[int] = []
        arr: List[int] = a.copy()
        max_steps: int = 40

        for _ in range(max_steps):
            if all(x == 0 for x in arr):
                break
            x: int = max(arr)
            if x == 0:
                break
            arr = [abs(val - x) for val in arr]
            ops.append(x)
        # After the loop, arr should be all zeros
        return len(ops), ops


class Main:
    """Main entry point for the program."""

    @staticmethod
    def main() -> None:
        """Reads input, processes test cases, and outputs results."""
        import threading

        def run():
            input_lines = sys.stdin.read().splitlines()
            input_iter = iter(input_lines)
            t: int = int(next(input_iter))
            solver = ArrayZeroSolver()
            output_lines: List[str] = []

            for _ in range(t):
                n_line = ''
                # Skip empty lines (if any)
                while n_line.strip() == '':
                    n_line = next(input_iter)
                n: int = int(n_line)
                a_line = ''
                while a_line.strip() == '':
                    a_line = next(input_iter)
                a: List[int] = list(map(int, a_line.strip().split()))
                k, ops = solver.solve_case(a)
                output_lines.append(str(k))
                if k > 0:
                    output_lines.append(' '.join(map(str, ops)))
            print('\n'.join(output_lines))

        threading.Thread(target=run,).start()


if __name__ == "__main__":
    Main.main()
