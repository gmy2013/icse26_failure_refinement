## gcd_optimizer.py
import math
from typing import List, Tuple

class GCDOptimizer:
    """
    Class responsible for calculating GCD and maximizing GCD with swaps under a budget.
    """

    @staticmethod
    def calculate_gcd(arr: List[int]) -> int:
        """
        Calculates the GCD of an array of integers.

        Args:
            arr (List[int]): List of integers.

        Returns:
            int: The GCD of the array.
        """
        if not arr:
            raise ValueError("Input array must not be empty.")
        gcd_value = arr[0]
        for num in arr[1:]:
            gcd_value = math.gcd(gcd_value, num)
        return gcd_value

    @staticmethod
    def maximize_gcd(a: List[int], b: List[int], swaps: List[Tuple[int, int, int]], budget: int) -> int:
        """
        Maximizes the GCD of array A by performing swaps with array B under a budget constraint.

        Args:
            a (List[int]): Array A.
            b (List[int]): Array B.
            swaps (List[Tuple[int, int, int]]): List of tuples representing swaps.
                Each tuple contains:
                - index of element in A
                - index of element in B
                - cost of swapping these elements
            budget (int): Budget constraint for performing swaps.

        Returns:
            int: The maximum GCD achievable within the budget.
        """
        if len(a) != len(b):
            raise ValueError("Array A and Array B must have the same length.")
        if budget < 0:
            raise ValueError("Budget must be a non-negative integer.")

        # Sort swaps by cost in ascending order
        swaps = sorted(swaps, key=lambda x: x[2])

        # Initialize variables
        current_budget = budget
        max_gcd = GCDOptimizer.calculate_gcd(a)

        # Perform swaps within the budget
        for swap in swaps:
            index_a, index_b, cost = swap
            if cost <= current_budget:
                # Perform the swap
                a[index_a], b[index_b] = b[index_b], a[index_a]
                current_budget -= cost

                # Recalculate GCD after the swap
                new_gcd = GCDOptimizer.calculate_gcd(a)
                max_gcd = max(max_gcd, new_gcd)

        return max_gcd

    @staticmethod
    def log_gcd_details(a: List[int], b: List[int], swaps: List[Tuple[int, int, int]], budget: int, log_file: str = "gcd_optimizer.log") -> None:
        """
        Logs the details of the GCD optimization process to a specified log file.

        Args:
            a (List[int]): Array A.
            b (List[int]): Array B.
            swaps (List[Tuple[int, int, int]]): List of tuples representing swaps.
                Each tuple contains:
                - index of element in A
                - index of element in B
                - cost of swapping these elements
            budget (int): Budget constraint for performing swaps.
            log_file (str): Path to the log file. Defaults to "gcd_optimizer.log".

        Returns:
            None
        """
        try:
            with open(log_file, 'a') as file:
                file.write(f"Initial Array A: {a}\n")
                file.write(f"Initial Array B: {b}\n")
                file.write(f"Swaps: {swaps}\n")
                file.write(f"Budget: {budget}\n")
        except Exception as e:
            raise ValueError(f"Error writing to log file: {e}")
