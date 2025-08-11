## road_leveling.py

from typing import List, Tuple, Optional


class RoadLeveling:
    """Handles efficient range queries for road leveling problem.

    Attributes:
        n (int): Number of road sections.
        a (List[int]): List of sand surplus/deficit for each section.
        prefix_sum (List[int]): Prefix sum array of a.
        min_prefix (List[int]): Minimum prefix sum up to each index.
        max_prefix (List[int]): Maximum prefix sum up to each index.
    """

    def __init__(self, a: List[int]) -> None:
        """Initializes the RoadLeveling object with the given sand array.

        Args:
            a (List[int]): List of sand surplus/deficit for each section.
        """
        self.n: int = len(a)
        self.a: List[int] = a
        self.prefix_sum: List[int] = self._compute_prefix_sum(a)
        self.min_prefix: List[int] = self._compute_min_prefix(self.prefix_sum)
        self.max_prefix: List[int] = self._compute_max_prefix(self.prefix_sum)

    def _compute_prefix_sum(self, a: List[int]) -> List[int]:
        """Computes prefix sum array.

        Args:
            a (List[int]): Input array.

        Returns:
            List[int]: Prefix sum array.
        """
        prefix_sum: List[int] = [0] * (self.n + 1)
        for i in range(self.n):
            prefix_sum[i + 1] = prefix_sum[i] + a[i]
        return prefix_sum

    def _compute_min_prefix(self, prefix_sum: List[int]) -> List[int]:
        """Computes minimum prefix sum up to each index.

        Args:
            prefix_sum (List[int]): Prefix sum array.

        Returns:
            List[int]: Minimum prefix sum up to each index.
        """
        min_prefix: List[int] = [0] * (self.n + 1)
        min_prefix[0] = prefix_sum[0]
        for i in range(1, self.n + 1):
            min_prefix[i] = min(min_prefix[i - 1], prefix_sum[i])
        return min_prefix

    def _compute_max_prefix(self, prefix_sum: List[int]) -> List[int]:
        """Computes maximum prefix sum up to each index.

        Args:
            prefix_sum (List[int]): Prefix sum array.

        Returns:
            List[int]: Maximum prefix sum up to each index.
        """
        max_prefix: List[int] = [0] * (self.n + 1)
        max_prefix[0] = prefix_sum[0]
        for i in range(1, self.n + 1):
            max_prefix[i] = max(max_prefix[i - 1], prefix_sum[i])
        return max_prefix

    def query(self, l: int, r: int) -> int:
        """Processes a single query for segment [l, r].

        Args:
            l (int): Left index (0-based, inclusive).
            r (int): Right index (0-based, inclusive).

        Returns:
            int: Minimum time to level the segment, or -1 if impossible.
        """
        # The sum of a[l:r+1] must be zero for leveling to be possible.
        total: int = self.prefix_sum[r + 1] - self.prefix_sum[l]
        if total != 0:
            return -1

        # The minimum time is the maximum absolute value of the prefix sum
        # difference within the segment.
        # We need to find the max and min of prefix_sum[i] for i in [l, r+1]
        segment_prefix: List[int] = self.prefix_sum[l:r + 2]
        min_in_segment: int = min(segment_prefix)
        max_in_segment: int = max(segment_prefix)
        min_time: int = max_in_segment - min_in_segment
        return min_time


class RoadLevelingSystem:
    """Manages multiple test cases and handles input/output for road leveling."""

    def __init__(self) -> None:
        """Initializes the RoadLevelingSystem."""
        self.test_cases: List[Tuple[int, int, List[int], List[Tuple[int, int]]]] = []

    def load_input(self, input_data: str) -> None:
        """Parses input data and stores test cases.

        Args:
            input_data (str): Raw input data as a string.
        """
        lines: List[str] = input_data.strip().split('\n')
        idx: int = 0
        t: int = int(lines[idx])
        idx += 1
        for _ in range(t):
            n_q: List[int] = list(map(int, lines[idx].split()))
            n: int = n_q[0]
            q: int = n_q[1]
            idx += 1
            a: List[int] = list(map(int, lines[idx].split()))
            idx += 1
            queries: List[Tuple[int, int]] = []
            for _ in range(q):
                l_r: List[int] = list(map(int, lines[idx].split()))
                l: int = l_r[0] - 1  # Convert to 0-based index
                r: int = l_r[1] - 1  # Convert to 0-based index
                queries.append((l, r))
                idx += 1
            self.test_cases.append((n, q, a, queries))

    def process(self) -> List[List[int]]:
        """Processes all test cases and queries.

        Returns:
            List[List[int]]: Results for each test case.
        """
        results: List[List[int]] = []
        for n, q, a, queries in self.test_cases:
            road_leveling: RoadLeveling = RoadLeveling(a)
            case_result: List[int] = []
            for l, r in queries:
                res: int = road_leveling.query(l, r)
                case_result.append(res)
            results.append(case_result)
        return results

    def output(self, results: List[List[int]]) -> None:
        """Formats and prints results to stdout.

        Args:
            results (List[List[int]]): Results for each test case.
        """
        for case_result in results:
            for res in case_result:
                print(res)
