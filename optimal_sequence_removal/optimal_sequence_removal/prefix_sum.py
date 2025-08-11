## prefix_sum.py

from typing import List

class PrefixSum:
    """Utility class for efficient prefix sum queries and prefix search.

    Attributes:
        _prefix (List[int]): The prefix sum array, where _prefix[i] is the sum of arr[0:i].
    """

    def __init__(self, arr: List[int]) -> None:
        """Initializes the PrefixSum object with the given array.

        Args:
            arr (List[int]): The input array for which prefix sums are computed.
        """
        n: int = len(arr)
        self._prefix: List[int] = [0] * (n + 1)
        for i in range(n):
            self._prefix[i + 1] = self._prefix[i] + arr[i]

    def sum(self, l: int, r: int) -> int:
        """Returns the sum of arr[l:r], i.e., arr[l] + arr[l+1] + ... + arr[r-1].

        Args:
            l (int): The starting index (inclusive).
            r (int): The ending index (exclusive).

        Returns:
            int: The sum of the subarray arr[l:r].
        """
        if l < 0 or r > len(self._prefix) - 1 or l > r:
            raise ValueError("Invalid indices for sum query.")
        return self._prefix[r] - self._prefix[l]

    def find_max_prefix(self, start: int, limit: int) -> int:
        """Finds the maximal end index such that sum of arr[start:end] <= limit.

        Args:
            start (int): The starting index of the prefix (inclusive).
            limit (int): The maximum allowed sum for the prefix.

        Returns:
            int: The maximal end index (exclusive) such that sum(arr[start:end]) <= limit.
                 Returns start if no prefix can be taken.
        """
        # Binary search for the largest end in [start+1, len(arr)+1] with sum <= limit
        left: int = start + 1
        right: int = len(self._prefix)
        base_sum: int = self._prefix[start]
        res: int = start
        while left < right:
            mid: int = (left + right) // 2
            if self._prefix[mid] - base_sum <= limit:
                res = mid
                left = mid + 1
            else:
                right = mid
        return res
