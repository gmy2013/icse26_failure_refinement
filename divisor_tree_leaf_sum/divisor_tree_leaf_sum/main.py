## main.py

from typing import List
from functools import lru_cache
from sympy import divisors


class DivisorTreeSolver:
    """Solver for sum of leaves in divisor trees for i^k up to depth d."""

    MOD: int = 10 ** 9 + 7

    def __init__(self) -> None:
        """Initialize the solver."""
        pass  # No instance variables needed; all logic is in methods.

    @lru_cache(maxsize=None)
    def f(self, x: int, d: int) -> int:
        """
        Recursively compute the number of leaves in the divisor tree of x up to depth d.

        Args:
            x (int): The number whose divisor tree is considered.
            d (int): The depth of the tree.

        Returns:
            int: The number of leaves modulo MOD.
        """
        if d == 0:
            return 1
        total = 0
        for y in divisors(x):
            total = (total + self.f(y, d - 1)) % self.MOD
        return total

    def sum_of_leaves(self, n: int, k: int, d: int) -> int:
        """
        Compute the sum of leaves in divisor trees for all i^k (1 ≤ i ≤ n) up to depth d.

        Args:
            n (int): The upper bound of i.
            k (int): The exponent.
            d (int): The depth of the divisor tree.

        Returns:
            int: The sum modulo MOD.
        """
        result = 0
        for i in range(1, n + 1):
            x = pow(i, k)
            result = (result + self.f(x, d)) % self.MOD
        return result


class Main:
    """Main CLI interface for the divisor tree sum problem."""

    def run(self) -> None:
        """
        Run the CLI interface: read input, process test cases, and print results.
        """
        import sys

        solver = DivisorTreeSolver()
        input_lines = sys.stdin.read().splitlines()
        t = int(input_lines[0])
        results: List[int] = []
        for idx in range(1, t + 1):
            n_str, k_str, d_str = input_lines[idx].strip().split()
            n = int(n_str)
            k = int(k_str)
            d = int(d_str)
            res = solver.sum_of_leaves(n, k, d)
            results.append(res)
        for res in results:
            print(res)


if __name__ == "__main__":
    Main().run()
