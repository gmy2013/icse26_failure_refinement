## main.py

from typing import List, Tuple


class ActionFigureDiscountOptimizer:
    """Optimizes the total cost of purchasing action figures with group discounts."""

    def __init__(self) -> None:
        """Initializes the optimizer. No state is maintained between test cases."""
        pass

    def compute_min_cost(self, n: int, s: str, verbose: bool = False) -> int:
        """
        Computes the minimum total cost for a single test case.

        Args:
            n (int): The number of days (length of s).
            s (str): A string of digits, each representing the cost of an action figure on that day.
            verbose (bool): If True, prints step-by-step explanations.

        Returns:
            int: The minimum total cost after applying the discount optimally.
        """
        # Convert string to list of integers (costs)
        costs: List[int] = [int(ch) for ch in s]
        total_cost: int = 0
        i: int = 0

        if verbose:
            print(f"Processing {n} days: {costs}")

        while i < n:
            # Find the next group of consecutive days with available figures
            group: List[int] = []
            while i < n and s[i] != '0':
                group.append(costs[i])
                i += 1
            if group:
                max_in_group = max(group)
                group_sum = sum(group)
                group_cost = group_sum - max_in_group
                total_cost += group_cost
                if verbose:
                    print(f"Group found: {group}, max: {max_in_group}, "
                          f"sum: {group_sum}, cost after discount: {group_cost}")
            # Skip days with no figure (cost '0')
            while i < n and s[i] == '0':
                i += 1

        if verbose:
            print(f"Total minimum cost: {total_cost}")
        return total_cost

    def process_test_cases(self, test_cases: List[Tuple[int, str]], verbose: bool = False) -> List[int]:
        """
        Processes multiple test cases.

        Args:
            test_cases (List[Tuple[int, str]]): List of tuples, each containing (n, s).
            verbose (bool): If True, prints step-by-step explanations for each test case.

        Returns:
            List[int]: List of minimum costs for each test case.
        """
        results: List[int] = []
        for idx, (n, s) in enumerate(test_cases):
            if verbose:
                print(f"\nTest case {idx + 1}: n={n}, s={s}")
            min_cost = self.compute_min_cost(n, s, verbose)
            results.append(min_cost)
        return results


class CLI:
    """Command-line interface for the ActionFigureDiscountOptimizer."""

    def __init__(self) -> None:
        """Initializes the CLI."""
        self.optimizer = ActionFigureDiscountOptimizer()

    def run(self) -> None:
        """
        Runs the CLI, handling user input and output.
        Reads from standard input in the following format:
            t
            n1
            s1
            n2
            s2
            ...
        Where t is the number of test cases, and for each test case,
        n is the number of days, s is the string of costs.
        """
        import sys

        args = sys.argv[1:]
        verbose: bool = False
        if '--verbose' in args:
            verbose = True
            args.remove('--verbose')

        if not sys.stdin.isatty():
            # Input is being piped in
            input_lines = sys.stdin.read().splitlines()
        else:
            input_lines = []
            try:
                t = int(input("Enter number of test cases: ").strip())
                input_lines.append(str(t))
                for _ in range(t):
                    n = int(input("Enter number of days: ").strip())
                    s = input("Enter cost string: ").strip()
                    input_lines.append(str(n))
                    input_lines.append(s)
            except (EOFError, ValueError):
                print("Invalid input.")
                return

        if not input_lines:
            print("No input provided.")
            return

        try:
            t = int(input_lines[0])
            test_cases: List[Tuple[int, str]] = []
            idx = 1
            for _ in range(t):
                n = int(input_lines[idx])
                s = input_lines[idx + 1]
                test_cases.append((n, s))
                idx += 2
        except (IndexError, ValueError):
            print("Invalid input format.")
            return

        results = self.optimizer.process_test_cases(test_cases, verbose)
        for res in results:
            print(res)


if __name__ == "__main__":
    cli = CLI()
    cli.run()
