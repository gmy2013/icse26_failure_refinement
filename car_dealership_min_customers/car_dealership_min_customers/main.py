## main.py

import sys
import math
from typing import List, Tuple

class CarDealershipSolver:
    """Solver for the car dealership grouping problem."""

    @staticmethod
    def parse_input() -> List[Tuple[int, int, List[int]]]:
        """Parses input from stdin.

        Returns:
            List of test cases, each as a tuple (n, x, models),
            where n is the number of models, x is the max cars per customer,
            and models is a list of car counts per model.
        """
        input_lines = sys.stdin.read().splitlines()
        test_cases: List[Tuple[int, int, List[int]]] = []
        idx: int = 0
        t: int = int(input_lines[idx])
        idx += 1
        for _ in range(t):
            n_x = input_lines[idx].split()
            n: int = int(n_x[0])
            x: int = int(n_x[1])
            idx += 1
            models: List[int] = list(map(int, input_lines[idx].split()))
            idx += 1
            test_cases.append((n, x, models))
        return test_cases

    @staticmethod
    def solve(test_cases: List[Tuple[int, int, List[int]]]) -> List[int]:
        """Solves the car dealership problem for each test case.

        Args:
            test_cases: List of test cases.

        Returns:
            List of minimal number of customers for each test case.
        """
        results: List[int] = []
        for n, x, models in test_cases:
            max_model: int = max(models)
            total_cars: int = sum(models)
            min_customers: int = max(max_model, math.ceil(total_cars / x))
            results.append(min_customers)
        return results

    @staticmethod
    def format_output(results: List[int]) -> None:
        """Prints the results, one per line.

        Args:
            results: List of results to print.
        """
        output = '\n'.join(str(res) for res in results)
        sys.stdout.write(output + '\n')


class Main:
    """Main entry point for the program."""

    @staticmethod
    def main() -> None:
        """Runs the car dealership solver."""
        test_cases = CarDealershipSolver.parse_input()
        results = CarDealershipSolver.solve(test_cases)
        CarDealershipSolver.format_output(results)


if __name__ == "__main__":
    Main.main()
