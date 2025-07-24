## main.py

from typing import List, Tuple
import sys



class CityConquestSolver:
    """Solver for the city conquest problem."""

    def __init__(self) -> None:
        """Initializes the CityConquestSolver."""
        pass

    def count_valid_starting_cities(self, n: int, deadlines: List[int]) -> int:
        """Counts the number of valid starting cities.

        Args:
            n: The number of cities.
            deadlines: A list of deadlines for each city.

        Returns:
            The number of valid starting cities.
        """
        # For each city, we want to check if starting from that city,
        # we can conquer all cities within their deadlines.
        # Since we can only move to adjacent cities, the time to reach city i
        # from starting city s is abs(i - s).
        # For city i, the latest possible starting city s is such that
        # abs(i - s) <= deadlines[i], i.e., s in [i - deadlines[i], i + deadlines[i]]
        # So, for each city, the valid starting city indices are in this range.
        # The intersection of all these ranges gives the set of valid starting cities.

        left = 0
        right = n - 1

        for i in range(n):
            l = max(0, i - deadlines[i])
            r = min(n - 1, i + deadlines[i])
            left = max(left, l)
            right = min(right, r)
            if left > right:
                # No valid starting city possible
                return 0

        return right - left + 1

    def process_test_cases(self, test_cases: List[Tuple[int, List[int]]]) -> List[int]:
        """Processes multiple test cases.

        Args:
            test_cases: A list of tuples, each containing the number of cities and the deadlines list.

        Returns:
            A list of results, one for each test case.
        """
        results: List[int] = []
        for n, deadlines in test_cases:
            result = self.count_valid_starting_cities(n, deadlines)
            results.append(result)
        return results


class Main:
    """Main class to handle input/output and program flow."""

    @staticmethod
    def parse_input() -> List[Tuple[int, List[int]]]:
        """Parses input from stdin.

        Returns:
            A list of test cases, each as a tuple (n, deadlines).
        """
        input_lines = sys.stdin.read().splitlines()
        test_cases: List[Tuple[int, List[int]]] = []
        idx = 0
        if not input_lines:
            return test_cases

        t = 0
        while idx < len(input_lines):
            line = input_lines[idx].strip()
            if not line:
                idx += 1
                continue
            if t == 0:
                try:
                    t = int(line)
                except ValueError:
                    raise ValueError("Invalid input: first line must be the number of test cases.")
                idx += 1
                continue
            # For each test case, read n and deadlines
            n_line = input_lines[idx].strip()
            if not n_line:
                idx += 1
                continue
            try:
                n = int(n_line)
            except ValueError:
                raise ValueError(f"Invalid input: expected integer for number of cities, got '{n_line}'.")
            idx += 1
            if idx >= len(input_lines):
                raise ValueError("Invalid input: deadlines line missing.")
            deadlines_line = input_lines[idx].strip()
            try:
                deadlines = list(map(int, deadlines_line.split()))
            except ValueError:
                raise ValueError(f"Invalid input: deadlines must be integers, got '{deadlines_line}'.")
            if len(deadlines) != n:
                raise ValueError(f"Invalid input: expected {n} deadlines, got {len(deadlines)}.")
            test_cases.append((n, deadlines))
            idx += 1
        if len(test_cases) != t:
            raise ValueError(f"Invalid input: expected {t} test cases, got {len(test_cases)}.")
        return test_cases

    @staticmethod
    def print_output(results: List[int]) -> None:
        """Prints the results to stdout.

        Args:
            results: A list of results to print.
        """
        for res in results:
            print(res)

    @staticmethod
    def main() -> None:
        """Main entry point."""
        try:
            test_cases = Main.parse_input()
            solver = CityConquestSolver()
            results = solver.process_test_cases(test_cases)
            Main.print_output(results)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    Main.main()
