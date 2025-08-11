## standard_binomial.py

"""Module for StandardBinomialCalculator: computes standard binomial coefficients.

Implements the StandardBinomialCalculator class, which precomputes factorials and
inverse factorials for efficient computation of standard binomial coefficients (n choose k)
modulo 10^9 + 7.

Optionally uses numpy for efficient array operations if available.
"""

from typing import List, Optional

try:
    import numpy as np
    _HAS_NUMPY = True
except ImportError:
    _HAS_NUMPY = False


class StandardBinomialCalculator:
    """Calculator for standard binomial coefficients using precomputed factorials.

    Attributes:
        mod (int): The modulus for all calculations.
        max_n (int): The maximum value of n to precompute.
        fact (List[int] or np.ndarray): Precomputed factorials.
        inv_fact (List[int] or np.ndarray): Precomputed modular inverses of factorials.
    """

    def __init__(self, max_n: int, mod: int = 10 ** 9 + 7) -> None:
        """Initializes the calculator and allocates arrays for factorials and inverses.

        Args:
            max_n (int): Maximum n to precompute.
            mod (int, optional): Modulus for calculations. Defaults to 10**9+7.
        """
        self.mod: int = mod
        self.max_n: int = max_n
        self.fact: Optional[List[int]] = None
        self.inv_fact: Optional[List[int]] = None
        self._precomputed: bool = False

    def precompute(self) -> None:
        """Precomputes factorials and inverse factorials up to max_n modulo mod."""
        n_max = self.max_n
        mod = self.mod

        if _HAS_NUMPY:
            fact = np.zeros(n_max + 1, dtype=np.int64)
            inv_fact = np.zeros(n_max + 1, dtype=np.int64)
        else:
            fact = [0] * (n_max + 1)
            inv_fact = [0] * (n_max + 1)

        # Compute factorials
        if _HAS_NUMPY:
            fact[0] = 1
            for i in range(1, n_max + 1):
                fact[i] = (fact[i - 1] * i) % mod
        else:
            fact[0] = 1
            for i in range(1, n_max + 1):
                fact[i] = (fact[i - 1] * i) % mod

        # Compute inverse factorials using Fermat's little theorem
        if _HAS_NUMPY:
            inv_fact[n_max] = pow(int(fact[n_max]), mod - 2, mod)
            for i in range(n_max, 0, -1):
                inv_fact[i - 1] = (inv_fact[i] * i) % mod
        else:
            inv_fact[n_max] = pow(fact[n_max], mod - 2, mod)
            for i in range(n_max, 0, -1):
                inv_fact[i - 1] = (inv_fact[i] * i) % mod

        self.fact = fact
        self.inv_fact = inv_fact
        self._precomputed = True

    def get(self, n: int, k: int) -> int:
        """Returns the standard binomial coefficient C(n, k) modulo mod.

        Args:
            n (int): The n parameter (row).
            k (int): The k parameter (column).

        Returns:
            int: The value of the standard binomial coefficient C(n, k) modulo mod.

        Raises:
            ValueError: If precompute() has not been called.
            IndexError: If n or k is out of precomputed bounds.
        """
        if not self._precomputed or self.fact is None or self.inv_fact is None:
            raise ValueError("Factorials not precomputed. Call precompute() first.")

        if n < 0 or k < 0 or k > n or n > self.max_n:
            return 0

        mod = self.mod
        if _HAS_NUMPY:
            res = (self.fact[n] * self.inv_fact[k]) % mod
            res = (res * self.inv_fact[n - k]) % mod
            return int(res)
        else:
            res = (self.fact[n] * self.inv_fact[k]) % mod
            res = (res * self.inv_fact[n - k]) % mod
            return res
