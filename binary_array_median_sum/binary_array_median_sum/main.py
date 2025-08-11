## main.py
from typing import List, Optional
import sys
import threading

MOD: int = 10 ** 9 + 7
MAX_N: int = 2 * 10 ** 5 + 10


class Combinatorics:
    """Efficient combinatorics for binomial coefficients modulo mod."""

    def __init__(self, max_n: int = MAX_N, mod: int = MOD) -> None:
        self.mod: int = mod
        self.max_n: int = max_n
        self.fact: List[int] = [1] * (self.max_n + 1)
        self.inv_fact: List[int] = [1] * (self.max_n + 1)
        self._precompute()

    def _precompute(self) -> None:
        """Precompute factorials and inverse factorials modulo mod."""
        for i in range(1, self.max_n + 1):
            self.fact[i] = self.fact[i - 1] * i % self.mod
        self.inv_fact[self.max_n] = pow(self.fact[self.max_n], self.mod - 2, self.mod)
        for i in range(self.max_n, 0, -1):
            self.inv_fact[i - 1] = self.inv_fact[i] * i % self.mod

    def nCr(self, n: int, r: int) -> int:
        """Compute n choose r modulo mod."""
        if r < 0 or r > n:
            return 0
        return self.fact[n] * self.inv_fact[r] % self.mod * self.inv_fact[n - r] % self.mod


class BinaryArrayMedianSumSolver:
    """Solver for sum of medians of all subsequences of length k in a binary array."""

    def __init__(self, max_n: int = MAX_N, mod: int = MOD) -> None:
        self.combi: Combinatorics = Combinatorics(max_n, mod)
        self.mod: int = mod

    def solve_case(self, n: int, k: int, a: List[int]) -> int:
        """
        Compute the sum of medians of all subsequences of length k in binary array a.

        Args:
            n: Length of the array.
            k: Length of subsequences.
            a: The binary array.

        Returns:
            The sum of medians modulo mod.
        """
        # Find all indices where a[i] == 1
        ones_indices: List[int] = [i for i, val in enumerate(a) if val == 1]
        total_ones: int = len(ones_indices)
        if k % 2 == 0:
            # For even k, median is not well-defined for binary array, as per problem context.
            # If needed, can be adjusted, but for now, assume k is always odd.
            return 0

        need_ones: int = (k + 1) // 2  # Minimum number of 1s in subsequence for median to be 1
        if total_ones < need_ones:
            return 0

        # For each position of 1, count the number of subsequences of length k where this 1 is the median
        # For a 1 at position i (among all ones), it is the median if:
        # - We pick (need_ones-1) ones before i, and (k-need_ones) elements after i (from the rest of the array)
        # For each 1 at index idx in ones_indices:
        result: int = 0
        for idx, pos in enumerate(ones_indices):
            left_ones: int = idx  # number of 1s before this position
            right_ones: int = total_ones - idx - 1  # number of 1s after this position

            # Number of ways to pick (need_ones-1) ones from left_ones
            ways_left: int = self.combi.nCr(left_ones, need_ones - 1)
            # Number of ways to pick (k-need_ones) elements from the rest (excluding this 1 and left_ones used)
            rest: int = n - pos - 1  # elements after this position
            left_rest: int = pos - left_ones  # zeros before this position
            right_rest: int = n - pos - 1 - right_ones  # zeros after this position

            # Number of elements to pick from the rest (excluding the ones used for left_ones and this 1)
            total_rest: int = n - 1 - left_ones  # all except this 1 and left_ones used
            # But we need to pick (k-need_ones) elements from the right of the array (including zeros and ones)
            # Actually, for each 1 at position pos, the number of ways is:
            # - choose (need_ones-1) from left_ones
            # - choose (k-need_ones) from n - pos - 1 (elements after pos)
            ways_right: int = self.combi.nCr(n - pos - 1, k - need_ones)
            result = (result + ways_left * ways_right) % self.mod

        return result


class Main:
    """Main class to handle input/output and run the solver."""

    @staticmethod
    def main() -> None:
        import sys

        def input() -> str:
            return sys.stdin.readline()

        solver: BinaryArrayMedianSumSolver = BinaryArrayMedianSumSolver(MAX_N, MOD)
        t_line: Optional[str] = sys.stdin.readline()
        while t_line is not None and t_line.strip() == '':
            t_line = sys.stdin.readline()
        t: int = int(t_line.strip()) if t_line is not None else 0
        results: List[int] = []
        for _ in range(t):
            n_k_line: Optional[str] = sys.stdin.readline()
            while n_k_line is not None and n_k_line.strip() == '':
                n_k_line = sys.stdin.readline()
            n_str, k_str = n_k_line.strip().split()
            n: int = int(n_str)
            k: int = int(k_str)
            a_line: Optional[str] = sys.stdin.readline()
            while a_line is not None and a_line.strip() == '':
                a_line = sys.stdin.readline()
            a: List[int] = list(map(int, a_line.strip().split()))
            result: int = solver.solve_case(n, k, a)
            results.append(result)
        for res in results:
            print(res)


if __name__ == "__main__":
    threading.Thread(target=Main.main).start()
