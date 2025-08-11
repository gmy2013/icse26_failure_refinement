## main.py

from typing import List
import sys
import heapq


class QuantumHappinessPlanner:
    """Class to compute the maximum number of happiness units Charlie can buy."""

    def compute_max_happiness(self, m: int, x: int, costs: List[int]) -> int:
        """Compute the maximum number of happiness units that can be bought.

        Args:
            m: Number of months.
            x: Amount of money earned per month.
            costs: List of happiness unit costs for each month (length m).

        Returns:
            The maximum number of happiness units that can be bought.
        """
        # Priority queue (min-heap) to store available happiness units' costs
        available_units: List[int] = []
        # Suffix sum of money available for each month (money earned before this month)
        money_accumulated: int = 0
        # Number of happiness units bought
        happiness_count: int = 0

        # Process months in reverse: from last month to first
        for month in range(m - 1, -1, -1):
            # Add the happiness unit available in this month to the heap
            heapq.heappush(available_units, costs[month])
            # Money earned before this month
            money_accumulated += x

            # Greedily buy as many happiness units as possible, starting from the cheapest
            while available_units and available_units[0] <= money_accumulated:
                cheapest_cost = heapq.heappop(available_units)
                money_accumulated -= cheapest_cost
                happiness_count += 1

        return happiness_count


class Main:
    """Main class to handle CLI input/output."""

    @staticmethod
    def main() -> None:
        """Main entry point for the program."""
        planner = QuantumHappinessPlanner()
        input_lines = sys.stdin.read().splitlines()
        line_idx = 0

        # Read number of test cases
        t = int(input_lines[line_idx].strip())
        line_idx += 1

        for _ in range(t):
            # Read m and x
            m_x = input_lines[line_idx].strip().split()
            line_idx += 1
            m = int(m_x[0])
            x = int(m_x[1])

            # Read costs
            costs_str = input_lines[line_idx].strip().split()
            line_idx += 1
            costs = [int(cost) for cost in costs_str]

            # Compute and print result
            result = planner.compute_max_happiness(m, x, costs)
            print(result)


if __name__ == "__main__":
    Main.main()
