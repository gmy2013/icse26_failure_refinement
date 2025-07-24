## combinatorics.py
"""Combinatorics module for precomputing factorials and inverse factorials modulo p.

This module provides the Combinatorics class, which precomputes factorials and inverse factorials
up to a specified maximum n, modulo a given prime p. It provides efficient computation of nCr,
as well as accessors for the precomputed factorial and inverse factorial arrays.

No external dependencies are required; only Python standard library is used.
"""


from typing import List

class Combinatorics:
    """Combinatorics utility for modular combinatorial calculations.

    Attributes:
        p (int): The modulus (should be a prime number).
        max_n (int): The maximum n for which factorials are precomputed.
        fact (List[int]): List of factorials modulo p.
        inv_fact (List[int]): List of inverse factorials modulo p.
    """

    def __init__(self, max_n: int = 100000, p: int = 10**9 + 7) -> None:
        """Initializes the combinatorics utility and precomputes factorials and inverse factorials.

        Args:
            max_n (int, optional): Maximum n for precomputation. Defaults to 100000.
            p (int, optional): Modulus (should be prime). Defaults to 10**9 + 7.
        """
        self.p: int = p
        self.max_n: int = max_n
        self.fact: List[int] = [1] * (self.max_n + 1)
        self.inv_fact: List[int] = [1] * (self.max_n + 1)
        self.precompute()

    def precompute(self) -> None:
        """Precomputes factorials and inverse factorials modulo p up to max_n."""
        for i in range(1, self.max_n + 1):
            self.fact[i] = (self.fact[i - 1] * i) % self.p
        # Compute inverse of factorial[max_n] using Fermat's little theorem
        self.inv_fact[self.max_n] = pow(self.fact[self.max_n], self.p - 2, self.p)
        for i in range(self.max_n, 0, -1):
            self.inv_fact[i - 1] = (self.inv_fact[i] * i) % self.p

    def nCr(self, n: int, r: int) -> int:
        """Computes n choose r modulo p.

        Args:
            n (int): The number of items.
            r (int): The number of items to choose.

        Returns:
            int: The value of nCr modulo p. Returns 0 if r < 0 or r > n.
        """
        if r < 0 or r > n or n < 0 or n > self.max_n:
            return 0
        return (self.fact[n] * self.inv_fact[r] % self.p) * self.inv_fact[n - r] % self.p

    def get_fact(self) -> List[int]:
        """Returns the list of precomputed factorials modulo p.

        Returns:
            List[int]: The list of factorials.
        """
        return self.fact

    def get_inv_fact(self) -> List[int]:
        """Returns the list of precomputed inverse factorials modulo p.

        Returns:
            List[int]: The list of inverse factorials.
        """
        return self.inv_fact
