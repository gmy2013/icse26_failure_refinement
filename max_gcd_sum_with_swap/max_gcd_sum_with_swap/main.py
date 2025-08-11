## main.py

import sys
import math
from typing import List, Tuple

class GCDUtils:
    """Utility class for GCD-related operations."""

    @staticmethod
    def compute_prefix_gcd(arr: List[int]) -> List[int]:
        """Compute prefix GCDs for the given array.

        Args:
            arr: List of integers.

        Returns:
            List of prefix GCDs, where prefix_gcd[i] = GCD(arr[0], ..., arr[i]).
        """
        n = len(arr)
        prefix_gcd = [0] * n
        if n == 0:
            return prefix_gcd
        prefix_gcd[0] = arr[0]
        for i in range(1, n):
            prefix_gcd[i] = math.gcd(prefix_gcd[i - 1], arr[i])
        return prefix_gcd

    @staticmethod
    def compute_suffix_gcd(arr: List[int]) -> List[int]:
        """Compute suffix GCDs for the given array.

        Args:
            arr: List of integers.

        Returns:
            List of suffix GCDs, where suffix_gcd[i] = GCD(arr[i], ..., arr[n-1]).
        """
        n = len(arr)
        suffix_gcd = [0] * n
        if n == 0:
            return suffix_gcd
        suffix_gcd[-1] = arr[-1]
        for i in range(n - 2, -1, -1):
            suffix_gcd[i] = math.gcd(suffix_gcd[i + 1], arr[i])
        return suffix_gcd


class GCDSegmentSwapSolver:
    """Solver for the segment swap GCD maximization problem."""

    def solve_case(self, a: List[int], b: List[int]) -> Tuple[int, int]:
        """Solve a single test case.

        For all possible segments (l, r), swap a[l:r+1] with b[l:r+1],
        and compute the sum of GCDs of the resulting arrays.
        Return the maximum sum and the number of ways to achieve it.

        Args:
            a: List of integers, first array.
            b: List of integers, second array.

        Returns:
            Tuple of (maximum sum, number of ways to achieve it).
        """
        n = len(a)
        # Precompute prefix and suffix GCDs for both arrays
        prefix_gcd_a = GCDUtils.compute_prefix_gcd(a)
        suffix_gcd_a = GCDUtils.compute_suffix_gcd(a)
        prefix_gcd_b = GCDUtils.compute_prefix_gcd(b)
        suffix_gcd_b = GCDUtils.compute_suffix_gcd(b)

        max_sum = -1
        count = 0

        # For all possible segments (l, r)
        for l in range(n):
            for r in range(l, n):
                # For a after swap:
                # a[0:l] + b[l:r+1] + a[r+1:]
                # GCD of a[0:l] is prefix_gcd_a[l-1] if l > 0 else 0
                # GCD of b[l:r+1] is prefix_gcd_b[r] if l == 0 else math.gcd(suffix_gcd_b[l], prefix_gcd_b[r])
                # GCD of a[r+1:] is suffix_gcd_a[r+1] if r+1 < n else 0

                # GCD of new a:
                if l == 0 and r == n - 1:
                    # Whole array swapped
                    gcd_a = prefix_gcd_b[n - 1]
                elif l == 0:
                    # Prefix is empty
                    gcd_a = math.gcd(prefix_gcd_b[r], suffix_gcd_a[r + 1] if r + 1 < n else 0)
                elif r == n - 1:
                    # Suffix is empty
                    gcd_a = math.gcd(prefix_gcd_a[l - 1], prefix_gcd_b[r])
                else:
                    gcd_a = math.gcd(prefix_gcd_a[l - 1], math.gcd(prefix_gcd_b[r] if l == 0 else math.gcd(suffix_gcd_b[l], prefix_gcd_b[r]), suffix_gcd_a[r + 1]))

                # For b after swap:
                # b[0:l] + a[l:r+1] + b[r+1:]
                if l == 0 and r == n - 1:
                    gcd_b = prefix_gcd_a[n - 1]
                elif l == 0:
                    gcd_b = math.gcd(prefix_gcd_a[r], suffix_gcd_b[r + 1] if r + 1 < n else 0)
                elif r == n - 1:
                    gcd_b = math.gcd(prefix_gcd_b[l - 1], prefix_gcd_a[r])
                else:
                    gcd_b = math.gcd(prefix_gcd_b[l - 1], math.gcd(prefix_gcd_a[r] if l == 0 else math.gcd(suffix_gcd_a[l], prefix_gcd_a[r]), suffix_gcd_b[r + 1]))

                total = gcd_a + gcd_b
                if total > max_sum:
                    max_sum = total
                    count = 1
                elif total == max_sum:
                    count += 1

        return max_sum, count


class Main:
    """Main class for input/output and program execution."""

    @staticmethod
    def main() -> None:
        """Main entry point for the program."""
        input_stream = sys.stdin
        output_stream = sys.stdout

        readline = input_stream.readline

        t_line = readline()
        while t_line.strip() == '':
            t_line = readline()
        t = int(t_line.strip())

        solver = GCDSegmentSwapSolver()

        for _ in range(t):
            n_line = readline()
            while n_line.strip() == '':
                n_line = readline()
            n = int(n_line.strip())

            a_line = readline()
            while a_line.strip() == '':
                a_line = readline()
            a = list(map(int, a_line.strip().split()))

            b_line = readline()
            while b_line.strip() == '':
                b_line = readline()
            b = list(map(int, b_line.strip().split()))

            max_sum, count = solver.solve_case(a, b)
            print(f"{max_sum} {count}", file=output_stream)

if __name__ == "__main__":
    Main.main()
