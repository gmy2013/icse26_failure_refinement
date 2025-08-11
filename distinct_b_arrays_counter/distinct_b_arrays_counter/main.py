## main.py
import argparse
from typing import List, Set, Tuple, Dict

class DistinctBArraysCounter:
    """Class to count the number of distinct b arrays for surjective mappings."""

    def __init__(self, n: int, k: int) -> None:
        """
        Initialize the counter with parameters n and k.

        Args:
            n (int): Length of array a.
            k (int): Number of distinct values in [1, k].
        """
        self.n: int = n
        self.k: int = k

    def count_distinct_b_arrays(self) -> int:
        """
        Count the number of distinct b arrays generated from all surjective a arrays.

        Returns:
            int: The number of distinct b arrays.
        """
        # For small k, we can enumerate all surjective mappings and their induced b arrays.
        # For large n, use mathematical insight: the number of distinct b arrays is k! * Stirling(n, k)
        # where Stirling(n, k) is the Stirling number of the second kind.

        if self.k > self.n or self.k <= 0 or self.n <= 0:
            return 0

        stirling = self._stirling_second_kind(self.n, self.k)
        factorial = self._factorial(self.k)
        return stirling * factorial

    def _generate_b_from_a(self, a: List[int]) -> Tuple[int]:
        """
        Generate b array from a array by mapping each value in a to its rank in sorted unique values.

        Args:
            a (List[int]): The input array a.

        Returns:
            Tuple[int]: The generated b array as a tuple.
        """
        unique_sorted = sorted(set(a))
        value_to_rank: Dict[int, int] = {v: i + 1 for i, v in enumerate(unique_sorted)}
        b = tuple(value_to_rank[x] for x in a)
        return b

    def _enumerate_a_states(
        self,
        pos: int,
        used: Set[int],
        a: List[int],
        b_set: Set[Tuple[int]]
    ) -> None:
        """
        Recursively enumerate all surjective a arrays and collect their b arrays.

        Args:
            pos (int): Current position in a.
            used (Set[int]): Set of used values in a so far.
            a (List[int]): Current a array being built.
            b_set (Set[Tuple[int]]): Set to collect unique b arrays.
        """
        if pos == self.n:
            if len(used) == self.k:
                b = self._generate_b_from_a(a)
                b_set.add(b)
            return
        for v in range(1, self.k + 1):
            a.append(v)
            used_added = v not in used
            if used_added:
                used.add(v)
            self._enumerate_a_states(pos + 1, used, a, b_set)
            a.pop()
            if used_added:
                used.remove(v)

    def _stirling_second_kind(self, n: int, k: int) -> int:
        """
        Compute the Stirling number of the second kind S(n, k).

        Args:
            n (int): Number of elements.
            k (int): Number of non-empty subsets.

        Returns:
            int: S(n, k)
        """
        # Use DP: S(n, k) = k * S(n-1, k) + S(n-1, k-1)
        S = [[0] * (k + 2) for _ in range(n + 2)]
        S[0][0] = 1
        for i in range(1, n + 1):
            for j in range(1, k + 1):
                S[i][j] = j * S[i - 1][j] + S[i - 1][j - 1]
        return S[n][k]

    def _factorial(self, x: int) -> int:
        """
        Compute factorial of x.

        Args:
            x (int): The number to compute factorial for.

        Returns:
            int: x!
        """
        result = 1
        for i in range(2, x + 1):
            result *= i
        return result


class CLI:
    """Command-line interface for the DistinctBArraysCounter."""

    def parse_args(self) -> Tuple[int, int]:
        """
        Parse command-line arguments for n and k.

        Returns:
            Tuple[int, int]: Parsed n and k values.
        """
        parser = argparse.ArgumentParser(
            description="Count the number of distinct b arrays for surjective mappings from [1, n] to [1, k]."
        )
        parser.add_argument(
            "--n",
            type=int,
            default=3,
            help="Length of array a (default: 3)"
        )
        parser.add_argument(
            "--k",
            type=int,
            default=2,
            help="Number of distinct values in [1, k] (default: 2)"
        )
        args = parser.parse_args()
        return args.n, args.k

    def run(self) -> None:
        """
        Run the command-line interface.
        """
        n, k = self.parse_args()
        counter = DistinctBArraysCounter(n, k)
        result = counter.count_distinct_b_arrays()
        print(f"Number of distinct b arrays for n={n}, k={k}: {result}")


if __name__ == "__main__":
    cli = CLI()
    cli.run()
