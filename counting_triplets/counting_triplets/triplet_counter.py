## triplet_counter.py

from typing import List

class TripletCounter:
    """Encapsulates the logic for counting ordered triplets (a, b, c) of positive integers
    such that ab + ac + bc <= n and a + b + c <= x.
    """

    def count_triplets(self, n: int, x: int) -> int:
        """Counts the number of ordered triplets (a, b, c) of positive integers
        such that ab + ac + bc <= n and a + b + c <= x.

        Args:
            n: The upper bound for ab + ac + bc.
            x: The upper bound for a + b + c.

        Returns:
            The number of valid ordered triplets (a, b, c).
        """
        count: int = 0
        # a, b, c >= 1, so a + b + c <= x => a <= x-2, b <= x-a-1, c <= x-a-b
        # ab + ac + bc <= n
        for a in range(1, x - 1):
            max_b: int = x - a - 1
            for b in range(1, max_b + 1):
                # For each (a, b), c >= 1, c <= x - a - b
                max_c_sum: int = x - a - b
                # ab + ac + bc <= n
                # ab + ac + bc = ab + a*c + b*c = ab + c*(a + b)
                # ab + c*(a + b) <= n
                # c*(a + b) <= n - ab
                ab: int = a * b
                ab_sum: int = a + b
                max_c_prod: int = (n - ab) // ab_sum if ab_sum > 0 else 0
                max_c: int = min(max_c_sum, max_c_prod)
                if max_c >= 1:
                    count += max_c
        return count
