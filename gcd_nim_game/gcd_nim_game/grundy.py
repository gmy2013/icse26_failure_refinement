## grundy.py

import numpy as np
from typing import List

class GrundyCalculator:
    """Class to precompute and provide Grundy numbers for the GCD-restricted Nim game."""

    def __init__(self, max_value: int = 10_000_000) -> None:
        """
        Initializes the GrundyCalculator and precomputes Grundy numbers up to max_value.

        Args:
            max_value (int): The maximum pile size for which to precompute Grundy numbers.
        """
        self.max_value: int = max_value
        self.grundy: np.ndarray = np.zeros(self.max_value + 1, dtype=np.int32)
        self.precompute_grundy()

    def precompute_grundy(self) -> None:
        """
        Precomputes Grundy numbers for all pile sizes up to self.max_value.

        The Grundy number for a pile of size x is the minimum excludant (mex) of the
        Grundy numbers of all positions reachable from x by removing y stones,
        where 1 <= y < x and gcd(x, y) == 1.
        """
        grundy = self.grundy
        max_value = self.max_value

        # For each pile size x, compute its Grundy number
        for x in range(1, max_value + 1):
            # To store Grundy numbers of all valid moves from x
            reachable = set()
            # For all y in 1..x-1 such that gcd(x, y) == 1
            # We can use Euler's totient function, but for generality, we check all y
            for y in range(1, x):
                if np.gcd(x, y) == 1:
                    reachable.add(grundy[x - y])
            # Compute mex (minimum excludant)
            mex = 0
            while mex in reachable:
                mex += 1
            grundy[x] = mex

    def get_grundy(self, x: int) -> int:
        """
        Returns the Grundy number for a given pile size.

        Args:
            x (int): The pile size.

        Returns:
            int: The Grundy number for the pile.
        """
        if 0 <= x <= self.max_value:
            return int(self.grundy[x])
        raise ValueError(f"Pile size {x} is out of precomputed range (0..{self.max_value})")
