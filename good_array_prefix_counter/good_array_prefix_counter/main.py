## main.py

from typing import List


class GoodArrayPrefixCounter:
    """Encapsulates the logic for counting good prefixes in an array."""

    def count_good_prefixes(self, arr: List[int]) -> int:
        """Counts the number of prefixes where some element equals the sum of the rest.

        A prefix is 'good' if there exists an element x in the prefix such that
        x == (sum of the prefix) - x, i.e., x == (sum of the prefix) / 2 and the sum is even.

        Args:
            arr: List[int] - The input array.

        Returns:
            int: The number of good prefixes.
        """
        good_prefix_count: int = 0
        prefix_sum: int = 0
        seen_elements: set[int] = set()

        for idx, num in enumerate(arr):
            prefix_sum += num
            seen_elements.add(num)
            # Only check if prefix_sum is even
            if prefix_sum % 2 == 0:
                half_sum = prefix_sum // 2
                if half_sum in seen_elements:
                    good_prefix_count += 1
        return good_prefix_count


class Main:
    """Handles user interaction and orchestrates the program flow."""

    def __init__(self) -> None:
        self.counter = GoodArrayPrefixCounter()

    def run(self) -> None:
        """Runs the main program loop, handling input and output."""
        try:
            t = int(input("Enter number of test cases: ").strip())
        except ValueError:
            print("Invalid input. Please enter an integer for the number of test cases.")
            return

        for case_num in range(1, t + 1):
            try:
                n = int(input(f"Test case {case_num}: Enter array length: ").strip())
                arr_str = input(f"Test case {case_num}: Enter array elements (space-separated): ").strip()
                arr = [int(x) for x in arr_str.split()]
                if len(arr) != n:
                    print(f"Error: Expected {n} elements, got {len(arr)}. Skipping this test case.")
                    continue
            except ValueError:
                print("Invalid input. Please enter integers only. Skipping this test case.")
                continue

            result = self.counter.count_good_prefixes(arr)
            print(f"Test case {case_num}: Number of good prefixes = {result}")


if __name__ == "__main__":
    main = Main()
    main.run()
