## main.py

from typing import List, Dict, Tuple
import sys
from collections import defaultdict


class InputParser:
    """Class to parse input from stdin for Charlie's happiness planner problem."""

    @staticmethod
    def parse_input() -> List[Dict]:
        """
        Parses the input from stdin.

        Returns:
            List[Dict]: A list of test case dictionaries, each containing:
                - 'm': int, number of months
                - 'x': int, monthly salary
                - 'opportunities': List[Tuple[int, int]], list of (cost, happiness) per month
        """
        test_cases = []
        lines = []
        for line in sys.stdin:
            line = line.strip()
            if line:
                lines.append(line)
        if not lines:
            return test_cases

        idx = 0
        t = int(lines[idx])
        idx += 1
        for _ in range(t):
            m_x = lines[idx].split()
            m = int(m_x[0])
            x = int(m_x[1])
            idx += 1
            opportunities = []
            for _ in range(m):
                c_h = lines[idx].split()
                c = int(c_h[0])
                h = int(c_h[1])
                opportunities.append((c, h))
                idx += 1
            test_cases.append({
                'm': m,
                'x': x,
                'opportunities': opportunities
            })
        return test_cases


class CharlieHappinessPlanner:
    """Class to solve Charlie's happiness maximization problem."""

    def solve(self, test_cases: List[Dict]) -> List[int]:
        """
        Solves all test cases.

        Args:
            test_cases (List[Dict]): List of test case dictionaries.

        Returns:
            List[int]: List of maximum happiness values for each test case.
        """
        results = []
        for case in test_cases:
            m = case['m']
            x = case['x']
            opportunities = case['opportunities']
            max_happiness = self._max_happiness(m, x, opportunities)
            results.append(max_happiness)
        return results

    def _max_happiness(self, m: int, x: int, opportunities: List[Tuple[int, int]]) -> int:
        """
        Computes the maximum happiness for a single test case using DP.

        Args:
            m (int): Number of months.
            x (int): Monthly salary.
            opportunities (List[Tuple[int, int]]): List of (cost, happiness) per month.

        Returns:
            int: Maximum achievable happiness.
        """
        # dp[i]: dict mapping available money to max happiness at month i
        # At month 0, Charlie has 0 money and 0 happiness
        dp = defaultdict(int)
        dp[0] = 0  # money: happiness

        for month in range(m):
            cost, happiness = opportunities[month]
            # At the start of this month, Charlie receives salary
            next_dp = defaultdict(int)
            for money, curr_happiness in dp.items():
                # Option 1: Skip this opportunity
                new_money = money + x
                if next_dp[new_money] < curr_happiness:
                    next_dp[new_money] = curr_happiness
                # Option 2: Take this opportunity if enough money (from previous months)
                if money >= cost:
                    spent_money = money - cost + x
                    new_happiness = curr_happiness + happiness
                    if next_dp[spent_money] < new_happiness:
                        next_dp[spent_money] = new_happiness
            dp = next_dp
        # The answer is the maximum happiness over all possible money states
        return max(dp.values()) if dp else 0


class OutputFormatter:
    """Class to format and print output for Charlie's happiness planner problem."""

    @staticmethod
    def format_output(results: List[int]) -> None:
        """
        Prints the results, one per line.

        Args:
            results (List[int]): List of results to print.
        """
        for res in results:
            print(res)


def main() -> None:
    """
    Main function to orchestrate input parsing, problem solving, and output formatting.
    """
    parser = InputParser()
    planner = CharlieHappinessPlanner()
    formatter = OutputFormatter()

    test_cases = parser.parse_input()
    results = planner.solve(test_cases)
    formatter.format_output(results)


if __name__ == "__main__":
    main()
