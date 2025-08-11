## main.py

from typing import List, Tuple


class MaxSubsequenceValueSolver:
    """Solver for the maximum subsequence value problem.

    The value of a subsequence is defined as:
        (size of subsequence) - (number of set bits in the bitwise OR of its elements)
    """

    def solve(self, test_cases: List[Tuple[int, List[int]]]) -> List[int]:
        """Solves multiple test cases.

        Args:
            test_cases: A list of tuples, each containing:
                - n: The number of elements in the array.
                - a: The list of integers.

        Returns:
            A list of integers, each representing the answer for a test case.
        """
        results: List[int] = []
        for n, a in test_cases:
            result = self._max_value_for_case(n, a)
            results.append(result)
        return results

    def _count_set_bits(self, x: int) -> int:
        """Counts the number of set bits (1s) in the binary representation of x.

        Args:
            x: The integer to count set bits in.

        Returns:
            The number of set bits in x.
        """
        return bin(x).count('1')

    def _max_value_for_case(self, n: int, a: List[int]) -> int:
        """Computes the maximum value for a single test case.

        Args:
            n: The number of elements in the array.
            a: The list of integers.

        Returns:
            The maximum value as per the problem statement.
        """
        # Value for each singleton subsequence
        max_value: int = float('-inf')
        for num in a:
            value = 1 - self._count_set_bits(num)
            if value > max_value:
                max_value = value

        # Value for the full array
        or_all: int = 0
        for num in a:
            or_all |= num
        value_full = n - self._count_set_bits(or_all)
        if value_full > max_value:
            max_value = value_full

        # Optionally, check all elements whose OR is the same as the full array
        # (i.e., all elements that do not reduce the OR)
        # This is an optimization: for all subsets whose OR is or_all,
        # the value is (size of subset) - set bits in or_all.
        # For small n, we could check all such subsets, but for n up to 100, this is not feasible.
        # So, we only check the full array and singletons.

        return max_value


class CLI:
    """Command-line interface for the MaxSubsequenceValueSolver."""

    def run(self) -> None:
        """Runs the CLI: parses input, solves the problem, and prints output."""
        test_cases = self._parse_input()
        solver = MaxSubsequenceValueSolver()
        results = solver.solve(test_cases)
        self._print_output(results)

    def _parse_input(self) -> List[Tuple[int, List[int]]]:
        """Parses input from stdin.

        Returns:
            A list of test cases, each as a tuple (n, a).
        """
        test_cases: List[Tuple[int, List[int]]] = []
        try:
            t_line = input()
            t = int(t_line.strip())
            for _ in range(t):
                n_line = input()
                n = int(n_line.strip())
                a_line = input()
                a = list(map(int, a_line.strip().split()))
                if len(a) != n:
                    raise ValueError("Number of elements does not match n.")
                test_cases.append((n, a))
        except Exception as e:
            print(f"Error parsing input: {e}")
            raise
        return test_cases

    def _print_output(self, results: List[int]) -> None:
        """Prints the results to stdout.

        Args:
            results: The list of results to print.
        """
        for res in results:
            print(res)


if __name__ == "__main__":
    cli = CLI()
    cli.run()
