## maximizer.py

from typing import List


class ArraySumMaximizer:
    """Class to maximize the sum of each prefix of an array by allowed operations.

    The allowed operation is to count all factors of 2 in the prefix,
    transfer them to the largest element, and compute the sum.
    """

    def __init__(self) -> None:
        """Initializes the ArraySumMaximizer instance."""
        pass

    def maximize_prefix_sums(self, a: List[int]) -> List[int]:
        """Maximizes the sum of each prefix of the array.

        For each prefix a[0:i+1], counts all factors of 2 in the prefix,
        transfers them to the largest element, and computes the sum.

        Args:
            a: List[int]. The input array.

        Returns:
            List[int]: The list of maximized prefix sums.
        """
        n: int = len(a)
        prefix_sums: List[int] = []
        prefix: List[int] = []
        for i in range(n):
            prefix.append(a[i])
            # Count total number of factors of 2 in the prefix
            total_twos: int = 0
            prefix_copy: List[int] = []
            for num in prefix:
                cnt: int = 0
                val: int = num
                while val % 2 == 0 and val > 0:
                    val //= 2
                    cnt += 1
                total_twos += cnt
                prefix_copy.append(val)
            # Find the index of the largest element in prefix_copy
            max_idx: int = 0
            for idx in range(1, len(prefix_copy)):
                if prefix_copy[idx] > prefix_copy[max_idx]:
                    max_idx = idx
            # Multiply the largest element by 2^total_twos
            prefix_copy[max_idx] *= (1 << total_twos)
            # Compute the sum
            prefix_sum: int = sum(prefix_copy)
            prefix_sums.append(prefix_sum)
        return prefix_sums
