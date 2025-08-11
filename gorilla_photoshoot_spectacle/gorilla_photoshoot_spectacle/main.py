## main.py

from typing import List, Dict


class GorillaPhotoshootSpectacle:
    """Class to compute the maximum spectacle value for gorilla photoshoot grids."""

    def __init__(self) -> None:
        """Initializes the GorillaPhotoshootSpectacle class."""
        pass

    def process_test_cases(self, test_cases: List[Dict]) -> List[int]:
        """Processes multiple test cases and returns the maximum spectacle value for each.

        Args:
            test_cases: A list of dictionaries, each containing keys:
                - 'n': int, number of rows in the grid.
                - 'm': int, number of columns in the grid.
                - 'k': int, size of the sub-square.
                - 'gorilla_heights': List[int], list of gorilla heights.

        Returns:
            List[int]: List of maximum spectacle values for each test case.
        """
        results: List[int] = []
        for case in test_cases:
            n: int = case['n']
            m: int = case['m']
            k: int = case['k']
            gorilla_heights: List[int] = case['gorilla_heights']
            result: int = self.max_spectacle(n, m, k, gorilla_heights)
            results.append(result)
        return results

    def max_spectacle(
        self, n: int, m: int, k: int, gorilla_heights: List[int]
    ) -> int:
        """Computes the maximum spectacle value for a single test case.

        Args:
            n: Number of rows in the grid.
            m: Number of columns in the grid.
            k: Size of the sub-square.
            gorilla_heights: List of gorilla heights.

        Returns:
            int: The maximum spectacle value.
        """
        cell_weights: List[int] = self._cell_weights(n, m, k)
        sorted_weights: List[int] = sorted(cell_weights, reverse=True)
        sorted_heights: List[int] = sorted(gorilla_heights, reverse=True)

        # Only as many gorillas as cells
        num_cells: int = n * m
        num_gorillas: int = min(len(sorted_heights), num_cells)
        spectacle: int = 0
        for i in range(num_gorillas):
            spectacle += sorted_weights[i] * sorted_heights[i]
        return spectacle

    def _cell_weights(self, n: int, m: int, k: int) -> List[int]:
        """Computes the weight (number of k x k sub-squares) for each cell in the grid.

        Args:
            n: Number of rows in the grid.
            m: Number of columns in the grid.
            k: Size of the sub-square.

        Returns:
            List[int]: List of weights for each cell, flattened row-wise.
        """
        weights: List[int] = []
        for i in range(n):
            for j in range(m):
                # The number of k x k sub-squares that include cell (i, j)
                row_choices: int = min(i + 1, n - k + 1, k, n - i)
                col_choices: int = min(j + 1, m - k + 1, k, m - j)
                # The cell is included in (number of possible top-left corners for k x k that include (i, j))
                row_count: int = min(i + 1, n - k + 1, k, n - i, n - k + 1)
                col_count: int = min(j + 1, m - k + 1, k, m - j, m - k + 1)
                # Actually, the number of k x k sub-squares that include (i, j) is:
                # (number of possible top-left corners for k x k that include (i, j))
                row_start: int = max(0, i - k + 1)
                row_end: int = min(i, n - k)
                col_start: int = max(0, j - k + 1)
                col_end: int = min(j, m - k)
                count: int = max(0, row_end - row_start + 1) * max(0, col_end - col_start + 1)
                weights.append(count)
        return weights


class CLI:
    """Command-line interface for the Gorilla Photoshoot Spectacle application."""

    def __init__(self) -> None:
        """Initializes the CLI class."""
        self.spectacle_solver = GorillaPhotoshootSpectacle()

    def read_input(self) -> List[Dict]:
        """Reads input from the user for multiple test cases.

        Returns:
            List[Dict]: List of test case dictionaries.
        """
        test_cases: List[Dict] = []
        try:
            t: int = int(input().strip())
        except Exception:
            print("Invalid input for number of test cases.")
            return test_cases

        for _ in range(t):
            try:
                nmk: List[int] = list(map(int, input().strip().split()))
                if len(nmk) != 3:
                    print("Invalid input for n, m, k.")
                    continue
                n, m, k = nmk
                gorilla_heights: List[int] = list(map(int, input().strip().split()))
                if len(gorilla_heights) != n * m:
                    print(f"Expected {n * m} gorilla heights, got {len(gorilla_heights)}.")
                    continue
                test_cases.append({
                    'n': n,
                    'm': m,
                    'k': k,
                    'gorilla_heights': gorilla_heights
                })
            except Exception:
                print("Invalid input for test case.")
                continue
        return test_cases

    def display_results(self, results: List[int]) -> None:
        """Displays the results to the user.

        Args:
            results: List of maximum spectacle values.
        """
        for value in results:
            print(value)

    def run(self) -> None:
        """Runs the CLI application."""
        test_cases: List[Dict] = self.read_input()
        if not test_cases:
            return
        results: List[int] = self.spectacle_solver.process_test_cases(test_cases)
        self.display_results(results)


if __name__ == "__main__":
    cli = CLI()
    cli.run()
