## main.py
from typing import List, Optional, Tuple
import sys
import bisect
import math

class CakeDivider:
    """Class to handle the logic for dividing the cake among three people."""

    def __init__(self) -> None:
        """Initializes the CakeDivider instance."""
        pass

    def prefix_sums(self, arr: List[int]) -> List[int]:
        """Computes prefix sums for the given array.

        Args:
            arr: List of integers.

        Returns:
            List of prefix sums, where prefix[i] = sum(arr[0:i]).
        """
        prefix = [0]
        for num in arr:
            prefix.append(prefix[-1] + num)
        return prefix

    def find_partition(
        self,
        n: int,
        a: List[int],
        b: List[int],
        c: List[int],
        min_share: int
    ) -> Optional[Tuple[int, int, int, int, int, int]]:
        """Finds a valid partition of the cake.

        Args:
            n: Number of cake pieces.
            a: Alice's valuations.
            b: Bob's valuations.
            c: Charlie's valuations.
            min_share: Minimum sum required for each person.

        Returns:
            Tuple of 1-based indices (l_a, r_a, l_b, r_b, l_c, r_c) if possible, else None.
        """
        prefix_a = self.prefix_sums(a)
        prefix_b = self.prefix_sums(b)
        prefix_c = self.prefix_sums(c)

        # For each possible end of Alice's slice
        for l_a in range(n):
            # Find minimal r_a such that Alice's sum >= min_share
            low, high = l_a + 1, n
            while low <= high:
                mid = (low + high) // 2
                sum_a = prefix_a[mid] - prefix_a[l_a]
                if sum_a >= min_share:
                    high = mid - 1
                else:
                    low = mid + 1
            r_a = low
            if r_a > n:
                continue
            sum_a = prefix_a[r_a] - prefix_a[l_a]
            if sum_a < min_share:
                continue

            # Now, Bob's slice starts at r_a, find minimal r_b such that Bob's sum >= min_share
            l_b = r_a
            if l_b >= n:
                continue
            low, high = l_b + 1, n
            while low <= high:
                mid = (low + high) // 2
                sum_b = prefix_b[mid] - prefix_b[l_b]
                if sum_b >= min_share:
                    high = mid - 1
                else:
                    low = mid + 1
            r_b = low
            if r_b > n:
                continue
            sum_b = prefix_b[r_b] - prefix_b[l_b]
            if sum_b < min_share:
                continue

            # Charlie gets the rest: from r_b to n
            l_c = r_b
            r_c = n
            if l_c >= n:
                continue
            sum_c = prefix_c[r_c] - prefix_c[l_c]
            if sum_c >= min_share:
                # Return 1-based indices as per competitive programming convention
                return (l_a + 1, r_a, l_b + 1, r_b, l_c + 1, r_c)
        return None

    def process_test_case(
        self,
        n: int,
        a: List[int],
        b: List[int],
        c: List[int]
    ) -> Optional[Tuple[int, int, int, int, int, int]]:
        """Processes a single test case.

        Args:
            n: Number of cake pieces.
            a: Alice's valuations.
            b: Bob's valuations.
            c: Charlie's valuations.

        Returns:
            Tuple of 1-based indices for the slices, or None if not possible.
        """
        tot = sum(a) + sum(b) + sum(c)
        min_share = math.ceil(tot / 3)
        return self.find_partition(n, a, b, c, min_share)


class Main:
    """Main class to handle input/output and run the program."""

    @staticmethod
    def main() -> None:
        """Reads input, processes test cases, and prints output."""
        input_lines = sys.stdin.read().splitlines()
        t = int(input_lines[0])
        idx = 1
        cake_divider = CakeDivider()
        for _ in range(t):
            n = int(input_lines[idx])
            idx += 1
            a = list(map(int, input_lines[idx].split()))
            idx += 1
            b = list(map(int, input_lines[idx].split()))
            idx += 1
            c = list(map(int, input_lines[idx].split()))
            idx += 1
            result = cake_divider.process_test_case(n, a, b, c)
            if result is None:
                print("NO")
            else:
                print(' '.join(map(str, result)))


if __name__ == "__main__":
    Main.main()
