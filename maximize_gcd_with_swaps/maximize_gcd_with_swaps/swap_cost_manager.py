## swap_cost_manager.py
from typing import List, Tuple

class SwapCostManager:
    """
    Class responsible for managing swap costs and filtering swaps based on budget constraints.
    """

    @staticmethod
    def calculate_swap_costs(a: List[int], b: List[int], c: List[int]) -> List[Tuple[int, int, int]]:
        """
        Calculates the swap costs between elements of arrays A and B.

        Args:
            a (List[int]): Array A.
            b (List[int]): Array B.
            c (List[int]): Array of swap costs corresponding to elements in A and B.

        Returns:
            List[Tuple[int, int, int]]: List of tuples representing swaps.
                Each tuple contains:
                - index of element in A
                - index of element in B
                - cost of swapping these elements
        """
        if len(a) != len(b) or len(a) != len(c):
            raise ValueError("Arrays A, B, and C must have the same length.")

        swaps = []
        for i in range(len(a)):
            swaps.append((i, i, c[i]))  # Assuming swaps are between corresponding indices in A and B
        return swaps

    @staticmethod
    def filter_swaps_by_budget(swaps: List[Tuple[int, int, int]], budget: int) -> List[Tuple[int, int, int]]:
        """
        Filters the list of swaps based on the given budget.

        Args:
            swaps (List[Tuple[int, int, int]]): List of tuples representing swaps.
                Each tuple contains:
                - index of element in A
                - index of element in B
                - cost of swapping these elements
            budget (int): Budget constraint for filtering swaps.

        Returns:
            List[Tuple[int, int, int]]: List of tuples representing swaps that fit within the budget.
        """
        if budget < 0:
            raise ValueError("Budget must be a non-negative integer.")

        # Filter swaps based on budget
        filtered_swaps = [swap for swap in swaps if swap[2] <= budget]
        return filtered_swaps

    @staticmethod
    def sort_swaps_by_cost(swaps: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
        """
        Sorts the swaps by their cost in ascending order.

        Args:
            swaps (List[Tuple[int, int, int]]): List of tuples representing swaps.
                Each tuple contains:
                - index of element in A
                - index of element in B
                - cost of swapping these elements

        Returns:
            List[Tuple[int, int, int]]: List of tuples sorted by cost in ascending order.
        """
        return sorted(swaps, key=lambda x: x[2])

    @staticmethod
    def log_swap_details(swaps: List[Tuple[int, int, int]], log_file: str = "swap_cost_manager.log") -> None:
        """
        Logs the details of swaps to a specified log file.

        Args:
            swaps (List[Tuple[int, int, int]]): List of tuples representing swaps.
                Each tuple contains:
                - index of element in A
                - index of element in B
                - cost of swapping these elements
            log_file (str): Path to the log file. Defaults to "swap_cost_manager.log".

        Returns:
            None
        """
        try:
            with open(log_file, 'a') as file:
                for swap in swaps:
                    file.write(f"Swap: A[{swap[0]}] <-> B[{swap[1]}], Cost: {swap[2]}\n")
        except Exception as e:
            raise ValueError(f"Error writing to log file: {e}")
