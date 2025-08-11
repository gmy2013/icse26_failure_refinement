## main.py

from typing import List


class ArrayEqualityChecker:
    """Class to check if two arrays can be made equal using allowed swap operations."""

    def check_arrays(self, n: int, a: List[int], b: List[int]) -> str:
        """Check if arrays a and b can be made equal using allowed swaps.

        Args:
            n: Length of the arrays.
            a: First array.
            b: Second array.

        Returns:
            'YES' if arrays can be made equal, 'NO' otherwise.
        """
        # Check if both arrays have the same elements
        if sorted(a) != sorted(b):
            return 'NO'

        # For odd n, check if the parity of the permutation is the same
        if n % 2 == 1:
            parity_a_to_b = self._get_parity(a, b)
            if parity_a_to_b != 0:
                return 'NO'

        return 'YES'

    def _get_parity(self, arr: List[int], target: List[int]) -> int:
        """Compute the parity of the permutation to transform arr into target.

        Args:
            arr: Source array.
            target: Target array.

        Returns:
            0 if the permutation is even, 1 if odd.
        """
        # Map value to its index in target
        value_to_index = {value: idx for idx, value in enumerate(target)}
        visited = [False] * len(arr)
        parity = 0

        for i in range(len(arr)):
            if visited[i] or value_to_index[arr[i]] == i:
                continue
            cycle_length = 0
            j = i
            while not visited[j]:
                visited[j] = True
                j = value_to_index[arr[j]]
                cycle_length += 1
            if cycle_length > 0:
                parity ^= (cycle_length + 1) % 2  # Odd-length cycle flips parity

        return parity


class Main:
    """Main class to handle input/output and test case processing."""

    def __init__(self) -> None:
        self.checker = ArrayEqualityChecker()

    def main(self) -> None:
        """Main function to process input and output results."""
        import sys

        input_lines = sys.stdin.read().splitlines()
        t = int(input_lines[0])
        idx = 1

        for _ in range(t):
            n = int(input_lines[idx])
            a = list(map(int, input_lines[idx + 1].split()))
            b = list(map(int, input_lines[idx + 2].split()))
            idx += 3

            result = self.checker.check_arrays(n, a, b)
            print(result)


if __name__ == "__main__":
    Main().main()
