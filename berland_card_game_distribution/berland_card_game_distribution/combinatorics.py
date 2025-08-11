## combinatorics.py

from typing import List

class Combinatorics:
    """Combinatorial utilities for factorial, inverse factorial, and nCr calculations.

    Attributes:
        max_n (int): The maximum value for which to precompute factorials.
        mod (int): The modulus for all combinatorial calculations.
        _fact (List[int]): Precomputed list of factorials modulo mod.
        _inv_fact (List[int]): Precomputed list of inverse factorials modulo mod.
    """

    def __init__(self, max_n: int = 1000, mod: int = 10**9 + 7) -> None:
        """Initializes the Combinatorics class and precomputes factorials and inverse factorials.

        Args:
            max_n (int, optional): Maximum n for which to precompute. Defaults to 1000.
            mod (int, optional): Modulus for calculations. Defaults to 10**9 + 7.
        """
        self.max_n: int = max_n
        self.mod: int = mod
        self._fact: List[int] = [1] * (self.max_n + 1)
        self._inv_fact: List[int] = [1] * (self.max_n + 1)
        self._precompute()

    def _precompute(self) -> None:
        """Precomputes factorials and inverse factorials modulo mod."""
        for i in range(1, self.max_n + 1):
            self._fact[i] = (self._fact[i - 1] * i) % self.mod
        # Compute inverse factorials using Fermat's little theorem
        self._inv_fact[self.max_n] = pow(self._fact[self.max_n], self.mod - 2, self.mod)
        for i in range(self.max_n - 1, -1, -1):
            self._inv_fact[i] = (self._inv_fact[i + 1] * (i + 1)) % self.mod

    def factorial(self, n: int) -> int:
        """Returns n! modulo mod.

        Args:
            n (int): The value to compute factorial for.

        Returns:
            int: n! % mod

        Raises:
            ValueError: If n is negative or exceeds max_n.
        """
        if n < 0 or n > self.max_n:
            raise ValueError(f"n must be in range [0, {self.max_n}]")
        return self._fact[n]

    def inv_factorial(self, n: int) -> int:
        """Returns modular inverse of n! modulo mod.

        Args:
            n (int): The value to compute inverse factorial for.

        Returns:
            int: (n!)^-1 % mod

        Raises:
            ValueError: If n is negative or exceeds max_n.
        """
        if n < 0 or n > self.max_n:
            raise ValueError(f"n must be in range [0, {self.max_n}]")
        return self._inv_fact[n]

    def nCr(self, n: int, r: int) -> int:
        """Computes n choose r modulo mod.

        Args:
            n (int): The total number of items.
            r (int): The number of items to choose.

        Returns:
            int: nCr % mod

        Raises:
            ValueError: If n or r is out of bounds.
        """
        if r < 0 or r > n or n < 0 or n > self.max_n:
            return 0
        return (self._fact[n] * self._inv_fact[r] % self.mod) * self._inv_fact[n - r] % self.mod
