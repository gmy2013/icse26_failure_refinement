## ordered_pairs_calculator.py
from utils import Utils

class OrderedPairsCalculator:
    """
    Class to calculate the number of valid ordered pairs (a, b) for given constraints.
    """

    def __init__(self, n: int, m: int):
        """
        Initialize the OrderedPairsCalculator with input values n and m.

        Args:
            n (int): Upper limit for the first element of the pair.
            m (int): Upper limit for the second element of the pair.
        """
        self.n = n
        self.m = m

    def calculate_valid_pairs(self) -> int:
        """
        Calculate the number of valid ordered pairs (a, b) such that:
        1 <= a <= n, 1 <= b <= m, and gcd(a, b) == 1.

        Returns:
            int: The count of valid ordered pairs.
        """
        # Validate input values
        if not Utils.validate_input(self.n, self.m):
            raise ValueError("Invalid input values. Both n and m must be positive integers.")

        # Use Euler's totient function to optimize the calculation
        def phi(x: int) -> int:
            """
            Calculate Euler's totient function for a given integer x.

            Args:
                x (int): The input integer.

            Returns:
                int: The value of Euler's totient function for x.
            """
            result = x
            p = 2
            while p * p <= x:
                if x % p == 0:
                    while x % p == 0:
                        x //= p
                    result -= result // p
                p += 1
            if x > 1:
                result -= result // x
            return result

        # Calculate the total number of valid pairs
        valid_pairs_count = 0
        for a in range(1, self.n + 1):
            valid_pairs_count += phi(a)

        # Adjust the count based on the range of b
        return valid_pairs_count * self.m
