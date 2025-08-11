## main.py

from typing import List, Tuple


class MaxRemovalOperationsSolver:
    """Solver for maximizing the number of valid removal operations."""

    def solve(self, test_cases: List[Tuple[int, List[int]]]) -> List[int]:
        """Solve all test cases.

        Args:
            test_cases: A list of tuples, each containing the length of the array and the array itself.

        Returns:
            A list of integers, each representing the maximum number of operations for the corresponding test case.
        """
        results: List[int] = []
        for _, a in test_cases:
            operations = self._max_operations(a)
            results.append(operations)
        return results

    def _max_operations(self, a: List[int]) -> int:
        """Compute the maximum number of valid removal operations for a single array.

        At each step, find the leftmost index i (1-based) such that a[i] == i,
        and remove both a[i] and a[i+1]. Repeat until no more valid operations are possible.

        Args:
            a: The input array.

        Returns:
            The maximum number of valid removal operations.
        """
        operations: int = 0
        arr: List[int] = a.copy()
        while True:
            found: bool = False
            n: int = len(arr)
            i: int = 0
            while i < n - 1:
                # 1-based index for comparison
                if arr[i] == i + 1:
                    # Remove arr[i] and arr[i+1]
                    del arr[i:i+2]
                    operations += 1
                    found = True
                    break  # Restart from the beginning after removal
                i += 1
            if not found:
                break
        return operations


class CLI:
    """Command-line interface for the MaxRemovalOperationsSolver."""

    def run(self) -> None:
        """Run the CLI: parse input, solve, and print output."""
        test_cases = self._parse_input()
        solver = MaxRemovalOperationsSolver()
        results = solver.solve(test_cases)
        self._print_output(results)

    def _parse_input(self) -> List[Tuple[int, List[int]]]:
        """Parse input from stdin.

        Input format:
            t
            n1
            a1_1 a1_2 ... a1_n1
            n2
            a2_1 a2_2 ... a2_n2
            ...

        Returns:
            A list of test cases, each as a tuple (n, a).
        """
        import sys

        lines = []
        for line in sys.stdin:
            line = line.strip()
            if line:
                lines.append(line)

        test_cases: List[Tuple[int, List[int]]] = []
        idx: int = 0
        t: int = int(lines[idx])
        idx += 1
        for _ in range(t):
            n: int = int(lines[idx])
            idx += 1
            a: List[int] = list(map(int, lines[idx].split()))
            idx += 1
            test_cases.append((n, a))
        return test_cases

    def _print_output(self, results: List[int]) -> None:
        """Print the results, one per line.

        Args:
            results: List of results to print.
        """
        for res in results:
            print(res)


if __name__ == "__main__":
    cli = CLI()
    cli.run()
