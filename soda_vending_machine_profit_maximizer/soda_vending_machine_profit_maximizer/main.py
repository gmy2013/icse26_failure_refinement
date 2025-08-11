## main.py

from collections import defaultdict
import sys
from typing import List, Dict, Tuple

class SodaVendingMachineProfitMaximizer:
    """Class to maximize profit for soda vending machine shelf assignment."""

    @staticmethod
    def process_test_cases(test_cases: List[Dict]) -> List[int]:
        """Process multiple test cases and return the list of maximum profits.

        Args:
            test_cases: List of test case dictionaries, each with keys:
                - 'n': int, number of shelves
                - 'bottles': List[Tuple[int, int]], each tuple is (brand, cost)

        Returns:
            List[int]: Maximum profit for each test case.
        """
        results: List[int] = []
        for case in test_cases:
            n: int = case['n']
            bottles: List[Tuple[int, int]] = case['bottles']
            profit: int = SodaVendingMachineProfitMaximizer.max_profit(n, bottles)
            results.append(profit)
        return results

    @staticmethod
    def max_profit(n: int, bottles: List[Tuple[int, int]]) -> int:
        """Compute the maximum profit for a single test case.

        Args:
            n: Number of shelves.
            bottles: List of (brand, cost) tuples.

        Returns:
            int: Maximum profit achievable.
        """
        brand_to_total_cost: Dict[int, int] = defaultdict(int)
        for brand, cost in bottles:
            brand_to_total_cost[brand] += cost

        # Get all brand total profits
        brand_profits: List[int] = list(brand_to_total_cost.values())
        # Sort descending to pick the n most profitable brands
        brand_profits.sort(reverse=True)

        # If there are fewer brands than shelves, just sum all
        max_brands: int = min(n, len(brand_profits))
        max_profit: int = sum(brand_profits[:max_brands])
        return max_profit


class CLI:
    """Command-line interface for reading input and printing output."""

    @staticmethod
    def read_input() -> List[Dict]:
        """Read input from stdin and parse into test cases.

        Returns:
            List[Dict]: List of test case dictionaries.
        """
        input_lines = sys.stdin.read().splitlines()
        test_cases: List[Dict] = []
        idx: int = 0
        t: int = int(input_lines[idx])
        idx += 1
        for _ in range(t):
            n_m = input_lines[idx].split()
            n: int = int(n_m[0])
            m: int = int(n_m[1])
            idx += 1
            bottles: List[Tuple[int, int]] = []
            for _ in range(m):
                brand_cost = input_lines[idx].split()
                brand: int = int(brand_cost[0])
                cost: int = int(brand_cost[1])
                bottles.append((brand, cost))
                idx += 1
            test_cases.append({'n': n, 'bottles': bottles})
        return test_cases

    @staticmethod
    def print_output(results: List[int]) -> None:
        """Print the results, one per line.

        Args:
            results: List of integers to print.
        """
        for res in results:
            print(res)


def main() -> None:
    """Main function to coordinate CLI and profit maximizer."""
    test_cases: List[Dict] = CLI.read_input()
    results: List[int] = SodaVendingMachineProfitMaximizer.process_test_cases(test_cases)
    CLI.print_output(results)


if __name__ == "__main__":
    main()
