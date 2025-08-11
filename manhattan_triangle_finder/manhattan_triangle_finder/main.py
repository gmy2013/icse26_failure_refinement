## main.py

from collections import defaultdict
import sys
from typing import List, Tuple, Dict, Optional

class ManhattanTriangleFinder:
    """Class to find three distinct points forming a Manhattan equilateral triangle."""

    def __init__(self, points: List[Tuple[int, int]]) -> None:
        """
        Initializes the finder with a list of points.

        Args:
            points: List of (x, y) tuples representing the points.
        """
        self.points: List[Tuple[int, int]] = points
        # Map from (x, y) to 1-based index for O(1) lookup
        self.point_to_index: Dict[Tuple[int, int], int] = {
            point: idx + 1 for idx, point in enumerate(points)
        }

    def find_triangle(self, d: int) -> Tuple[int, int, int]:
        """
        Finds three distinct points such that all pairwise Manhattan distances are exactly d.

        Args:
            d: The required Manhattan distance (must be even).

        Returns:
            A tuple of three 1-based indices of the points forming the triangle,
            or (0, 0, 0) if no such triangle exists.
        """
        if d % 2 != 0:
            return (0, 0, 0)  # Impossible for odd d

        # For each point, try all possible configurations
        for idx, (x, y) in enumerate(self.points):
            # Four possible configurations for equilateral triangle in Manhattan metric
            candidates = [
                # Axis-aligned right triangle
                ((x + d, y), (x, y + d)),
                ((x - d, y), (x, y + d)),
                ((x + d, y), (x, y - d)),
                ((x - d, y), (x, y - d)),
                # Diagonal triangle
                ((x + d // 2, y + d // 2), (x - d // 2, y - d // 2)),
                ((x + d // 2, y - d // 2), (x - d // 2, y + d // 2)),
            ]
            for (p2, p3) in candidates:
                idx2 = self.point_to_index.get(p2, 0)
                idx3 = self.point_to_index.get(p3, 0)
                # Ensure all indices are distinct and nonzero
                if idx2 and idx3 and idx2 != idx3 and idx2 != idx + 1 and idx3 != idx + 1:
                    return (idx + 1, idx2, idx3)
        return (0, 0, 0)


class Main:
    """Main class for input parsing, test case processing, and output formatting."""

    @staticmethod
    def parse_input() -> Tuple[int, List[List[Tuple[int, int]]], List[int]]:
        """
        Parses input from stdin.

        Returns:
            A tuple containing:
                - Number of test cases
                - List of points for each test case
                - List of d values for each test case
        """
        input_lines = sys.stdin.read().splitlines()
        t = int(input_lines[0])
        ptr = 1
        test_points: List[List[Tuple[int, int]]] = []
        test_ds: List[int] = []
        for _ in range(t):
            n, d = map(int, input_lines[ptr].split())
            ptr += 1
            points: List[Tuple[int, int]] = []
            for _ in range(n):
                x, y = map(int, input_lines[ptr].split())
                points.append((x, y))
                ptr += 1
            test_points.append(points)
            test_ds.append(d)
        return t, test_points, test_ds

    @staticmethod
    def process_test_cases() -> None:
        """
        Processes all test cases and prints the results.
        """
        t, test_points, test_ds = Main.parse_input()
        for case_idx in range(t):
            points = test_points[case_idx]
            d = test_ds[case_idx]
            finder = ManhattanTriangleFinder(points)
            result = finder.find_triangle(d)
            print(f"{result[0]} {result[1]} {result[2]}")


if __name__ == "__main__":
    Main.process_test_cases()
