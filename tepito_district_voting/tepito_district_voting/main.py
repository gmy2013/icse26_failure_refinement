## main.py

from typing import List, Tuple, Optional


class DistrictPartitioner:
    """Handles partitioning the 2 x n grid into connected districts and maximizing Álvaro's wins."""

    def __init__(self, n: int, row1: str, row2: str) -> None:
        """
        Initializes the DistrictPartitioner.

        Args:
            n: Number of columns in the grid (must be a multiple of 3).
            row1: String representing the first row of the grid.
            row2: String representing the second row of the grid.
        """
        self.n: int = n
        self.grid: List[List[str]] = [list(row1), list(row2)]
        self.memo: dict = {}

        # Precompute all possible connected 3-cell shapes (relative positions)
        self.shapes: List[List[Tuple[int, int]]] = self._get_district_shapes()

    def _get_district_shapes(self) -> List[List[Tuple[int, int]]]:
        """
        Returns all possible connected 3-cell shapes in a 2xN grid.

        Returns:
            List of shapes, each shape is a list of (row, col) offsets.
        """
        # All possible connected 3-cell shapes in a 2xN grid
        # Each shape is a list of (row, col) offsets from the starting cell
        shapes = [
            # Horizontal line on top row
            [(0, 0), (0, 1), (0, 2)],
            # Horizontal line on bottom row
            [(1, 0), (1, 1), (1, 2)],
            # Vertical line
            [(0, 0), (1, 0), (0, 1)],
            [(0, 0), (1, 0), (1, 1)],
            # L-shape: top left corner
            [(0, 0), (0, 1), (1, 0)],
            # L-shape: bottom left corner
            [(1, 0), (1, 1), (0, 0)],
            # L-shape: top right corner
            [(0, 0), (0, 1), (1, 1)],
            # L-shape: bottom right corner
            [(1, 0), (1, 1), (0, 1)],
        ]
        return shapes

    def _count_alvaro_in_shape(self, base_row: int, base_col: int, shape: List[Tuple[int, int]]) -> int:
        """
        Counts the number of 'A' supporters in the given shape starting at (base_row, base_col).

        Args:
            base_row: Starting row index.
            base_col: Starting column index.
            shape: List of (row, col) offsets.

        Returns:
            Number of 'A' supporters in the shape.
        """
        count = 0
        for dr, dc in shape:
            r, c = base_row + dr, base_col + dc
            if 0 <= r < 2 and 0 <= c < self.n:
                if self.grid[r][c] == 'A':
                    count += 1
        return count

    def max_alvaro_wins(self) -> int:
        """
        Computes the maximum number of districts where Álvaro has at least 2 supporters.

        Returns:
            Maximum number of districts Álvaro can win.
        """
        # Use DP with bitmask to represent used cells
        # 2 rows * n columns = 2n cells, so bitmask is 2n bits
        total_cells = 2 * self.n

        def cell_bit(row: int, col: int) -> int:
            return row * self.n + col

        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dp(used_mask: int) -> int:
            # Base case: if all cells are used, return 0
            if used_mask == (1 << total_cells) - 1:
                return 0

            # Find the first unused cell (row, col)
            for idx in range(total_cells):
                if not (used_mask & (1 << idx)):
                    row, col = divmod(idx, self.n)
                    break
            else:
                return 0  # All used

            max_wins = float('-inf')
            # Try all shapes at this position
            for shape in self.shapes:
                valid = True
                shape_bits = 0
                cells = []
                for dr, dc in shape:
                    r, c = row + dr, col + dc
                    if 0 <= r < 2 and 0 <= c < self.n:
                        bit = cell_bit(r, c)
                        if used_mask & (1 << bit):
                            valid = False
                            break
                        shape_bits |= (1 << bit)
                        cells.append((r, c))
                    else:
                        valid = False
                        break
                if not valid or len(cells) != 3:
                    continue
                # Count 'A' in this shape
                alvaro_count = sum(self.grid[r][c] == 'A' for r, c in cells)
                win = 1 if alvaro_count >= 2 else 0
                # Recurse
                result = win + dp(used_mask | shape_bits)
                if result > max_wins:
                    max_wins = result
            return max_wins if max_wins != float('-inf') else 0

        return dp(0)


class InputHandler:
    """Handles reading and parsing input for multiple test cases."""

    def __init__(self) -> None:
        pass

    def read_test_cases(self) -> List[Tuple[int, str, str]]:
        """
        Reads test cases from standard input.

        Returns:
            List of tuples (n, row1, row2) for each test case.
        """
        import sys
        input_lines = sys.stdin.read().splitlines()
        test_cases: List[Tuple[int, str, str]] = []
        idx = 0
        t = int(input_lines[idx])
        idx += 1
        for _ in range(t):
            n = int(input_lines[idx])
            idx += 1
            row1 = input_lines[idx].strip()
            idx += 1
            row2 = input_lines[idx].strip()
            idx += 1
            test_cases.append((n, row1, row2))
        return test_cases


class OutputHandler:
    """Handles outputting the results."""

    def __init__(self) -> None:
        pass

    def print_results(self, results: List[int]) -> None:
        """
        Prints the results, one per line.

        Args:
            results: List of integers to print.
        """
        for res in results:
            print(res)


class Main:
    """Main class to orchestrate the program flow."""

    def main(self) -> None:
        """
        Main entry point for the program.
        """
        input_handler = InputHandler()
        output_handler = OutputHandler()
        test_cases = input_handler.read_test_cases()
        results: List[int] = []
        for n, row1, row2 in test_cases:
            partitioner = DistrictPartitioner(n, row1, row2)
            max_wins = partitioner.max_alvaro_wins()
            results.append(max_wins)
        output_handler.print_results(results)


if __name__ == "__main__":
    Main().main()
