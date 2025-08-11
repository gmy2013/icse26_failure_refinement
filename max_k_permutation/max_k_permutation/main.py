## main.py

from typing import List, Tuple


class MaxKPermutationSolver:
    """Solver for the max_k_permutation problem.

    Provides methods to compute, for each test case, the permutation of 1..n
    that maximizes the final value of k after alternating bitwise AND and OR
    operations, starting with k=0 and the first operation being AND.
    """

    def solve(self, test_cases: List[int]) -> List[Tuple[int, List[int]]]:
        """Solves the max_k_permutation problem for multiple test cases.

        Args:
            test_cases: A list of integers, each representing n for a test case.

        Returns:
            A list of tuples, each containing:
                - The maximum possible value of k after all operations.
                - The permutation of 1..n that achieves this value.
        """
        results: List[Tuple[int, List[int]]] = []
        for n in test_cases:
            max_k, permutation = self._compute_permutation(n)
            results.append((max_k, permutation))
        return results

    def _compute_permutation(self, n: int) -> Tuple[int, List[int]]:
        """Computes the optimal permutation and resulting k for a given n.

        The optimal strategy is to arrange the numbers in decreasing order,
        i.e., [n, n-1, ..., 1]. This maximizes the bits set in k after
        alternating AND and OR operations.

        Args:
            n: The size of the permutation.

        Returns:
            A tuple containing:
                - The maximum possible value of k after all operations.
                - The permutation of 1..n that achieves this value.
        """
        # Generate the permutation in decreasing order
        permutation: List[int] = list(range(n, 0, -1))

        # Simulate the operations to compute the final value of k
        k: int = 0
        for idx, num in enumerate(permutation):
            if idx % 2 == 0:
                # Even index: AND operation
                k = k & num
            else:
                # Odd index: OR operation
                k = k | num

        return k, permutation


class Main:
    """Main entry point for the max_k_permutation program."""

    @staticmethod
    def main() -> None:
        """Reads input, solves the problem, and prints the results.

        Input format:
            The first line contains an integer t, the number of test cases.
            Each of the next t lines contains a single integer n.

        Output format:
            For each test case, print two lines:
                - The first line contains the maximum possible value of k.
                - The second line contains the permutation (space-separated).
        """
        import sys

        # Read number of test cases
        t_line = sys.stdin.readline()
        while t_line.strip() == '':
            t_line = sys.stdin.readline()
        t: int = int(t_line.strip())

        test_cases: List[int] = []
        read_cases: int = 0
        while read_cases < t:
            n_line = sys.stdin.readline()
            if n_line == '':
                continue
            n_line = n_line.strip()
            if n_line == '':
                continue
            n = int(n_line)
            test_cases.append(n)
            read_cases += 1

        solver = MaxKPermutationSolver()
        results = solver.solve(test_cases)

        for max_k, permutation in results:
            print(max_k)
            print(' '.join(str(num) for num in permutation))


if __name__ == "__main__":
    Main.main()
