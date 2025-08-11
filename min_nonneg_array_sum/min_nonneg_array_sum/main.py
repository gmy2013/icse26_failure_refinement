## main.py

import sys
from typing import List


class MinNonNegArraySum:
    """Class to maintain a non-negative integer array and process greedy queries to minimize sum."""

    def __init__(self, n: int) -> None:
        """Initialize the array of size n with all zeros.

        Args:
            n (int): The size of the array.
        """
        self.n: int = n
        self.a: List[int] = [0] * n

    def process_query(self, x: int, y: int) -> str:
        """Process a query on positions x and y, greedily minimizing the sum.

        For each query (x, y), attempt to decrement one of the two positions if its value > 0.
        If both are zero, increment x by default.

        Args:
            x (int): 0-based index of the first position.
            y (int): 0-based index of the second position.

        Returns:
            str: The operation performed, e.g., 'x-', 'y-', 'x+', or 'y+'.
        """
        if self.a[x] > 0:
            self.a[x] -= 1
            return 'x-'
        elif self.a[y] > 0:
            self.a[y] -= 1
            return 'y-'
        else:
            # Both are zero, increment x by default for determinism
            self.a[x] += 1
            return 'x+'

    def get_array(self) -> List[int]:
        """Get the current state of the array.

        Returns:
            List[int]: The current array.
        """
        return self.a.copy()


class Main:
    """Main class to handle input/output and orchestrate the process."""

    @staticmethod
    def main() -> None:
        """Entry point for the program. Reads input, processes queries, and outputs results."""
        input_stream = sys.stdin
        output_stream = sys.stdout

        # Read n and q
        first_line = input_stream.readline()
        while first_line.strip() == '':
            first_line = input_stream.readline()
        n_q = first_line.strip().split()
        n: int = int(n_q[0])
        q: int = int(n_q[1])

        # Initialize the MinNonNegArraySum object
        min_array_sum = MinNonNegArraySum(n)

        # Process each query
        for _ in range(q):
            line = input_stream.readline()
            while line.strip() == '':
                line = input_stream.readline()
            x_str, y_str = line.strip().split()
            x: int = int(x_str) - 1  # Convert to 0-based index
            y: int = int(y_str) - 1  # Convert to 0-based index
            op_result = min_array_sum.process_query(x, y)
            output_stream.write(f"{op_result}\n")

        # If needed, output the final array (not specified in requirements)
        # final_array = min_array_sum.get_array()
        # output_stream.write(' '.join(map(str, final_array)) + '\n')


if __name__ == "__main__":
    Main.main()
