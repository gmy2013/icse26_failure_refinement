## main.py

from collections import defaultdict, deque
from typing import List, Dict, Tuple


class TreeSolver:
    """Class to solve the tree increment problem using tree DP."""

    def solve_multiple(self, test_cases: List[Dict]) -> List[int]:
        """Solve multiple test cases.

        Args:
            test_cases: List of test case dicts, each with keys:
                - 'n': int, number of nodes
                - 'a': List[int], node values (1-based)
                - 'parents': List[int], parent of each node 2..n (1-based)

        Returns:
            List[int]: Minimum number of increment operations for each test case.
        """
        results = []
        for case in test_cases:
            n = case['n']
            a = case['a']
            parents = case['parents']
            result = self.solve_single(n, a, parents)
            results.append(result)
        return results

    def solve_single(self, n: int, a: List[int], parents: List[int]) -> int:
        """Solve a single test case.

        Args:
            n: Number of nodes.
            a: List of node values, 1-based (a[0] is value of node 1).
            parents: List of parent indices for nodes 2..n (1-based).

        Returns:
            int: Minimum number of increment operations.
        """
        tree = self._build_tree(n, parents)
        # Convert a to 1-based for easier indexing
        a1 = [0] + a
        _, min_operations = self._dfs(1, tree, a1)
        return min_operations

    def _build_tree(self, n: int, parents: List[int]) -> Dict[int, List[int]]:
        """Build adjacency list for the tree.

        Args:
            n: Number of nodes.
            parents: List of parent indices for nodes 2..n (1-based).

        Returns:
            Dict[int, List[int]]: Adjacency list, 1-based node indices.
        """
        tree = defaultdict(list)
        for child, parent in enumerate(parents, start=2):
            tree[parent].append(child)
        return tree

    def _dfs(
        self, v: int, tree: Dict[int, List[int]], a: List[int]
    ) -> Tuple[int, int]:
        """Post-order DFS to compute required increments.

        Args:
            v: Current node index (1-based).
            tree: Adjacency list.
            a: Node values, 1-based.

        Returns:
            Tuple[int, int]: (final value at v after increments, total increments in subtree)
        """
        if v not in tree or not tree[v]:
            # Leaf node
            return a[v], 0

        children_sum = 0
        total_increments = 0
        for child in tree[v]:
            child_value, child_increments = self._dfs(child, tree, a)
            children_sum += child_value
            total_increments += child_increments

        if a[v] > children_sum:
            # Need to increment children to match a[v]
            increment = a[v] - children_sum
            total_increments += increment
            return a[v], total_increments
        else:
            # Need to increment this node to match children_sum
            increment = children_sum - a[v]
            total_increments += increment
            return children_sum, total_increments


class Main:
    """Main class for CLI input/output."""

    @staticmethod
    def main() -> None:
        """Main entry point for CLI."""
        import sys

        input_lines = deque(sys.stdin.read().splitlines())
        t = int(input_lines.popleft())
        test_cases = []

        for _ in range(t):
            n = int(input_lines.popleft())
            a = list(map(int, input_lines.popleft().split()))
            parents = list(map(int, input_lines.popleft().split()))
            test_cases.append({'n': n, 'a': a, 'parents': parents})

        solver = TreeSolver()
        results = solver.solve_multiple(test_cases)
        for res in results:
            print(res)


if __name__ == "__main__":
    Main.main()
