## main.py

from typing import List
import sys

class MinOperationsSolver:
    """Solver for minimum operations to make substrings of two strings equal.

    Uses prefix sum arrays for character frequencies to efficiently answer queries.
    """

    def __init__(self, n: int, a: str, b: str) -> None:
        """Initializes the solver with two strings and precomputes prefix sums.

        Args:
            n: Length of the strings.
            a: First string.
            b: Second string.
        """
        self.n: int = n
        self.a: str = a
        self.b: str = b
        self.prefix_a: List[List[int]] = self._build_prefix_sum(a)
        self.prefix_b: List[List[int]] = self._build_prefix_sum(b)

    def _build_prefix_sum(self, s: str) -> List[List[int]]:
        """Builds a prefix sum array for character frequencies.

        Args:
            s: Input string.

        Returns:
            A 2D list where prefix[c][i] is the count of character c up to position i.
        """
        prefix: List[List[int]] = [[0] * (self.n + 1) for _ in range(26)]
        for i in range(1, self.n + 1):
            char_idx = ord(s[i - 1]) - ord('a')
            for c in range(26):
                prefix[c][i] = prefix[c][i - 1]
            prefix[char_idx][i] += 1
        return prefix

    def min_operations(self, l: int, r: int) -> int:
        """Calculates the minimum number of operations to make substrings a[l..r] and b[l..r] equal.

        Args:
            l: Left index (1-based, inclusive).
            r: Right index (1-based, inclusive).

        Returns:
            The minimum number of operations required.
        """
        ops: int = 0
        for c in range(26):
            count_a = self.prefix_a[c][r] - self.prefix_a[c][l - 1]
            count_b = self.prefix_b[c][r] - self.prefix_b[c][l - 1]
            ops += abs(count_a - count_b)
        return ops // 2  # Each operation fixes one mismatch in both strings

class MainApp:
    """Main application class for CLI and user interaction."""

    def run(self) -> None:
        """Runs the main application loop, handling input and output."""
        input = sys.stdin.readline

        n_q_line = ''
        while n_q_line.strip() == '':
            n_q_line = input()
        n_str, q_str = n_q_line.strip().split()
        n: int = int(n_str)
        q: int = int(q_str)

        a_line = ''
        while a_line.strip() == '':
            a_line = input()
        a: str = a_line.strip()

        b_line = ''
        while b_line.strip() == '':
            b_line = input()
        b: str = b_line.strip()

        solver = MinOperationsSolver(n, a, b)

        results: List[str] = []
        for _ in range(q):
            query_line = ''
            while query_line.strip() == '':
                query_line = input()
            l_str, r_str = query_line.strip().split()
            l: int = int(l_str)
            r: int = int(r_str)
            min_ops = solver.min_operations(l, r)
            results.append(str(min_ops))

        print('\n'.join(results))


if __name__ == "__main__":
    app = MainApp()
    app.run()
