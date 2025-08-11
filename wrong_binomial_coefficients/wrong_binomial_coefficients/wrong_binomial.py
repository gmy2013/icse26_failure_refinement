## wrong_binomial.py

"""Module for WrongBinomialCalculator: computes 'wrong' binomial coefficients via DP.

Implements the WrongBinomialCalculator class, which precomputes and queries
the 'wrong' binomial coefficients using a non-standard recurrence relation.
All computations are performed modulo 10^9 + 7.

Optionally uses numpy for efficient array operations if available.
"""

from typing import List, Optional

try:
    import numpy as np
    _HAS_NUMPY = True
except ImportError:
    _HAS_NUMPY = False


class WrongBinomialCalculator:
    """Calculator for 'wrong' binomial coefficients using dynamic programming.

    Attributes:
        mod (int): The modulus for all calculations.
        max_n (int): The maximum value of n to precompute.
        C (List[List[int]] or np.ndarray): DP table for wrong binomial coefficients.
    """

    def __init__(self, max_n: int, mod: int = 10 ** 9 + 7) -> None:
        """Initializes the calculator and allocates the DP table.

        Args:
            max_n (int): Maximum n to precompute.
            mod (int, optional): Modulus for calculations. Defaults to 10**9+7.
        """
        self.mod: int = mod
        self.max_n: int = max_n
        self.C: Optional[List[List[int]]] = None
        self._precomputed: bool = False

    def precompute(self) -> None:
        """Precomputes the DP table for wrong binomial coefficients up to max_n.

        The 'wrong' recurrence is:
            C[n][k] = C[n-1][k] + C[n-1][k-1] + 1
        with base cases:
            C[0][0] = 1
            C[n][0] = 1 for all n >= 0
            C[n][k] = 0 for k < 0 or k > n
        """
        n_max = self.max_n
        mod = self.mod

        if _HAS_NUMPY:
            # Use numpy for fast array operations
            C = np.zeros((n_max + 1, n_max + 1), dtype=np.int64)
        else:
            # Use standard Python lists
            C = [[0] * (n_max + 1) for _ in range(n_max + 1)]

        # Base case: C[0][0] = 1
        if _HAS_NUMPY:
            C[0, 0] = 1
        else:
            C[0][0] = 1

        # Fill DP table
        for n in range(1, n_max + 1):
            if _HAS_NUMPY:
                C[n, 0] = 1
            else:
                C[n][0] = 1
            for k in range(1, n + 1):
                if _HAS_NUMPY:
                    val = (C[n - 1, k] + C[n - 1, k - 1] + 1) % mod
                    C[n, k] = val
                else:
                    val = (C[n - 1][k] + C[n - 1][k - 1] + 1) % mod
                    C[n][k] = val

        self.C = C
        self._precomputed = True

    def get(self, n: int, k: int) -> int:
        """Returns the wrong binomial coefficient C[n][k].

        Args:
            n (int): The n parameter (row).
            k (int): The k parameter (column).

        Returns:
            int: The value of the wrong binomial coefficient C[n][k] modulo mod.

        Raises:
            ValueError: If precompute() has not been called.
            IndexError: If n or k is out of precomputed bounds.
        """
        if not self._precomputed or self.C is None:
            raise ValueError("DP table not precomputed. Call precompute() first.")

        if n < 0 or k < 0 or k > n or n > self.max_n:
            return 0

        if _HAS_NUMPY:
            return int(self.C[n, k])
        else:
            return self.C[n][k]
