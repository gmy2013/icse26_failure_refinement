## main.py

from collections import Counter
from typing import List


class MexCalculator:
    """Class to compute the maximum MEX for a given array and increment value."""

    def compute_max_mex(self, n: int, x: int, a: List[int]) -> int:
        """Compute the maximum MEX after any number of increments by x.

        Args:
            n: The number of elements in the array.
            x: The increment value.
            a: The list of integers.

        Returns:
            The maximum possible MEX.
        """
        # Count the frequency of each residue class modulo x
        residue_count = Counter()
        for value in a:
            residue = value % x
            residue_count[residue] += 1

        # Try to construct the MEX from 0 upwards
        mex = 0
        while True:
            residue = mex % x
            if residue_count[residue] > 0:
                residue_count[residue] -= 1
                mex += 1
            else:
                break
        return mex


class MainApp:
    """Main application class to handle input/output and invoke MexCalculator."""

    def __init__(self) -> None:
        """Initialize the MainApp with a MexCalculator instance."""
        self.calculator = MexCalculator()

    def run(self) -> None:
        """Read input, process each test case, and output the result."""
        import sys

        input_lines = sys.stdin.read().splitlines()
        line_idx = 0

        # Read number of test cases
        t = 0
        if line_idx < len(input_lines):
            t = int(input_lines[line_idx].strip())
            line_idx += 1

        for _ in range(t):
            # Read n and x
            while line_idx < len(input_lines) and input_lines[line_idx].strip() == '':
                line_idx += 1  # Skip empty lines
            if line_idx >= len(input_lines):
                break
            n_x_line = input_lines[line_idx].strip()
            line_idx += 1
            n_str, x_str = n_x_line.split()
            n = int(n_str)
            x = int(x_str)

            # Read array a
            a = []
            while len(a) < n and line_idx < len(input_lines):
                a_line = input_lines[line_idx].strip()
                if a_line:
                    a.extend(map(int, a_line.split()))
                line_idx += 1

            # Compute and print the result
            max_mex = self.calculator.compute_max_mex(n, x, a)
            print(max_mex)


if __name__ == "__main__":
    app = MainApp()
    app.run()
