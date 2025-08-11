## fibonacci_divisible.py

from typing import List
from pisano import PisanoPeriodCalculator

class FibonacciDivisibleIndexFinder:
    """Class to find indices of Fibonacci numbers divisible by k within Pisano period.

    This class uses PisanoPeriodCalculator to determine the Pisano period for a given modulus k,
    then finds all indices within one period where the Fibonacci number is divisible by k.
    It also provides a method to get the n-th such index in the infinite Fibonacci sequence.
    """

    def __init__(self, pisano_calculator: PisanoPeriodCalculator) -> None:
        """Initializes the FibonacciDivisibleIndexFinder.

        Args:
            pisano_calculator: An instance of PisanoPeriodCalculator to compute Pisano periods.
        """
        self._pisano_calculator = pisano_calculator
        self._divisible_indices_cache = {}

    def find_divisible_indices(self, k: int) -> List[int]:
        """Finds all indices within one Pisano period where Fibonacci numbers are divisible by k.

        Args:
            k: The modulus to check divisibility.

        Returns:
            A list of indices (0-based) within the Pisano period where F_i % k == 0.

        Raises:
            ValueError: If k is not a positive integer.
        """
        if k <= 0:
            raise ValueError("Modulus k must be a positive integer.")

        if k in self._divisible_indices_cache:
            return self._divisible_indices_cache[k][:]  # Return a copy

        period = self._pisano_calculator.get_pisano_period(k)
        divisible_indices = [i for i, val in enumerate(period) if val == 0]

        self._divisible_indices_cache[k] = divisible_indices
        return divisible_indices[:]

    def get_nth_divisible_index(self, n: int, k: int) -> int:
        """Returns the index in the Fibonacci sequence of the n-th Fibonacci number divisible by k.

        Args:
            n: The 1-based occurrence number (n >= 1).
            k: The modulus to check divisibility.

        Returns:
            The index (0-based) in the Fibonacci sequence of the n-th Fibonacci number divisible by k.

        Raises:
            ValueError: If n < 1 or k < 1, or if there are no divisible Fibonacci numbers for k.
        """
        if n < 1:
            raise ValueError("n must be at least 1.")
        if k < 1:
            raise ValueError("k must be at least 1.")

        divisible_indices = self.find_divisible_indices(k)
        period_length = self._pisano_calculator.get_period_length(k)

        if not divisible_indices:
            raise ValueError(f"No Fibonacci number is divisible by {k} in its Pisano period.")

        # The sequence of indices where F_i % k == 0 repeats every period_length
        # The n-th occurrence is at:
        #   period_length * (q) + divisible_indices[r]
        # where q = (n-1) // len(divisible_indices), r = (n-1) % len(divisible_indices)
        num_per_period = len(divisible_indices)
        q, r = divmod(n - 1, num_per_period)
        index = q * period_length + divisible_indices[r]
        return index
