## pisano.py

from typing import List, Dict

class PisanoPeriodCalculator:
    """Class to compute Pisano periods for Fibonacci numbers modulo k.

    The Pisano period is the period with which the sequence of Fibonacci numbers
    taken modulo k repeats. This class provides methods to compute the Pisano period
    and its length for a given modulus k.
    """

    def __init__(self) -> None:
        """Initializes the PisanoPeriodCalculator with an internal cache."""
        self._period_cache: Dict[int, List[int]] = {}
        self._length_cache: Dict[int, int] = {}

    def get_pisano_period(self, k: int) -> List[int]:
        """Computes the Pisano period for a given modulus k.

        Args:
            k: The modulus for which to compute the Pisano period.

        Returns:
            A list of integers representing the Pisano period of Fibonacci numbers modulo k.

        Raises:
            ValueError: If k is not a positive integer.
        """
        if k <= 0:
            raise ValueError("Modulus k must be a positive integer.")

        if k in self._period_cache:
            return self._period_cache[k][:]  # Return a copy to prevent external modification

        period: List[int] = [0, 1]
        prev: int = 0
        curr: int = 1

        # The Pisano period always starts with 0, 1
        for _ in range(2, k * k + 1):  # Pisano period length is at most k*k
            next_val = (prev + curr) % k
            period.append(next_val)
            prev, curr = curr, next_val

            # Pisano period detected: 0, 1
            if prev == 0 and curr == 1:
                period = period[:-2]  # Remove the last two elements (start of new period)
                break

        self._period_cache[k] = period
        self._length_cache[k] = len(period)
        return period[:]

    def get_period_length(self, k: int) -> int:
        """Returns the length of the Pisano period for a given modulus k.

        Args:
            k: The modulus for which to compute the Pisano period length.

        Returns:
            The length of the Pisano period.

        Raises:
            ValueError: If k is not a positive integer.
        """
        if k <= 0:
            raise ValueError("Modulus k must be a positive integer.")

        if k in self._length_cache:
            return self._length_cache[k]

        # Ensure the period is computed and cached
        self.get_pisano_period(k)
        return self._length_cache[k]
