## sequence_remover.py

from typing import List, Tuple, Optional
from prefix_sum import PrefixSum

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
