## main.py

import sys
from typing import List


class GridOperationSolver:
    """Solver for minimizing operations to whiten all black cells in a grid."""

    def __init__(self) -> None:
        """Initializes the GridOperationSolver."""
        pass

    def min_operations(self, n: int, a: List[int]) -> int:
        """Calculates the minimum number of operations to whiten all black cells.

        Args:
            n: The number of rows in the grid.
            a: A list of integers, where a[i] is the number of black cells in row i.

        Returns:
            The minimum number of operations required.
        """
        # Copy the list to avoid mutating the input
        black_cells = a[:]
        total_ops = 0
        i = 0

        while i < n - 1:
            # The number of 2x2 subgrid operations we can apply between row i and i+1
            subgrid_ops = min(black_cells[i], black_cells[i + 1])
            if subgrid_ops > 0:
                black_cells[i] -= subgrid_ops
                black_cells[i + 1] -= subgrid_ops
                total_ops += subgrid_ops
            i += 1

        # After all possible 2x2 subgrid operations, whiten remaining black cells row-wise
        for row_black in black_cells:
            if row_black > 0:
                total_ops += row_black

        return total_ops


class MainApp:
    """Main application class for handling input/output and running the solver."""

    def __init__(self) -> None:
        """Initializes the MainApp and its solver."""
        self.solver = GridOperationSolver()

    def run(self) -> None:
        """Reads input, processes each test case, and prints the results."""
        input_lines = sys.stdin.read().splitlines()
        idx = 0
        t = int(input_lines[idx])
        idx += 1

        for _ in range(t):
            n = int(input_lines[idx])
            idx += 1
            a = list(map(int, input_lines[idx].split()))
            idx += 1
            min_ops = self.solver.min_operations(n, a)
            print(min_ops)


if __name__ == "__main__":
    app = MainApp()
    app.run()
