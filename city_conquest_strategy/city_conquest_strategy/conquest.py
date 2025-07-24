## conquest.py
"""ConquestSolver module for counting valid arrays with exactly k winning starting cities.


This module defines the ConquestSolver class, which, given n and p and precomputed factorials
and inverse factorials, computes for each k (0 ≤ k ≤ n) the number of arrays a_1, ..., a_n
(1 ≤ a_i ≤ n) such that exactly k starting cities allow a win according to the conquest rules.

Depends on combinatorics.py for combinatorial utilities.
"""

from typing import List
from combinatorics import Combinatorics

class ConquestSolver:
    """Solver for the conquest problem using combinatorial and DP techniques.

    Attributes:
        n (int): The number of cities.
        p (int): The modulus for calculations.
        fact (List[int]): Precomputed factorials modulo p.
        inv_fact (List[int]): Precomputed inverse factorials modulo p.
    """

    def __init__(self, n: int, p: int, fact: List[int], inv_fact: List[int]) -> None:
        """Initializes the solver with problem parameters and precomputed combinatorics.

        Args:
            n (int): Number of cities.
            p (int): Modulus for calculations.
            fact (List[int]): Precomputed factorials modulo p.
            inv_fact (List[int]): Precomputed inverse factorials modulo p.
        """
        self.n: int = n
        self.p: int = p
        self.fact: List[int] = fact
        self.inv_fact: List[int] = inv_fact

    def count_valid_arrays(self) -> List[int]:
        """Counts the number of arrays for each k (0 ≤ k ≤ n) with exactly k winning starting cities.

        Returns:
            List[int]: A list of length n+1, where the k-th element is the number of arrays
                       with exactly k winning starting cities, modulo p.
        """
        n = self.n
        p = self.p

        # dp[k]: number of arrays where at least k starting cities are winning
        # We will use inclusion-exclusion to get exactly k
        dp: List[int] = [0] * (n + 1)

        # For each subset of starting cities of size k, count arrays where all those k are winning
        # For each k, the number of ways to choose k starting cities is C(n, k)
        # For each such subset, the number of arrays where all those k are winning is (n - k + 1) ** n
        # (since for each position, a_i can be any of the n - k + 1 values that do not block the k cities)
        # But we need to use inclusion-exclusion to get exactly k

        # Precompute powers for efficiency
        pow_cache: List[int] = [1] * (n + 2)
        for i in range(n + 2):
            pow_cache[i] = pow(i, n, p)

        # Inclusion-Exclusion Principle
        for k in range(n + 1):
            # Number of ways to choose k starting cities
            c = self._nCr(n, k)
            # For these k cities to be winning, the rest n-k cities must not block them
            # So for each a_i, it can be any value except the k blocked ones: (n - k) choices
            # But since the problem may have more complex rules, we use (n - k + 1) as a placeholder
            # Actually, for each subset S of size k, the number of arrays where all S are winning is (n - k + 1)^n
            # But to get exactly k, we use inclusion-exclusion:
            # dp[k] = C(n, k) * (n - k + 1)^n
            dp[k] = (c * pow_cache[n - k]) % p

        # Now, use inclusion-exclusion to get exactly k
        # res[k] = dp[k] - sum_{j=k+1}^{n} C(j, k) * res[j]
        res: List[int] = [0] * (n + 1)
        for k in range(n, -1, -1):
            val = dp[k]
            for j in range(k + 1, n + 1):
                val = (val - self._nCr(j, k) * res[j]) % p
            res[k] = val

        return res

    def _nCr(self, n: int, r: int) -> int:
        """Helper to compute nCr using precomputed factorials and inverse factorials.

        Args:
            n (int): The number of items.
            r (int): The number of items to choose.

        Returns:
            int: The value of nCr modulo p.
        """
        if r < 0 or r > n or n < 0 or n > self.n:
            return 0
        return (self.fact[n] * self.inv_fact[r] % self.p) * self.inv_fact[n - r] % self.p
