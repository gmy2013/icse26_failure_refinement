## main.py

from typing import List, Tuple
import sys
import threading
from collections import defaultdict

class InputHandler:
    """Handles input parsing from sys.stdin."""

    def read_input(self) -> List[Tuple[int, List[int], List[int]]]:
        """
        Reads multiple test cases from standard input.

        Returns:
            List of tuples, each containing:
                - n: int, number of nodes
                - a: List[int], node values (1-based index)
                - parents: List[int], parent indices for nodes 2..n (1-based)
        """
        input_lines = sys.stdin.read().splitlines()
        test_cases = []
        idx = 0
        t = int(input_lines[idx])
        idx += 1
        for _ in range(t):
            n = int(input_lines[idx])
            idx += 1
            a = list(map(int, input_lines[idx].split()))
            idx += 1
            if n == 1:
                parents = []
            else:
                parents = list(map(int, input_lines[idx].split()))
                idx += 1
            test_cases.append((n, a, parents))
        return test_cases


class TreeRootMaximizer:
    """
    Maximizes the root value of a tree by performing allowed operations.

    Attributes:
        n (int): Number of nodes.
        a (List[int]): Node values (0-based index).
        parents (List[int]): Parent indices for nodes 2..n (1-based).
        tree (defaultdict): Adjacency list representation of the tree.
    """

    def __init__(self, n: int, a: List[int], parents: List[int]) -> None:
        """
        Initializes the tree structure.

        Args:
            n: Number of nodes.
            a: List of node values (1-based index from input, converted to 0-based).
            parents: List of parent indices for nodes 2..n (1-based).
        """
        self.n = n
        self.a = a[:]  # 0-based
        self.parents = parents[:]
        self.tree = defaultdict(list)  # type: defaultdict[int, List[int]]
        for child_idx, parent in enumerate(self.parents, start=1):
            # parent is 1-based, child_idx is 1-based (since node 1 is root)
            self.tree[parent - 1].append(child_idx)
        # Ensure all nodes are in the tree
        for i in range(n):
            if i not in self.tree:
                self.tree[i] = []

    def maximize_root(self) -> int:
        """
        Computes the maximum possible value at the root after allowed operations.

        Returns:
            int: The maximized root value.
        """
        root_value, _ = self._dfs(0)
        return root_value

    def _dfs(self, node: int) -> Tuple[int, int]:
        """
        Post-order DFS to compute the maximum value at each node.

        Args:
            node: Current node index (0-based).

        Returns:
            Tuple[int, int]: (maximized value at this node, sum of values that can be pushed up)
        """
        if not self.tree[node]:
            # Leaf node: cannot push up anything, value remains as is
            return self.a[node], 0

        child_pushable = []
        child_values = []
        for child in self.tree[node]:
            child_val, child_push = self._dfs(child)
            child_values.append(child_val)
            child_pushable.append(child_push)

        # The maximum number of times we can perform the operation at this node
        # is limited by the minimum value among its children
        min_child_val = min(child_values)
        # We can perform the operation min_child_val times
        # For each operation, all children decrease by 1, and this node increases by len(children)
        # After all possible operations, all children are reduced by min_child_val
        # The value at this node increases by min_child_val * len(children)
        # The remaining value at each child is child_val - min_child_val

        # After pushing up, the value at this node:
        node_value = self.a[node] + min_child_val * len(self.tree[node])
        # The sum of values that can be pushed up from children (after their min_child_val is subtracted)
        pushable_sum = 0
        for i, child in enumerate(self.tree[node]):
            # Each child: child_values[i] - min_child_val + child_pushable[i]
            pushable_sum += (child_values[i] - min_child_val) + child_pushable[i]
        return node_value, pushable_sum


class OutputHandler:
    """Handles output to sys.stdout."""

    def write_output(self, results: List[int]) -> None:
        """
        Writes the results to standard output.

        Args:
            results: List of integers, one per test case.
        """
        for res in results:
            print(res)


class Main:
    """Orchestrates the program flow."""

    def main(self) -> None:
        """
        Main entry point for the program.
        """
        input_handler = InputHandler()
        test_cases = input_handler.read_input()
        results = []
        for n, a, parents in test_cases:
            maximizer = TreeRootMaximizer(n, a, parents)
            result = maximizer.maximize_root()
            results.append(result)
        output_handler = OutputHandler()
        output_handler.write_output(results)


def run() -> None:
    """Runs the main function in a separate thread for fast input."""
    Main().main()

if __name__ == "__main__":
    threading.Thread(target=run).start()
