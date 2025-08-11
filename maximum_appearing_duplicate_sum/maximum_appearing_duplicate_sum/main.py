## main.py

from collections import Counter
from typing import List


class MADProcessor:
    """Processor for computing the MAD (most frequent element) for array prefixes."""

    def process_test_case(self, a: List[int]) -> int:
        """Process a single test case and return the sum of MADs for all iterations.

        Args:
            a: List[int] - The input array.

        Returns:
            int: The sum of MADs for all prefixes in all iterations.
        """
        total_sum: int = 0
        arr: List[int] = a.copy()
        while any(arr):
            mad_list: List[int] = self.mad_prefix(arr)
            total_sum += sum(mad_list)
            # Subtract MAD from each prefix
            for i in range(len(arr)):
                arr[i] = max(0, arr[i] - mad_list[i])
        return total_sum

    def mad_prefix(self, arr: List[int]) -> List[int]:
        """Compute the MAD (most frequent element) for each prefix of the array.

        Args:
            arr: List[int] - The input array.

        Returns:
            List[int]: List of MADs for each prefix.
        """
        freq_counter: Counter = Counter()
        mad_list: List[int] = []
        max_freq: int = 0
        mad_value: int = 0

        for i, val in enumerate(arr):
            freq_counter[val] += 1
            if freq_counter[val] > max_freq or (
                freq_counter[val] == max_freq and val < mad_value
            ):
                max_freq = freq_counter[val]
                mad_value = val
            mad_list.append(mad_value)
        return mad_list


class CLI:
    """Command-line interface for the MADProcessor."""

    def __init__(self) -> None:
        self.mad_processor: MADProcessor = MADProcessor()

    def run(self) -> None:
        """Run the CLI to process input and output results."""
        import sys

        input_lines = sys.stdin.read().splitlines()
        idx: int = 0
        t: int = int(input_lines[idx].strip())
        idx += 1

        for _ in range(t):
            n: int = int(input_lines[idx].strip())
            idx += 1
            a: List[int] = list(map(int, input_lines[idx].strip().split()))
            idx += 1
            result: int = self.mad_processor.process_test_case(a)
            print(result)


if __name__ == "__main__":
    cli = CLI()
    cli.run()
