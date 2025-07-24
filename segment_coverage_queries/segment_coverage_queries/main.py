## main.py
from typing import List, Dict
import bisect
import sys


class SegmentCoverageSolver:
    """Solver for computing the number of integer points covered by exactly k segments."""

    def __init__(self) -> None:
        """Initializes the solver. No state is kept between test cases."""
        pass

    def process_test_case(
        self, n: int, q: int, x: List[int], ks: List[int]
    ) -> List[int]:
        """
        Processes a single test case.

        Args:
            n: Number of points (segments are between consecutive points).
            q: Number of queries.
            x: List of strictly increasing integer points.
            ks: List of query integers, each asking for the number of integer points
                covered by exactly k segments.

        Returns:
            List of answers for each query in ks.
        """
        coverage_counts = self._compute_coverage_counts(x)
        answers = []
        for k in ks:
            answers.append(coverage_counts.get(k, 0))
        return answers

    def _compute_coverage_counts(self, x: List[int]) -> Dict[int, int]:
        """
        Computes the number of integer points covered by exactly c segments,
        for all possible c.

        Args:
            x: List of strictly increasing integer points.

        Returns:
            Dictionary mapping coverage count c to the number of integer points
            covered by exactly c segments.
        """
        n = len(x)
        if n < 2:
            return {}

        # Step 1: Build events for sweep line (difference array)
        # Each segment is [x[i], x[i+1]], covers all integer points in [x[i], x[i+1]]
        # For each segment, +1 at x[i], -1 at x[i+1]+1
        events = []
        for i in range(n - 1):
            left = x[i]
            right = x[i + 1]
            # Only consider if there is at least one integer point in [left, right]
            if left > right:
                continue
            events.append((left, 1))
            events.append((right + 1, -1))

        # Step 2: Process events in order
        events.sort()
        coverage_counts: Dict[int, int] = {}
        curr_coverage = 0
        prev_pos = None

        # We need to process all integer points in the union of all segments
        # For each interval [prev_pos, pos-1], all integer points in this interval
        # have the same coverage count (curr_coverage)
        for pos, delta in events:
            if prev_pos is not None and prev_pos < pos:
                # All integer points in [prev_pos, pos-1] have curr_coverage
                count = pos - prev_pos
                if curr_coverage > 0:
                    coverage_counts[curr_coverage] = (
                        coverage_counts.get(curr_coverage, 0) + count
                    )
            curr_coverage += delta
            prev_pos = pos

        # No need to process after the last event, as segments end at x[n-1]
        return coverage_counts


class Main:
    """Main class to handle input/output and delegate to the solver."""

    @staticmethod
    def main() -> None:
        """
        Main entry point. Reads input, processes test cases, and prints answers.
        """
        solver = SegmentCoverageSolver()
        input_lines = sys.stdin.read().splitlines()
        line_idx = 0

        t = int(input_lines[line_idx].strip())
        line_idx += 1

        for _ in range(t):
            n_q = input_lines[line_idx].strip().split()
            n = int(n_q[0])
            q = int(n_q[1])
            line_idx += 1

            x = list(map(int, input_lines[line_idx].strip().split()))
            line_idx += 1

            ks = list(map(int, input_lines[line_idx].strip().split()))
            line_idx += 1

            answers = solver.process_test_case(n, q, x, ks)
            print(" ".join(map(str, answers)))


if __name__ == "__main__":
    Main.main()
