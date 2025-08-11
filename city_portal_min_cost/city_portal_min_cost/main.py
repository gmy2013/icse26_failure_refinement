## main.py

from bisect import bisect_left
from typing import List, Tuple, Dict


class CityPortalSystem:
    """Handles city portal color mapping and efficient minimum cost queries.

    Attributes:
        n (int): Number of cities.
        city_portals (List[str]): List of portal colors for each city.
        color_to_indices (Dict[str, List[int]]): Mapping from color to sorted list of city indices.
    """

    def __init__(self, n: int, city_portals: List[str]) -> None:
        """Initializes the CityPortalSystem with city portal colors.

        Args:
            n (int): Number of cities.
            city_portals (List[str]): List of portal colors for each city.
        """
        self.n: int = n
        self.city_portals: List[str] = city_portals
        self.color_to_indices: Dict[str, List[int]] = {}
        self._preprocess()

    def _preprocess(self) -> None:
        """Preprocesses the city portal colors to map each color to sorted city indices."""
        for idx, color in enumerate(self.city_portals):
            if color not in self.color_to_indices:
                self.color_to_indices[color] = []
            self.color_to_indices[color].append(idx)
        # Ensure all lists are sorted (though they are in input order)
        for indices in self.color_to_indices.values():
            indices.sort()

    def min_cost(self, x: int, y: int) -> int:
        """Finds the minimum cost to move from city x to city y.

        Args:
            x (int): Source city index (0-based).
            y (int): Destination city index (0-based).

        Returns:
            int: Minimum cost (number of moves) to reach city y from city x.
        """
        if x == y:
            return 0

        color_x = self.city_portals[x]
        color_y = self.city_portals[y]

        # Direct move if any color is shared between x and y
        if color_x == color_y:
            return 1

        # Try to find the minimal distance via color_y
        if color_y in self.color_to_indices:
            indices = self.color_to_indices[color_y]
            # Use bisect to find the closest city with color_y to x
            pos = bisect_left(indices, x)
            min_dist = float('inf')
            if pos < len(indices):
                min_dist = min(min_dist, abs(indices[pos] - x))
            if pos > 0:
                min_dist = min(min_dist, abs(indices[pos - 1] - x))
            # If y itself is the closest, cost is 1, else cost is 2 (move to closest, then to y)
            if min_dist == abs(y - x):
                return 1
            else:
                return 2
        # If color_y does not exist, cannot reach
        return -1


class QueryProcessor:
    """Manages multiple test cases and processes queries using CityPortalSystem.

    Attributes:
        systems (List[CityPortalSystem]): List of CityPortalSystem instances for each test case.
        queries_per_case (List[List[Tuple[int, int]]]): List of queries for each test case.
    """

    def __init__(self) -> None:
        """Initializes the QueryProcessor."""
        self.systems: List[CityPortalSystem] = []
        self.queries_per_case: List[List[Tuple[int, int]]] = []

    def add_test_case(self, n: int, city_portals: List[str], queries: List[Tuple[int, int]]) -> None:
        """Adds a test case with its city portals and queries.

        Args:
            n (int): Number of cities.
            city_portals (List[str]): List of portal colors for each city.
            queries (List[Tuple[int, int]]): List of queries as (x, y) tuples (0-based).
        """
        system = CityPortalSystem(n, city_portals)
        self.systems.append(system)
        self.queries_per_case.append(queries)

    def process_all(self) -> List[List[int]]:
        """Processes all queries for all test cases.

        Returns:
            List[List[int]]: List of results for each test case.
        """
        all_results: List[List[int]] = []
        for system, queries in zip(self.systems, self.queries_per_case):
            case_results: List[int] = []
            for x, y in queries:
                cost = system.min_cost(x, y)
                case_results.append(cost)
            all_results.append(case_results)
        return all_results


def main() -> None:
    """Entry point: reads input, processes queries, and prints results."""
    import sys

    input_lines = sys.stdin.read().splitlines()
    line_idx = 0

    t = int(input_lines[line_idx].strip())
    line_idx += 1

    processor = QueryProcessor()

    for _ in range(t):
        n, q = map(int, input_lines[line_idx].strip().split())
        line_idx += 1
        city_portals = input_lines[line_idx].strip().split()
        line_idx += 1
        queries: List[Tuple[int, int]] = []
        for _ in range(q):
            x_str, y_str = input_lines[line_idx].strip().split()
            x, y = int(x_str), int(y_str)
            queries.append((x, y))
            line_idx += 1
        processor.add_test_case(n, city_portals, queries)

    results = processor.process_all()
    for case_result in results:
        for res in case_result:
            print(res)


if __name__ == "__main__":
    main()
