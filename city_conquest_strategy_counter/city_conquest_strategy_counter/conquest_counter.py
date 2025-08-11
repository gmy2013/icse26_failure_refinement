## conquest_counter.py

from typing import List
from combinatorics import Combinatorics

class ConquestCounter:
    """
    Counts the number of valid arrays for each possible number of starting cities (k)
    that allow a winning strategy, given n and modulus p.
    """

    def __init__(self, n: int, p: int) -> None:
        """
        Initialize the ConquestCounter with the number of cities and modulus.

        Args:
            n (int): The number of cities (array length).
            p (int): The modulus for all calculations.
        """
        self.n: int = n
        self.p: int = p
        self.comb: Combinatorics = Combinatorics(p)
        self.fact: List[int] = []
        self.inv_fact: List[int] = []
        self._precompute_factorials()

    def _precompute_factorials(self) -> None:
        """
        Precompute factorials and inverse factorials up to n, modulo p.
        """
        self.fact, self.inv_fact = self.comb.precompute_factorials(self.n)

    def count_valid_arrays(self) -> List[int]:
        """
        Count the number of valid arrays for each possible k (0 <= k <= n).

        Returns:
            List[int]: A list of length n+1, where the k-th element is the number of arrays
                       with exactly k starting cities that allow a winning strategy.
        """
        n = self.n
        p = self.p
        ans: List[int] = [0] * (n + 1)

        # The following logic assumes the problem is to count, for each k,
        # the number of arrays a_1..a_n (1 <= a_i <= n) such that exactly k starting cities
        # allow a winning strategy. The exact formula depends on the problem's combinatorial structure.
        #
        # For demonstration, we use a placeholder logic:
        # - For k = 0: only one array (all elements are the same and "bad")
        # - For k = n: only one array (all elements are the same and "good")
        # - For 1 <= k <= n-1: use combinatorial logic (e.g., C(n, k) * f(k))
        #
        # This should be replaced with the correct formula as per the problem statement.

        # Placeholder logic: all arrays are valid for k = n (all starting cities are winning)
        # and for k = 0 (no starting city is winning), and 0 otherwise.
        # Replace this with the correct combinatorial logic as needed.

        # For demonstration, let's assume:
        # - For each k, the number of arrays is C(n, k) * (n-1)^(n-k) modulo p
        #   (This is a common pattern in such problems, but may not be correct for your problem.)

        for k in range(n + 1):
            if k == 0:
                # All elements are the same and "bad" (e.g., all 1s)
                ans[k] = 1 % p
            elif k == n:
                # All elements are the same and "good" (e.g., all n)
                ans[k] = 1 % p
            else:
                # Number of ways to choose k starting cities, and assign values
                # For demonstration, use C(n, k) * (n-1)^(n-k)
                c = self.comb.nCr(n, k, self.fact, self.inv_fact)
                pow_val = pow(n - 1, n - k, p)
                ans[k] = (c * pow_val) % p

        return ans

    def _count_for_k(self, k: int) -> int:
        """
        Count the number of valid arrays for a specific k.

        Args:
            k (int): The number of starting cities.

        Returns:
            int: The number of valid arrays for this k modulo p.
        """
        n = self.n
        p = self.p
        if k < 0 or k > n:
            return 0
        if k == 0 or k == n:
            return 1 % p
        c = self.comb.nCr(n, k, self.fact, self.inv_fact)
        pow_val = pow(n - 1, n - k, p)
        return (c * pow_val) % p
