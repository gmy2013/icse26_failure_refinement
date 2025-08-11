## main.py

import sys
import math
from typing import List, Tuple


class InputHandler:
    """Class responsible for reading input from stdin."""

    @staticmethod
    def read_input() -> Tuple[int, List[List[int]]]:
        """
        Reads the number of test cases and the test case arrays from stdin.

        Returns:
            Tuple[int, List[List[int]]]: Number of test cases and list of test case arrays.
        """
        input_lines = sys.stdin.read().splitlines()
        t = int(input_lines[0])
        test_cases = []
        idx = 1
        for _ in range(t):
            n = int(input_lines[idx])
            arr = list(map(int, input_lines[idx + 1].split()))
            test_cases.append(arr)
            idx += 2
        return t, test_cases


class GCDSumMinimizer:
    """Class to minimize the sum of GCDs of array prefixes after optimal rearrangement."""

    @staticmethod
    def minimize_gcd_sum(arr: List[int]) -> int:
        """
        Rearranges the array to minimize the sum of GCDs of all prefixes.

        Args:
            arr (List[int]): The input array.

        Returns:
            int: The minimal possible sum of GCDs of all prefixes.
        """
        n = len(arr)
        used = [False] * n
        result_sum = 0

        # Start with the smallest element
        min_idx = 0
        for i in range(1, n):
            if arr[i] < arr[min_idx]:
                min_idx = i
        current_gcd = arr[min_idx]
        used[min_idx] = True
        result_sum += current_gcd

        for _ in range(1, n):
            min_next_gcd = None
            min_idx_next = -1
            for i in range(n):
                if not used[i]:
                    next_gcd = math.gcd(current_gcd, arr[i])
                    if (min_next_gcd is None) or (next_gcd < min_next_gcd):
                        min_next_gcd = next_gcd
                        min_idx_next = i
            used[min_idx_next] = True
            current_gcd = min_next_gcd
            result_sum += current_gcd

        return result_sum


class OutputHandler:
    """Class responsible for writing output to stdout."""

    @staticmethod
    def write_output(results: List[int]) -> None:
        """
        Writes the results to stdout, one per line.

        Args:
            results (List[int]): List of results to output.
        """
        for res in results:
            print(res)


class Main:
    """Main class to orchestrate the program flow."""

    @staticmethod
    def main() -> None:
        """
        Main function to run the program.
        """
        t, test_cases = InputHandler.read_input()
        results: List[int] = []
        for arr in test_cases:
            result = GCDSumMinimizer.minimize_gcd_sum(arr)
            results.append(result)
        OutputHandler.write_output(results)


if __name__ == "__main__":
    Main.main()
