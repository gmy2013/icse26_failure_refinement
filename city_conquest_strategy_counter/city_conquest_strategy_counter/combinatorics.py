## combinatorics.py

from typing import List, Tuple

class Combinatorics:
    """Provides combinatorial utilities: modular inverse, nCr, and factorial precomputation."""

    def __init__(self, p: int) -> None:
        """
        Initialize the Combinatorics object with a given modulus.

        Args:
            p (int): The modulus for all combinatorial calculations.
        """
        self.p: int = p

    def modinv(self, a: int) -> int:
        """
        Compute the modular inverse of a modulo p using Fermat's little theorem.

        Args:
            a (int): The number to find the modular inverse of.

        Returns:
            int: The modular inverse of a modulo p.
        """
        return pow(a, self.p - 2, self.p)

    def precompute_factorials(self, up_to: int) -> Tuple[List[int], List[int]]:
        """
        Precompute factorials and inverse factorials modulo p up to a given number.

        Args:
            up_to (int): The maximum number to compute factorials for.

        Returns:
            Tuple[List[int], List[int]]: A tuple containing two lists:
                - fact: fact[i] = i! % p for i in 0..up_to
                - inv_fact: inv_fact[i] = (i!)^{-1} % p for i in 0..up_to
        """
        fact: List[int] = [1] * (up_to + 1)
        inv_fact: List[int] = [1] * (up_to + 1)

        for i in range(1, up_to + 1):
            fact[i] = (fact[i - 1] * i) % self.p

        inv_fact[up_to] = self.modinv(fact[up_to])
        for i in range(up_to - 1, -1, -1):
            inv_fact[i] = (inv_fact[i + 1] * (i + 1)) % self.p

        return fact, inv_fact

    def nCr(self, n: int, r: int, fact: List[int], inv_fact: List[int]) -> int:
        """
        Compute the binomial coefficient C(n, r) modulo p.

        Args:
            n (int): The number of items.
            r (int): The number of items to choose.
            fact (List[int]): Precomputed list of factorials modulo p.
            inv_fact (List[int]): Precomputed list of inverse factorials modulo p.

        Returns:
            int: The value of C(n, r) modulo p.
        """
        if r < 0 or r > n:
            return 0
        return (fact[n] * inv_fact[r] % self.p) * inv_fact[n - r] % self.p
