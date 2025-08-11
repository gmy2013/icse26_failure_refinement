## main.py

from typing import List, Tuple


class GoodArraySolver:
    """Solver for finding the maximum length of a 'good' array for given (l, r) pairs."""

    @staticmethod
    def max_good_array_length(l: int, r: int) -> int:
        """Compute the maximum length n of a 'good' array for the given l and r.

        A 'good' array is defined such that the sum of the first (n-1) natural numbers
        does not exceed r - l.

        Args:
            l (int): The lower bound of the range.
            r (int): The upper bound of the range.

        Returns:
            int: The maximum possible length n of the 'good' array.
        """
        max_sum = r - l
        if max_sum < 0:
            return 0

        # Binary search for the largest n such that (n-1)*n/2 <= max_sum
        left: int = 1
        right: int = 2 * 10**9  # Safe upper bound for n
        result: int = 1

        while left <= right:
            mid: int = (left + right) // 2
            sum_n_minus_1: int = (mid - 1) * mid // 2
            if sum_n_minus_1 <= max_sum:
                result = mid
                left = mid + 1
            else:
                right = mid - 1

        return result

    def process_test_cases(self, test_cases: List[Tuple[int, int]]) -> List[int]:
        """Process multiple test cases and compute the maximum good array length for each.

        Args:
            test_cases (List[Tuple[int, int]]): List of (l, r) pairs.

        Returns:
            List[int]: List of results for each test case.
        """
        results: List[int] = []
        for l, r in test_cases:
            max_length = self.max_good_array_length(l, r)
            results.append(max_length)
        return results


class CLI:
    """Command-line interface for the GoodArraySolver."""

    def __init__(self) -> None:
        self.solver = GoodArraySolver()

    def run(self) -> None:
        """Run the CLI: read input, process test cases, and print results."""
        try:
            t_line = input().strip()
            while t_line == '':
                t_line = input().strip()
            t: int = int(t_line)
        except (ValueError, EOFError):
            print("Invalid input for number of test cases.")
            return

        test_cases: List[Tuple[int, int]] = []
        read_cases: int = 0
        while read_cases < t:
            try:
                line = input().strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) != 2:
                    print("Each test case must contain exactly two integers.")
                    continue
                l, r = int(parts[0]), int(parts[1])
                test_cases.append((l, r))
                read_cases += 1
            except (ValueError, EOFError):
                print("Invalid input for test case. Please enter two integers.")
                continue

        results: List[int] = self.solver.process_test_cases(test_cases)
        for res in results:
            print(res)


if __name__ == "__main__":
    cli = CLI()
    cli.run()
