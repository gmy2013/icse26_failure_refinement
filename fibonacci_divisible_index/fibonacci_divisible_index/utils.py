## utils.py

class Utils:
    """Utility class for modular arithmetic operations."""

    @staticmethod
    def modular_index(idx: int, mod: int = 10**9 + 7) -> int:
        """Returns the index modulo mod.

        Args:
            idx: The integer index to be reduced.
            mod: The modulus to use (default: 10^9 + 7).

        Returns:
            The value of idx modulo mod.

        Raises:
            ValueError: If mod is not a positive integer.
        """
        if mod <= 0:
            raise ValueError("Modulus must be a positive integer.")
        return idx % mod
