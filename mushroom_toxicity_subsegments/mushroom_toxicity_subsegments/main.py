## main.py

from collections import Counter
from typing import List, Tuple


class MushroomToxicitySolver:
    """Solver for counting valid subsegments with nonzero final toxicity."""

    def solve(self, test_cases: List[Tuple[int, int, List[int]]]) -> List[int]:
        """Solve all test cases.

        Args:
            test_cases: List of tuples, each containing (n, x, a),
                where n is the number of mushrooms,
                x is the toxicity threshold,
                a is the list of toxicity values.

        Returns:
            List of integers, each representing the answer for a test case.
        """
        results: List[int] = []
        for n, x, a in test_cases:
            result = self._count_valid_subsegments(n, x, a)
            results.append(result)
        return results

    def _count_valid_subsegments(self, n: int, x: int, a: List[int]) -> int:
        """Count the number of subsegments with nonzero final toxicity.

        Args:
            n: Number of mushrooms.
            x: Toxicity threshold.
            a: List of toxicity values.

        Returns:
            The number of valid subsegments.
        """
        mod = x + 1
        prefix_sum = 0
        prefix_count = Counter()
        prefix_count[0] = 1  # Empty prefix sum
        total_subsegments = 0

        for value in a:
            prefix_sum = (prefix_sum + value) % mod
            # For each position, the number of subsegments ending here
            # whose sum modulo mod is zero is prefix_count[prefix_sum]
            # So, total subsegments so far = number of prefixes so far
            # The number of subsegments ending here is i+1 (since 0-based)
            # But we want subsegments whose sum modulo mod != 0
            # So, total subsegments ending here = i+1
            # Number of subsegments with sum modulo mod == 0 = prefix_count[prefix_sum]
            # So, number of subsegments with sum modulo mod != 0 = (i+1) - prefix_count[prefix_sum]
            # But we need to count all subsegments, so we count for all prefixes
            # Instead, we can count total number of subsegments, and subtract those with sum modulo mod == 0

            prefix_count[prefix_sum] += 1

        # Total number of subsegments = n * (n+1) // 2
        total_subsegments = n * (n + 1) // 2

        # Number of subsegments with sum modulo mod == 0
        zero_mod_subsegments = 0
        for count in prefix_count.values():
            # For each prefix sum value, the number of ways to choose two positions with the same prefix sum
            # (i.e., subsegment sum modulo mod == 0) is C(count, 2)
            zero_mod_subsegments += count * (count - 1) // 2

        valid_subsegments = total_subsegments - zero_mod_subsegments
        return valid_subsegments


class Main:
    """Main class for input parsing, output printing, and program flow."""

    @staticmethod
    def parse_input() -> List[Tuple[int, int, List[int]]]:
        """Parse input from standard input.

        Returns:
            List of test cases, each as a tuple (n, x, a).
        """
        import sys

        input_lines = sys.stdin.read().splitlines()
        test_cases: List[Tuple[int, int, List[int]]] = []
        idx = 0
        t = int(input_lines[idx].strip())
        idx += 1
        for _ in range(t):
            n_x = input_lines[idx].strip().split()
            n = int(n_x[0])
            x = int(n_x[1])
            idx += 1
            a = list(map(int, input_lines[idx].strip().split()))
            idx += 1
            test_cases.append((n, x, a))
        return test_cases

    @staticmethod
    def print_output(results: List[int]) -> None:
        """Print the results to standard output.

        Args:
            results: List of integers to print, one per line.
        """
        for res in results:
            print(res)

    @staticmethod
    def main() -> None:
        """Main program entry point."""
        test_cases = Main.parse_input()
        solver = MushroomToxicitySolver()
        results = solver.solve(test_cases)
        Main.print_output(results)


if __name__ == "__main__":
    Main.main()
