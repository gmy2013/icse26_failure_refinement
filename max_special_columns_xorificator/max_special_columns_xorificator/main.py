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
