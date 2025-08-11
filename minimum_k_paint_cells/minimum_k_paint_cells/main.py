## main.py

from bisect import bisect_left
from typing import List, Tuple


class PaintCellsSolver:
    """Solver for finding the minimum k to paint all required cells."""

    def __init__(self) -> None:
        """Initializes the PaintCellsSolver."""
        pass

    def min_k_for_case(self, a: List[int]) -> int:
        """
        Finds the minimum k such that all required cells in 'a' can be painted
        with at most one extra cell painted.

        Args:
            a: List of required cell indices (sorted, unique).

        Returns:
            The minimal integer k.
        """
        a_sorted = sorted(a)
        n = len(a_sorted)
        # The minimal k is at least 1, maximal is the largest gap + 1
        left, right = 1, max(1, a_sorted[-1] - a_sorted[0] + 1)
        answer = right
        while left <= right:
            mid = (left + right) // 2
            if self.is_possible(a_sorted, mid):
                answer = mid
                right = mid - 1
            else:
                left = mid + 1
        return answer

    def is_possible(self, a: List[int], k: int) -> bool:
        """
        Checks if all required cells can be painted with at most one extra cell,
        using brush length k.

        Args:
            a: Sorted list of required cell indices.
            k: Brush length.

        Returns:
            True if possible, False otherwise.
        """
        n = len(a)
        i = 0
        used_extra = False
        while i < n:
            # Paint from a[i] to a[i] + k - 1
            end = a[i] + k - 1
            j = i
            # Move j to the last index covered by this stroke
            while j < n and a[j] <= end:
                j += 1
            # If we have not used the extra cell, try to extend by one
            if not used_extra and j < n and a[j] == end + 1:
                # Use the extra cell to cover a[j]
                used_extra = True
                end += 1
                j += 1
                # Also cover any further cells within the extended range
                while j < n and a[j] <= end:
                    j += 1
            i = j
        # If we never needed to use the extra cell, that's fine
        return True

class InputHandler:
    """Handles input parsing for the problem."""

    def __init__(self) -> None:
        """Initializes the InputHandler."""
        pass

    def read_input(self) -> Tuple[int, List[List[int]]]:
        """
        Reads input from standard input.

        Returns:
            A tuple (t, test_cases), where t is the number of test cases,
            and test_cases is a list of lists of required cell indices.
        """
        import sys
        input_lines = sys.stdin.read().splitlines()
        t = int(input_lines[0])
        test_cases = []
        idx = 1
        for _ in range(t):
            n = int(input_lines[idx])
            idx += 1
            a = list(map(int, input_lines[idx].split()))
            idx += 1
            test_cases.append(a)
        return t, test_cases

class OutputHandler:
    """Handles output formatting and printing."""

    def __init__(self) -> None:
        """Initializes the OutputHandler."""
        pass

    def print_results(self, results: List[int]) -> None:
        """
        Prints the results, one per line.

        Args:
            results: List of integers to print.
        """
        for res in results:
            print(res)

class Main:
    """Main class to run the program."""

    def __init__(self) -> None:
        """Initializes the Main class."""
        self.input_handler = InputHandler()
        self.solver = PaintCellsSolver()
        self.output_handler = OutputHandler()

    def run(self) -> None:
        """Runs the main program logic."""
        t, test_cases = self.input_handler.read_input()
        results = []
        for a in test_cases:cd
            min_k = self.solver.min_k_for_case(a)
            results.append(min_k)
        self.output_handler.print_results(results)


if __name__ == "__main__":
    main = Main()
    main.run()
