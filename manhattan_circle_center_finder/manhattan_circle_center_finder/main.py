## main.py

from typing import List, Tuple


class ManhattanCircleFinder:
    """Class to find the center of a Manhattan circle in a grid."""

    @staticmethod
    def find_center(grid: List[List[str]], n: int, m: int) -> Tuple[int, int]:
        """Finds the center of the Manhattan circle in the given grid.

        Args:
            grid: 2D list representing the grid.
            n: Number of rows in the grid.
            m: Number of columns in the grid.

        Returns:
            Tuple of (row, col) representing the center (1-based indexing).
        """
        min_sum = float('inf')
        max_sum = float('-inf')
        min_diff = float('inf')
        max_diff = float('-inf')

        for i in range(n):
            for j in range(m):
                if grid[i][j] == '#':
                    s = i + j
                    d = i - j
                    if s < min_sum:
                        min_sum = s
                    if s > max_sum:
                        max_sum = s
                    if d < min_diff:
                        min_diff = d
                    if d > max_diff:
                        max_diff = d

        # The center is at the average of the extremal sums and diffs
        center_row = (min_sum + max_sum + min_diff + max_diff) // 4
        center_col = (min_sum + max_sum - min_diff - max_diff) // 4

        # Convert to 1-based indexing
        return center_row + 1, center_col + 1


class InputParser:
    """Class to parse input for the Manhattan circle problem."""

    @staticmethod
    def parse_input() -> List[Tuple[int, int, List[List[str]]]]:
        """Parses input from standard input.

        Returns:
            List of tuples, each containing (n, m, grid) for a test case.
        """
        import sys

        input_lines = sys.stdin.read().splitlines()
        test_cases = []
        idx = 0

        if idx >= len(input_lines):
            return test_cases

        t = int(input_lines[idx].strip())
        idx += 1

        for _ in range(t):
            if idx >= len(input_lines):
                break
            n_m = input_lines[idx].strip().split()
            idx += 1
            n = int(n_m[0])
            m = int(n_m[1])
            grid = []
            for _ in range(n):
                if idx >= len(input_lines):
                    break
                row = list(input_lines[idx].strip())
                grid.append(row)
                idx += 1
            test_cases.append((n, m, grid))
        return test_cases


class OutputFormatter:
    """Class to format and output the results."""

    @staticmethod
    def format_output(centers: List[Tuple[int, int]]) -> None:
        """Prints the centers for each test case.

        Args:
            centers: List of (row, col) tuples representing centers.
        """
        for row, col in centers:
            print(f"{row} {col}")


class Main:
    """Main class to orchestrate the Manhattan circle center finding."""

    def __init__(self) -> None:
        self.parser = InputParser()
        self.finder = ManhattanCircleFinder()
        self.formatter = OutputFormatter()

    def main(self) -> None:
        """Main method to run the program."""
        test_cases = self.parser.parse_input()
        centers: List[Tuple[int, int]] = []
        for n, m, grid in test_cases:
            center = self.finder.find_center(grid, n, m)
            centers.append(center)
        self.formatter.format_output(centers)


if __name__ == "__main__":
    Main().main()
