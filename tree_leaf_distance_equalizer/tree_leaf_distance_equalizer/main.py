## main.py

from collections import defaultdict, deque
import sys
from typing import List, Tuple, Dict



class TreeLeafDistanceEqualizer:
    """Class to compute minimum leaf-removal operations to equalize leaf distances from root."""

    def __init__(self, n: int, edges: List[Tuple[int, int]]) -> None:
        """Initializes the tree structure.

        Args:
            n: Number of nodes in the tree.
            edges: List of edges, each as a tuple (u, v).
        """
        self.n: int = n
        self.tree: Dict[int, List[int]] = defaultdict(list)
        for u, v in edges:
            self.tree[u].append(v)
            self.tree[v].append(u)

    def min_operations(self) -> int:
        """Calculates the minimum number of leaf-removal operations.

        Returns:
            The minimum number of operations required.
        """
        if self.n == 1:
            # Only root node, no leaves to remove.
            return 0

        # BFS to compute depth of each node and identify leaves.
        depth_count: Dict[int, int] = defaultdict(int)
        visited: List[bool] = [False] * (self.n + 1)
        queue: deque = deque()
        queue.append((1, 0))  # (node, depth)
        visited[1] = True

        leaves_total: int = 0

        while queue:
            node, depth = queue.popleft()
            is_leaf: bool = True
            for neighbor in self.tree[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append((neighbor, depth + 1))
                    is_leaf = False
            if is_leaf:
                depth_count[depth] += 1
                leaves_total += 1

        if not depth_count:
            return 0

        max_leaves_at_same_depth: int = max(depth_count.values())
        min_operations: int = leaves_total - max_leaves_at_same_depth
        return min_operations


class Main:
    """Main class for input parsing and process orchestration."""

    def parse_input(self) -> List[Tuple[int, List[Tuple[int, int]]]]:
        """Parses input from stdin.

        Returns:
            List of test cases, each as (n, edges).
        """
        input_lines = sys.stdin.read().splitlines()
        test_cases: List[Tuple[int, List[Tuple[int, int]]]] = []
        idx: int = 0
        t: int = int(input_lines[idx])
        idx += 1
        for _ in range(t):
            n: int = int(input_lines[idx])
            idx += 1
            edges: List[Tuple[int, int]] = []
            for _ in range(n - 1):
                u_str, v_str = input_lines[idx].split()
                u, v = int(u_str), int(v_str)
                edges.append((u, v))
                idx += 1
            test_cases.append((n, edges))
        return test_cases

    def process(self) -> None:
        """Processes all test cases and prints results."""
        test_cases = self.parse_input()
        results: List[int] = []
        for n, edges in test_cases:
            equalizer = TreeLeafDistanceEqualizer(n, edges)
            result = equalizer.min_operations()
            results.append(result)
        for res in results:
            print(res)


if __name__ == "__main__":
    main = Main()
    main.process()
