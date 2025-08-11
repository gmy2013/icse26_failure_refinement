## main.py

import sys
from typing import List, Dict, Set, Tuple

class SubtreeDP:
    """Implements bottom-up DP for subset sum of subtree sizes in a tree."""

    def __init__(self, n: int, edges: Dict[int, List[int]]) -> None:
        """
        Args:
            n: Number of nodes in the tree.
            edges: Adjacency list representing the tree.
        """
        self.n = n
        self.edges = edges
        self.dp: List[Set[int]] = [set() for _ in range(n + 1)]

    def compute(self, root: int, subtree_sizes: List[int]) -> Set[int]:
        """
        Computes all possible sums of disjoint subtree sizes that can be removed from the tree.

        Args:
            root: The root node of the tree.
            subtree_sizes: List of subtree sizes for each node.

        Returns:
            Set of all possible sums of removed subtree sizes (excluding 0).
        """
        def dfs(u: int) -> Set[int]:
            # For each node, maintain a set of possible sums of removed subtrees in its subtree
            possible: Set[int] = set()
            for v in self.edges.get(u, []):
                child_possible = dfs(v)
                # Merge child_possible into possible using subset sum DP
                if not possible:
                    possible = child_possible.copy()
                else:
                    new_possible = possible.copy()
                    for x in possible:
                        for y in child_possible:
                            new_possible.add(x + y)
                    new_possible |= child_possible
                    possible = new_possible
            # Option to remove the whole subtree rooted at u (excluding the root of the whole tree)
            if u != root:
                possible.add(subtree_sizes[u])
            self.dp[u] = possible
            return possible

        return dfs(root)

class Tree:
    """Represents a single rooted tree and computes possible OR values."""

    def __init__(self, n: int, parents: List[int]) -> None:
        """
        Args:
            n: Number of nodes in the tree.
            parents: List of parent indices for nodes 2..n (1-based).
        """
        self.n = n
        self.parents = parents
        self.edges: Dict[int, List[int]] = {}
        self.subtree_sizes: List[int] = [0] * (n + 1)
        self.root: int = 1
        self._build_tree()

    def _build_tree(self) -> None:
        """Builds the adjacency list from the parent list."""
        for i in range(2, self.n + 1):
            p = self.parents[i - 2]
            if p not in self.edges:
                self.edges[p] = []
            self.edges[p].append(i)

    def compute_subtree_sizes(self) -> None:
        """Computes the size of the subtree rooted at each node."""
        def dfs(u: int) -> int:
            size = 1
            for v in self.edges.get(u, []):
                size += dfs(v)
            self.subtree_sizes[u] = size
            return size
        dfs(self.root)

    def get_possible_or(self) -> int:
        """
        Computes the maximal bitwise OR of the sizes of removed disjoint subtrees.

        Returns:
            The maximal bitwise OR value for this tree.
        """
        self.compute_subtree_sizes()
        dp_solver = SubtreeDP(self.n, self.edges)
        possible_sums = dp_solver.compute(self.root, self.subtree_sizes)
        # The problem asks for the maximal bitwise OR of any subset of possible sums
        # We can use subset DP to compute the maximal OR
        or_result = 0
        for s in possible_sums:
            or_result |= s
        # Also, the whole tree can be removed as a single subtree
        or_result = max(or_result, self.subtree_sizes[self.root])
        return or_result

class ForestProcessor:
    """Handles parsing input, processing test cases, and aggregating results."""

    def parse_input(self, input_lines: List[str]) -> List[List[Tuple[int, List[int]]]]:
        """
        Parses the input lines into test cases.

        Args:
            input_lines: List of input lines.

        Returns:
            List of test cases, each test case is a list of (n, parents) for each tree in the forest.
        """
        test_cases: List[List[Tuple[int, List[int]]]] = []
        idx = 0
        t = int(input_lines[idx].strip())
        idx += 1
        for _ in range(t):
            m = int(input_lines[idx].strip())
            idx += 1
            trees: List[Tuple[int, List[int]]] = []
            for _ in range(m):
                n = int(input_lines[idx].strip())
                idx += 1
                if n == 1:
                    parents = []
                else:
                    parents = list(map(int, input_lines[idx].strip().split()))
                    idx += 1
                trees.append((n, parents))
            test_cases.append(trees)
        return test_cases

    def process_test_cases(self, test_cases: List[List[Tuple[int, List[int]]]]) -> List[int]:
        """
        Processes all test cases and computes the maximal OR for each forest.

        Args:
            test_cases: List of test cases.

        Returns:
            List of maximal OR values for each test case.
        """
        results: List[int] = []
        for trees in test_cases:
            or_values: List[int] = []
            for n, parents in trees:
                tree = Tree(n, parents)
                or_value = tree.get_possible_or()
                or_values.append(or_value)
            # For the forest, combine the OR values of all trees
            forest_or = 0
            for val in or_values:
                forest_or |= val
            results.append(forest_or)
        return results

def main() -> None:
    """Entry point: reads input, processes test cases, and prints results."""
    input_lines = sys.stdin.read().splitlines()
    processor = ForestProcessor()
    test_cases = processor.parse_input(input_lines)
    results = processor.process_test_cases(test_cases)
    for res in results:
        print(res)

if __name__ == "__main__":
    main()
