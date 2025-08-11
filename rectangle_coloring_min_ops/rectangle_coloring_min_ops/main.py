## main.py

from typing import List, Dict, Any


class Rectangle:
    """Represents a rectangle and provides row/column completion costs."""

    def __init__(self, width: int, height: int) -> None:
        """Initializes a Rectangle with given width and height.

        Args:
            width: The width of the rectangle (number of columns).
            height: The height of the rectangle (number of rows).
        """
        self._width: int = width
        self._height: int = height

    def get_completion_costs(self) -> List[int]:
        """Returns the list of costs to fully color each row and column.

        Returns:
            A list of integers, each representing the cost to color a row or column.
            There are 'height' row costs (each of value 'width') and
            'width' column costs (each of value 'height').
        """
        row_costs = [self._width] * self._height
        col_costs = [self._height] * self._width
        return row_costs + col_costs


class RectangleColoringSolver:
    """Solves the rectangle coloring problem for multiple test cases."""

    @staticmethod
    def solve(test_cases: List[Dict[str, Any]]) -> List[int]:
        """Solves all test cases and returns the minimal coloring costs.

        Args:
            test_cases: A list of dictionaries, each representing a test case with keys:
                - 'n': number of rectangles
                - 'k': required number of points
                - 'rectangles': list of (width, height) tuples

        Returns:
            A list of integers, each being the minimal coloring cost for the corresponding test case,
            or -1 if it is not possible to reach at least k points.
        """
        results: List[int] = []
        for case in test_cases:
            n: int = case['n']
            k: int = case['k']
            rectangles: List[List[int]] = case['rectangles']

            completion_costs: List[int] = []
            for rect_dims in rectangles:
                width, height = rect_dims
                rect = Rectangle(width, height)
                completion_costs.extend(rect.get_completion_costs())

            if len(completion_costs) < k:
                results.append(-1)
                continue

            completion_costs.sort()
            min_cost = sum(completion_costs[:k])
            results.append(min_cost)
        return results


class Main:
    """Handles input/output and orchestrates the rectangle coloring solution."""

    @staticmethod
    def parse_input() -> List[Dict[str, Any]]:
        """Parses input from stdin as per the problem specification.

        Returns:
            A list of test case dictionaries.
        """
        import sys

        input_lines = sys.stdin.read().splitlines()
        test_cases: List[Dict[str, Any]] = []
        idx = 0
        t = int(input_lines[idx].strip())
        idx += 1

        for _ in range(t):
            n_k = input_lines[idx].strip().split()
            idx += 1
            n = int(n_k[0])
            k = int(n_k[1])
            rectangles: List[List[int]] = []
            for _ in range(n):
                a_b = input_lines[idx].strip().split()
                idx += 1
                width = int(a_b[0])
                height = int(a_b[1])
                rectangles.append([width, height])
            test_cases.append({'n': n, 'k': k, 'rectangles': rectangles})
        return test_cases

    @staticmethod
    def print_output(results: List[int]) -> None:
        """Prints the results, one per line.

        Args:
            results: List of results to print.
        """
        for res in results:
            print(res)

    @staticmethod
    def main() -> None:
        """Main entry point for the program."""
        test_cases = Main.parse_input()
        results = RectangleColoringSolver.solve(test_cases)
        Main.print_output(results)


if __name__ == "__main__":
    Main.main()
