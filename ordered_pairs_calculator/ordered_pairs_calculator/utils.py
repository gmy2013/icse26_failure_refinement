## utils.py
import math

class Utils:
    """Utility class containing shared functions for the project."""

    @staticmethod
    def gcd(a: int, b: int) -> int:
        """
        Calculate the greatest common divisor (GCD) of two integers.

        Args:
            a (int): First integer.
            b (int): Second integer.

        Returns:
            int: The GCD of a and b.
        """
        return math.gcd(a, b)

    @staticmethod
    def validate_input(n: int, m: int) -> bool:
        """
        Validate the input values for n and m.

        Args:
            n (int): First input value.
            m (int): Second input value.

        Returns:
            bool: True if inputs are valid, False otherwise.
        """
        if not isinstance(n, int) or not isinstance(m, int):
            return False
        if n <= 0 or m <= 0:
            return False
        return True
