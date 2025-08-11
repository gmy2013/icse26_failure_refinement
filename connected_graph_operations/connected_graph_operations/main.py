## main.py
from typing import List, Tuple


class ConnectedGraphSolver:
    """Solver for the connected graph problem under divisibility constraints."""

    def solve(self, test_cases: List[Tuple[int, List[int]]]) -> List[str]:
        """Solves multiple test cases.

        Args:
            test_cases: List of tuples, each containing n and the array a.

        Returns:
            List of strings, each representing the output for a test case.
        """
        results: List[str] = []
        for n, a in test_cases:
            root: int = self._find_root(a)
            if root == -1:
                # All values are the same, impossible to connect as per constraints
                results.append("NO")
                continue
            edges: List[Tuple[int, int]] = self._build_edges(a, root)
            output_lines: List[str] = ["YES"]
            for u, v in edges:
                # Output is 1-based indexing
                output_lines.append(f"{u + 1} {v + 1}")
            results.append('\n'.join(output_lines))
        return results

    def _find_root(self, a: List[int]) -> int:
        """Finds the index of a node with a unique value.

        Args:
            a: List of node values.

        Returns:
            Index of the root node, or -1 if all values are the same.
        """
        n: int = len(a)
        for i in range(1, n):
            if a[i] != a[0]:
                return 0  # Use the first node as root if there is at least one different value
        return -1  # All values are the same

    def _build_edges(self, a: List[int], root: int) -> List[Tuple[int, int]]:
        """Builds the list of edges to connect the graph under the constraints.

        Args:
            a: List of node values.
            root: Index of the root node.

        Returns:
            List of edges as tuples (u, v), 0-based indices.
        """
        n: int = len(a)
        edges: List[Tuple[int, int]] = []
        # First, connect all nodes with value different from root to root
        for i in range(n):
            if a[i] != a[root]:
                edges.append((root, i))
        # Then, connect all nodes with the same value as root (except root itself)
        # to any node already connected (which must have a different value)
        # We can pick the first such node
        first_diff: int = -1
        for i in range(n):
            if a[i] != a[root]:
                first_diff = i
                break
        for i in range(n):
            if i != root and a[i] == a[root]:
                # Connect to a node with different value
                edges.append((first_diff, i))
        return edges


class Main:
    """Main class for input/output and program entry point."""

    @staticmethod
    def main() -> None:
        """Reads input, solves the problem, and prints output."""
        import sys

        input_lines: List[str] = sys.stdin.read().splitlines()
        t: int = int(input_lines[0])
        test_cases: List[Tuple[int, List[int]]] = []
        idx: int = 1
        for _ in range(t):
            n: int = int(input_lines[idx])
            a: List[int] = list(map(int, input_lines[idx + 1].split()))
            test_cases.append((n, a))
            idx += 2

        solver = ConnectedGraphSolver()
        results: List[str] = solver.solve(test_cases)
        print('\n'.join(results))


if __name__ == "__main__":
    Main.main()
