## main.py

import sys
import bisect
import itertools
from typing import List, Tuple, Optional


class SubarraySumIndexer:
    """Provides efficient mapping from b's index to (l, r) in a, and subarray/range sum queries."""

    def __init__(self, a: List[int]) -> None:
        """Initializes the indexer with array a, computes prefix sums and start indices.

        Args:
            a: The input array.
        """
        self.n: int = len(a)
        self.a: List[int] = a[:]
        self.prefix: List[int] = [0] + list(itertools.accumulate(a))
        # start_indices[i] = the starting index in b for subarrays starting at a[i]
        self.start_indices: List[int] = [0]
        for i in range(self.n):
            self.start_indices.append(self.start_indices[-1] + self.n - i)
        # Now, start_indices[i] = sum_{j=0}^{i-1} (n-j)
        # start_indices[n] = total number of subarrays

    def b_index_to_lr(self, idx: int) -> Tuple[int, int]:
        """Maps index in b to (l, r) in a.

        Args:
            idx: Index in b (0-based).

        Returns:
            (l, r): The subarray in a corresponding to b[idx].

        Raises:
            IndexError: If idx is out of bounds.
        """
        if idx < 0 or idx >= self.start_indices[-1]:
            raise IndexError(f"Index {idx} out of bounds for b (length {self.start_indices[-1]})")
        # Find l such that start_indices[l] <= idx < start_indices[l+1]
        l: int = bisect.bisect_right(self.start_indices, idx) - 1
        offset: int = idx - self.start_indices[l]
        r: int = l + offset
        return (l, r)

    def subarray_sum(self, l: int, r: int) -> int:
        """Returns the sum of a[l..r] (inclusive).

        Args:
            l: Left index (inclusive).
            r: Right index (inclusive).

        Returns:
            The sum of a[l..r].

        Raises:
            IndexError: If l or r are out of bounds.
        """
        if not (0 <= l <= r < self.n):
            raise IndexError(f"Invalid subarray indices: l={l}, r={r}, n={self.n}")
        return self.prefix[r + 1] - self.prefix[l]

    def range_sum(self, l: int, r: int) -> int:
        """Returns the sum of b[l..r] (inclusive), i.e., sum of subarray sums in a.

        Args:
            l: Left index in b (inclusive).
            r: Right index in b (inclusive).

        Returns:
            The sum of b[l..r].

        Raises:
            IndexError: If l or r are out of bounds.
        """
        if not (0 <= l <= r < self.start_indices[-1]):
            raise IndexError(f"Invalid b range: l={l}, r={r}, b_len={self.start_indices[-1]}")
        # For each index in [l, r], map to (l1, r1) in a, sum a[l1..r1]
        # To optimize, process by blocks of subarrays starting at the same l1
        total: int = 0
        left: int = l
        while left <= r:
            # Find the subarray start index for left
            l1: int = bisect.bisect_right(self.start_indices, left) - 1
            # The first index in b for subarrays starting at l1
            start_b: int = self.start_indices[l1]
            # The last index in b for subarrays starting at l1
            end_b: int = self.start_indices[l1 + 1] - 1
            # The range in b we can process in this block
            block_left: int = left
            block_right: int = min(r, end_b)
            # For b[block_left..block_right], all have the same l1, r1 varies
            for idx in range(block_left, block_right + 1):
                offset: int = idx - start_b
                r1: int = l1 + offset
                total += self.subarray_sum(l1, r1)
            left = block_right + 1
        return total


class QueryProcessor:
    """Processes queries using SubarraySumIndexer."""

    def __init__(self, indexer: SubarraySumIndexer) -> None:
        """Initializes the processor with a SubarraySumIndexer.

        Args:
            indexer: The SubarraySumIndexer instance.
        """
        self.indexer: SubarraySumIndexer = indexer

    def process_queries(self, queries: List[Tuple[int, int]]) -> List[int]:
        """Processes a list of (l, r) queries on b.

        Args:
            queries: List of (l, r) tuples, 0-based indices in b.

        Returns:
            List of sums for each query.

        Raises:
            IndexError: If any query is out of bounds.
        """
        results: List[int] = []
        for l, r in queries:
            try:
                res = self.indexer.range_sum(l, r)
            except IndexError as e:
                raise IndexError(f"Query ({l}, {r}) is invalid: {e}")
            results.append(res)
        return results


class CLI:
    """Command-line interface for the subarray sum range query program."""

    def run(self) -> None:
        """Runs the CLI, reading input, processing queries, and printing results."""
        try:
            n_line: Optional[str] = sys.stdin.readline()
            if not n_line:
                print("Error: Missing input for n.", file=sys.stderr)
                return
            n: int = int(n_line.strip())
            if n <= 0:
                print("Error: n must be positive.", file=sys.stderr)
                return

            a_line: Optional[str] = sys.stdin.readline()
            if not a_line:
                print("Error: Missing input for array a.", file=sys.stderr)
                return
            a_strs: List[str] = a_line.strip().split()
            if len(a_strs) != n:
                print(f"Error: Expected {n} elements for array a, got {len(a_strs)}.", file=sys.stderr)
                return
            a: List[int] = [int(x) for x in a_strs]

            q_line: Optional[str] = sys.stdin.readline()
            if not q_line:
                print("Error: Missing input for number of queries.", file=sys.stderr)
                return
            q: int = int(q_line.strip())
            if q < 0:
                print("Error: Number of queries must be non-negative.", file=sys.stderr)
                return

            queries: List[Tuple[int, int]] = []
            for i in range(q):
                query_line: Optional[str] = sys.stdin.readline()
                if not query_line:
                    print(f"Error: Missing input for query {i + 1}.", file=sys.stderr)
                    return
                parts: List[str] = query_line.strip().split()
                if len(parts) != 2:
                    print(f"Error: Query {i + 1} must have two integers.", file=sys.stderr)
                    return
                l, r = map(int, parts)
                queries.append((l, r))

            indexer = SubarraySumIndexer(a)
            processor = QueryProcessor(indexer)
            try:
                results = processor.process_queries(queries)
            except IndexError as e:
                print(f"Error: {e}", file=sys.stderr)
                return

            for res in results:
                print(res)
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            return


if __name__ == "__main__":
    cli = CLI()
    cli.run()
