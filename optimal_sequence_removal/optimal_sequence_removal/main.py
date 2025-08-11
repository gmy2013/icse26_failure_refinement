## main.py

from typing import List, Tuple, Union, Optional
import sys

class PrefixSum:
    """Utility class for efficient prefix sum queries and prefix search.

    Attributes:
        _prefix (List[int]): The prefix sum array, where _prefix[i] is the sum of arr[0:i].
    """

    def __init__(self, arr: List[int]) -> None:
        """Initializes the PrefixSum object with the given array.

        Args:
            arr (List[int]): The input array for which prefix sums are computed.
        """
        n: int = len(arr)
        self._prefix: List[int] = [0] * (n + 1)
        for i in range(n):
            self._prefix[i + 1] = self._prefix[i] + arr[i]

    def sum(self, l: int, r: int) -> int:
        """Returns the sum of arr[l:r], i.e., arr[l] + arr[l+1] + ... + arr[r-1].

        Args:
            l (int): The starting index (inclusive).
            r (int): The ending index (exclusive).

        Returns:
            int: The sum of the subarray arr[l:r].
        """
        if l < 0 or r > len(self._prefix) - 1 or l > r:
            raise ValueError("Invalid indices for sum query.")
        return self._prefix[r] - self._prefix[l]

    def find_max_prefix(self, start: int, limit: int) -> int:
        """Finds the maximal end index such that sum of arr[start:end] <= limit.

        Args:
            start (int): The starting index of the prefix (inclusive).
            limit (int): The maximum allowed sum for the prefix.

        Returns:
            int: The maximal end index (exclusive) such that sum(arr[start:end]) <= limit.
                 Returns start if no prefix can be taken.
        """
        left: int = start + 1
        right: int = len(self._prefix)
        base_sum: int = self._prefix[start]
        res: int = start
        while left < right:
            mid: int = (left + right) // 2
            if self._prefix[mid] - base_sum <= limit:
                res = mid
                left = mid + 1
            else:
                right = mid
        return res

class SequenceRemover:
    """Implements DP logic to compute minimum cost and number of optimal sequences.

    Attributes:
        a (List[int]): The array to be removed.
        b (List[int]): The array of prefix sum limits.
        n (int): Length of array a.
        m (int): Length of array b.
        prefix_sum (PrefixSum): Utility for prefix sum and prefix search.
        MOD (int): Modulo for counting number of ways.
    """

    def __init__(self, a: List[int], b: List[int]) -> None:
        """Initializes the SequenceRemover with arrays a and b.

        Args:
            a (List[int]): The array to be removed.
            b (List[int]): The array of prefix sum limits.
        """
        self.a: List[int] = a
        self.b: List[int] = b
        self.n: int = len(a)
        self.m: int = len(b)
        self.prefix_sum: PrefixSum = PrefixSum(a)
        self.MOD: int = 10 ** 9 + 7

    def min_cost_and_count(self) -> Tuple[int, int]:
        """Computes the minimum cost and number of optimal sequences.

        Returns:
            Tuple[int, int]: (minimum cost, number of optimal sequences)
                             If impossible, returns (-1, 0).
        """
        # dp[i][k] = (min_cost, count)
        # i: current position in a (0..n)
        # k: current index in b (1..m)
        # Only need two rows: current and next
        INF: int = 1 << 60

        # Initialize DP tables
        curr_cost: List[int] = [INF] * (self.m + 2)
        curr_count: List[int] = [0] * (self.m + 2)
        next_cost: List[int] = [INF] * (self.m + 2)
        next_count: List[int] = [0] * (self.m + 2)

        # Base case: at position n (all removed), cost 0, 1 way
        for k in range(1, self.m + 2):
            curr_cost[k] = 0
            curr_count[k] = 1

        # Process from n-1 down to 0
        for i in range(self.n - 1, -1, -1):
            # Swap current and next
            curr_cost, next_cost = next_cost, curr_cost
            curr_count, next_count = next_count, curr_count
            # Reset current row
            for k in range(1, self.m + 2):
                curr_cost[k] = INF
                curr_count[k] = 0

            for k in range(1, self.m + 1):
                # Option 1: Increment k (if k < m)
                if k + 1 <= self.m:
                    cost_inc = 1 + next_cost[k + 1]
                    if cost_inc < curr_cost[k]:
                        curr_cost[k] = cost_inc
                        curr_count[k] = next_count[k + 1]
                    elif cost_inc == curr_cost[k]:
                        curr_count[k] = (curr_count[k] + next_count[k + 1]) % self.MOD

                # Option 2: Remove prefix (if possible)
                max_end = self.prefix_sum.find_max_prefix(i, self.b[k - 1])
                if max_end > i:
                    cost_rem = 1 + next_cost[k]
                    if cost_rem < curr_cost[k]:
                        curr_cost[k] = cost_rem
                        curr_count[k] = next_count[k]
                    elif cost_rem == curr_cost[k]:
                        curr_count[k] = (curr_count[k] + next_count[k]) % self.MOD

        min_cost: int = curr_cost[1]
        count: int = curr_count[1]
        if min_cost >= INF:
            return -1, 0
        return min_cost, count

class Main:
    """Main class for orchestrating input, processing, and output."""

    @staticmethod
    def read_input() -> Tuple[int, List[Tuple[List[int], List[int]]]]:
        """Reads input from stdin.

        Returns:
            Tuple[int, List[Tuple[List[int], List[int]]]]: Number of test cases and list of (a, b) pairs.
        """
        input_lines: List[str] = []
        for line in sys.stdin:
            if line.strip() == '':
                continue
            input_lines.append(line.strip())
        ptr: int = 0
        t: int = int(input_lines[ptr])
        ptr += 1
        cases: List[Tuple[List[int], List[int]]] = []
        for _ in range(t):
            n, m = map(int, input_lines[ptr].split())
            ptr += 1
            a = list(map(int, input_lines[ptr].split()))
            ptr += 1
            b = list(map(int, input_lines[ptr].split()))
            ptr += 1
            cases.append((a, b))
        return t, cases

    @staticmethod
    def process_cases(cases: List[Tuple[List[int], List[int]]]) -> List[Union[int, Tuple[int, int]]]:
        """Processes all test cases.

        Args:
            cases (List[Tuple[List[int], List[int]]]): List of (a, b) pairs.

        Returns:
            List[Union[int, Tuple[int, int]]]: List of results for each case.
        """
        results: List[Union[int, Tuple[int, int]]] = []
        for a, b in cases:
            remover = SequenceRemover(a, b)
            min_cost, count = remover.min_cost_and_count()
            if min_cost == -1:
                results.append(-1)
            else:
                results.append((min_cost, count))
        return results

    @staticmethod
    def print_output(results: List[Union[int, Tuple[int, int]]]) -> None:
        """Prints the results to stdout.

        Args:
            results (List[Union[int, Tuple[int, int]]]): Results to print.
        """
        for res in results:
            if isinstance(res, int):
                print(res)
            else:
                print(f"{res[0]} {res[1]}")

if __name__ == "__main__":
    t, cases = Main.read_input()
    results = Main.process_cases(cases)
    Main.print_output(results)
