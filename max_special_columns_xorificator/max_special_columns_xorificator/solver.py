## solver.py
from collections import Counter
from itertools import product
from typing import List, Tuple, Dict


class MatrixXORSolver:
    """Solver for maximizing the number of 'special' columns in a binary matrix by flipping rows."""

    def __init__(self) -> None:
        """Initializes the MatrixXORSolver."""
        pass

    def solve(
        self, test_cases: List[Tuple[int, int, List[str]]]
    ) -> List[Tuple[int, str]]:
        """
        Solves multiple test cases.

        Args:
            test_cases: A list of tuples, each containing:
                - n: Number of rows in the matrix.
                - m: Number of columns in the matrix.
                - matrix: List of n strings, each of length m, representing the binary matrix.

        Returns:
            A list of tuples, each containing:
                - max_special: The maximum number of special columns achievable.
                - flip_mask: A string of length n, where each character is '0' (no flip) or '1' (flip row).
        """
        results: List[Tuple[int, str]] = []
        for n, m, matrix in test_cases:
            patterns = self._columns_to_patterns(matrix)
            max_special, flip_mask = self._find_optimal_flip(n, m, patterns)
            results.append((max_special, flip_mask))
        return results

    def _columns_to_patterns(self, matrix: List[str]) -> Dict[str, int]:
        """
        Groups columns by their bit patterns.

        Args:
            matrix: List of n strings, each of length m.

        Returns:
            A dictionary mapping each unique column pattern (as a string) to its frequency.
        """
        if not matrix:
            return {}

        n = len(matrix)
        m = len(matrix[0])
        patterns: Counter = Counter()
        for col in range(m):
            pattern = ''.join(matrix[row][col] for row in range(n))
            patterns[pattern] += 1
        return dict(patterns)

    def _find_optimal_flip(
        self, n: int, m: int, patterns: Dict[str, int]
    ) -> Tuple[int, str]:
        """
        Finds the row flip mask that maximizes the number of special columns.

        Args:
            n: Number of rows.
            m: Number of columns.
            patterns: Dictionary mapping column patterns to their frequency.

        Returns:
            A tuple (max_special, flip_mask), where:
                - max_special: Maximum number of special columns.
                - flip_mask: String of length n, '0' (no flip) or '1' (flip row).
        """
        max_special: int = 0
        best_mask: str = '0' * n

        # Precompute all unique patterns for efficiency
        unique_patterns = list(patterns.keys())

        # For each possible row flip mask (2^n possibilities)
        for flip_tuple in product((0, 1), repeat=n):
            flip_mask = ''.join(str(bit) for bit in flip_tuple)
            special_count = 0

            # For each unique column pattern
            for pattern in unique_patterns:
                # Apply the flip mask to the pattern
                flipped_pattern = [
                    str((int(bit) ^ flip_tuple[row]))
                    for row, bit in enumerate(pattern)
                ]
                # Count number of 1s in the flipped column
                ones_count = sum(1 for bit in flipped_pattern if bit == '1')
                if ones_count == 1:
                    special_count += patterns[pattern]

            if special_count > max_special:
                max_special = special_count
                best_mask = flip_mask

        return max_special, best_mask
## main.py
from typing import List, Tuple
from solver import MatrixXORSolver


class Main:
    """Main entry point for the MatrixXORSolver application."""

    @staticmethod
    def main() -> None:
        """
        Parses input, solves the problem using MatrixXORSolver, and prints the results.
        """
        import sys

        def read_ints() -> List[int]:
            return list(map(int, sys.stdin.readline().split()))

        # Read number of test cases
        t_line = ''
        while t_line.strip() == '':
            t_line = sys.stdin.readline()
        t = int(t_line.strip())

        test_cases: List[Tuple[int, int, List[str]]] = []
        for _ in range(t):
            # Read n and m
            while True:
                nm_line = sys.stdin.readline()
                if nm_line.strip():
                    break
            n, m = map(int, nm_line.strip().split())
            # Read n lines of the matrix
            matrix: List[str] = []
            while len(matrix) < n:
                row_line = sys.stdin.readline()
                if row_line.strip():
                    matrix.append(row_line.strip())
            test_cases.append((n, m, matrix))

        # Solve all test cases
        solver = MatrixXORSolver()
        results = solver.solve(test_cases)

        # Print results
        for max_special, flip_mask in results:
            print(max_special)
            print(flip_mask)


if __name__ == "__main__":
    Main.main()
