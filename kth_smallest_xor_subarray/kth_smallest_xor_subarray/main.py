## main.py

import sys
import threading
from typing import List, Tuple

class KthSmallestXorSolver:
    """Solver for finding the k-th smallest minimum xor among all subarrays."""

    def solve(self, test_cases: List[Tuple[int, int, List[int]]]) -> List[int]:
        """
        For each test case, find the k-th smallest minimum xor among all subarrays of length at least 2.

        Args:
            test_cases: List of tuples (n, k, a), where
                n: int, length of array
                k: int, k-th smallest to find
                a: List[int], the array

        Returns:
            List[int]: The answer for each test case.
        """
        results: List[int] = []
        for n, k, a in test_cases:
            min_xors = self._collect_min_xors(a)
            # Find the k-th smallest
            min_xors.sort()
            if k <= len(min_xors):
                results.append(min_xors[k - 1])
            else:
                # If k is out of bounds, return -1 (problem statement may specify otherwise)
                results.append(-1)
        return results

    def _collect_min_xors(self, a: List[int]) -> List[int]:
        """
        Collect all minimum xors for all subarrays of length at least 2.

        For each pair of adjacent elements in the original array, count the number of subarrays
        where they are adjacent in the sorted subarray, and collect their xor value that many times.

        Args:
            a: List[int], the array

        Returns:
            List[int]: All minimum xors (with multiplicity) for all subarrays of length at least 2.
        """
        n: int = len(a)
        # For each adjacent pair (i, i+1), count the number of subarrays where they are adjacent in the sorted subarray
        pair_counts = self._count_adjacent_pairs(a)
        min_xors: List[int] = []
        for i, j, count in pair_counts:
            xor_val = a[i] ^ a[j]
            min_xors.extend([xor_val] * count)
        return min_xors

    def _count_adjacent_pairs(self, a: List[int]) -> List[Tuple[int, int, int]]:
        """
        For each adjacent pair (i, i+1) in the original array, count the number of subarrays
        where they are adjacent in the sorted subarray.

        This is done using a monotonic stack to find, for each element, the previous and next greater elements.

        Args:
            a: List[int], the array

        Returns:
            List[Tuple[int, int, int]]: List of (i, i+1, count) for each adjacent pair.
        """
        n: int = len(a)
        # For each position, find the left and right boundaries where a[i] is the maximum
        left: List[int] = [-1] * n
        right: List[int] = [n] * n

        # Monotonic stack for previous greater
        stack: List[int] = []
        for i in range(n):
            while stack and a[stack[-1]] < a[i]:
                stack.pop()
            if stack:
                left[i] = stack[-1]
            stack.append(i)

        # Monotonic stack for next greater
        stack.clear()
        for i in range(n - 1, -1, -1):
            while stack and a[stack[-1]] <= a[i]:
                stack.pop()
            if stack:
                right[i] = stack[-1]
            stack.append(i)

        # For each adjacent pair (i, i+1), count the number of subarrays where both are present and a[i] and a[i+1] are adjacent in the sorted subarray
        # The number of such subarrays is (i - left[i]) * (right[i+1] - (i+1))
        pair_counts: List[Tuple[int, int, int]] = []
        for i in range(n - 1):
            l = max(left[i], left[i + 1])
            r = min(right[i], right[i + 1])
            count = (i - l) * (r - (i + 1))
            if count > 0:
                pair_counts.append((i, i + 1, count))
        return pair_counts


class InputHandler:
    """Handles fast input reading."""

    @staticmethod
    def read_input() -> List[Tuple[int, int, List[int]]]:
        """
        Reads input from sys.stdin.

        Returns:
            List[Tuple[int, int, List[int]]]: List of test cases.
        """
        input_lines = sys.stdin.read().splitlines()
        test_cases: List[Tuple[int, int, List[int]]] = []
        idx: int = 0
        t: int = int(input_lines[idx])
        idx += 1
        for _ in range(t):
            n_k = input_lines[idx].split()
            n = int(n_k[0])
            k = int(n_k[1])
            idx += 1
            a = list(map(int, input_lines[idx].split()))
            idx += 1
            test_cases.append((n, k, a))
        return test_cases


class OutputHandler:
    """Handles fast output writing."""

    @staticmethod
    def write_output(results: List[int]) -> None:
        """
        Writes results to sys.stdout.

        Args:
            results: List[int], the results to write.
        """
        output = '\n'.join(map(str, results))
        sys.stdout.write(output + '\n')


def main() -> None:
    """Main function to run the program."""
    test_cases = InputHandler.read_input()
    solver = KthSmallestXorSolver()
    results = solver.solve(test_cases)
    OutputHandler.write_output(results)


if __name__ == "__main__":
    threading.Thread(target=main).start()
