## main.py

from typing import List, Dict


class BracketSequenceSolver:
    """Solver for counting valid bracket substring inversions."""

    def solve(self, test_cases: List[str]) -> List[int]:
        """Solves all test cases.

        Args:
            test_cases: List of bracket sequences as strings.

        Returns:
            List of integers, each representing the answer for a test case.
        """
        results: List[int] = []
        for s in test_cases:
            result = self._count_valid_pairs(s)
            results.append(result)
        return results

    def _count_valid_pairs(self, s: str) -> int:
        """Counts the number of valid (l, r) pairs for a given bracket sequence.

        Args:
            s: The bracket sequence string.

        Returns:
            The number of valid pairs (l, r) such that inverting s[l..r] keeps the sequence regular.
        """
        n: int = len(s)
        prefix_sum: List[int] = [0] * (n + 1)
        for i in range(n):
            if s[i] == '(':
                prefix_sum[i + 1] = prefix_sum[i] + 1
            else:
                prefix_sum[i + 1] = prefix_sum[i] - 1

        # Precompute minimum prefix sums for each position
        min_prefix: List[int] = [0] * (n + 1)
        min_prefix[0] = prefix_sum[0]
        for i in range(1, n + 1):
            min_prefix[i] = min(min_prefix[i - 1], prefix_sum[i])

        # Precompute minimum suffix sums for each position
        min_suffix: List[int] = [0] * (n + 2)
        min_suffix[n + 1] = float('inf')
        for i in range(n, -1, -1):
            min_suffix[i] = min(prefix_sum[i], min_suffix[i + 1])

        # Map from prefix sum value to list of positions
        prefix_indices: Dict[int, List[int]] = {}
        for idx, val in enumerate(prefix_sum):
            if val not in prefix_indices:
                prefix_indices[val] = []
            prefix_indices[val].append(idx)

        answer: int = 0
        # For each possible pair (l, r) with even length and balance zero
        # We can fix l, and for each r > l, prefix_sum[r] == prefix_sum[l]
        # We need to check that inverting s[l:r] does not make any prefix negative
        # and the overall sequence remains regular

        # For each possible prefix sum value, process all pairs of indices
        for val, indices in prefix_indices.items():
            m = len(indices)
            # For each pair of indices (i, j) with i < j
            # s[i:j] is a candidate substring
            # We need to check:
            #   - min_prefix[j] - prefix_sum[i] >= 0 (no negative prefix in [i, j])
            #   - min_suffix[j] - (prefix_sum[i] - (prefix_sum[j] - prefix_sum[i])) >= 0
            #     (no negative prefix after inversion)
            #   - The length is even (since only then can the balance be zero)
            for idx1 in range(m):
                i = indices[idx1]
                # Use binary search to find all j > i
                for idx2 in range(idx1 + 1, m):
                    j = indices[idx2]
                    if (j - i) % 2 != 0:
                        continue  # Only even length substrings
                    # Check if inverting s[i:j] keeps the sequence regular
                    # After inversion, the prefix sum in [i+1, j] is flipped
                    # The minimum prefix in [i+1, j] before inversion is:
                    min_in_range = min_prefix[j] - prefix_sum[i]
                    if min_in_range < 0:
                        continue
                    # After inversion, the minimum suffix from j to end is:
                    # The new prefix sum at position j is prefix_sum[i]
                    # The difference in prefix sum is delta = prefix_sum[j] - prefix_sum[i]
                    # After inversion, the suffix from j onwards is shifted by -2*delta
                    delta = prefix_sum[j] - prefix_sum[i]
                    min_suf = min_suffix[j] - (prefix_sum[j] - 2 * delta)
                    if min_suf < 0:
                        continue
                    answer += 1
        return answer


class Main:
    """Main class for handling input/output and invoking the solver."""

    @staticmethod
    def main() -> None:
        """Reads input, processes test cases, and prints results."""
        import sys

        input_lines = sys.stdin.read().splitlines()
        t: int = int(input_lines[0])
        test_cases: List[str] = input_lines[1:1 + t]

        solver = BracketSequenceSolver()
        results: List[int] = solver.solve(test_cases)
        for res in results:
            print(res)


if __name__ == "__main__":
    Main.main()
