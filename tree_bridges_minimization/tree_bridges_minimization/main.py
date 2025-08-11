## main.py

from typing import List, Tuple
import sys
import threading

class InputParser:
    """Class responsible for parsing input from stdin."""

    @staticmethod
    def parse_input() -> List[Tuple[int, List[Tuple[int, int]]]]:
        """
        Parses the input from sys.stdin.

        Returns:
            List of tuples, each containing:
                - n: int, number of nodes in the tree
                - edges: List of (u, v) tuples representing edges
        """
        input_lines = sys.stdin.read().splitlines()
        testcases = []
        idx = 0
        t = int(input_lines[idx])
        idx += 1
        for _ in range(t):
            n = int(input_lines[idx])
            idx += 1
            edges = []
            for _ in range(n - 1):
                u, v = map(int, input_lines[idx].split())
                edges.append((u - 1, v - 1))  # Convert to 0-based index
                idx += 1
            testcases.append((n, edges))
        return testcases


class TreeBridgesMinimizer:
    """
    Class to compute the minimum number of bridges in a tree after adding k edges.
    """

    def __init__(self, n: int, edges: List[Tuple[int, int]]) -> None:
        """
        Initializes the tree structure.

        Args:
            n: Number of nodes in the tree.
            edges: List of (u, v) tuples representing edges.
        """
        self.n: int = n
        self.edges: List[List[int]] = [[] for _ in range(n)]
        for u, v in edges:
            self.edges[u].append(v)
            self.edges[v].append(u)
        self.subtree_size: List[int] = [0] * n
        self.depth: List[int] = [0] * n
        self.parent: List[int] = [-1] * n
        self.bridges: int = n - 1  # Initially, a tree has n-1 bridges

    def compute_subtree_sizes(self) -> None:
        """
        Computes the size of each subtree and the depth of each node.
        """
        def dfs(u: int, p: int, d: int) -> int:
            self.parent[u] = p
            self.depth[u] = d
            size = 1
            for v in self.edges[u]:
                if v == p:
                    continue
                size += dfs(v, u, d + 1)
            self.subtree_size[u] = size
            return size

        dfs(0, -1, 0)

    def min_bridges_for_all_k(self) -> List[int]:
        """
        For each k (1 <= k < n), computes the minimum number of bridges after adding k edges.

        Returns:
            List of minimum number of bridges for each k (1-based index).
        """
        # The number of bridges in a tree is n-1.
        # Adding an edge can reduce the number of bridges by at most 1,
        # but only if it connects two different components of the bridge forest.
        # In a tree, every edge is a bridge. Adding an edge creates a cycle,
        # and all edges in that cycle are no longer bridges.
        # The minimum number of bridges after adding k edges is max(0, n-1-k).
        # However, in a general tree, adding an edge can remove more than one bridge
        # if the cycle covers more than one bridge (e.g., in a chain).
        # For a caterpillar, the best we can do is to add edges between the farthest apart nodes.

        # For a tree, the maximum number of bridges that can be removed by adding k edges is k,
        # unless the tree is a chain, in which case adding an edge between the two ends
        # removes all bridges in the cycle (i.e., more than one).
        # But in a general tree, the best is to add edges between nodes with the largest distance.

        # For this problem, since the root has only one child, the tree is a caterpillar.
        # The optimal is to add edges between leaves as far apart as possible.

        # To generalize, we can find the diameter of the tree.
        # Adding an edge between the two ends of the diameter removes all bridges in the path.

        # Let's find the diameter path.
        from collections import deque

        def bfs(start: int) -> Tuple[int, List[int]]:
            visited = [False] * self.n
            parent = [-1] * self.n
            q = deque()
            q.append(start)
            visited[start] = True
            last = start
            while q:
                u = q.popleft()
                last = u
                for v in self.edges[u]:
                    if not visited[v]:
                        visited[v] = True
                        parent[v] = u
                        q.append(v)
            # Reconstruct path
            path = []
            cur = last
            while cur != -1:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return last, path

        # First BFS to find one end of the diameter
        far_node, _ = bfs(0)
        # Second BFS to find the other end and the diameter path
        other_far_node, diameter_path = bfs(far_node)
        diameter_length = len(diameter_path) - 1

        # The best we can do is to add edges to cover the diameter path
        # Each edge added between two nodes on the diameter can remove all bridges in the cycle
        # For a caterpillar, after covering the diameter, the remaining bridges are in the branches

        # For each k, the minimum number of bridges is:
        # - For k <= diameter_length, bridges = n-1 - k
        # - For k > diameter_length, bridges = n-1 - diameter_length - (k - diameter_length)
        #   but since after covering the diameter, only branches remain, which are leaves

        # Actually, after covering the diameter, the remaining bridges are in the branches,
        # which are attached to the diameter path. Each such branch is a leaf, and its edge is a bridge.

        # Let's count the number of leaves not on the diameter path
        on_diameter = [False] * self.n
        for node in diameter_path:
            on_diameter[node] = True

        leaf_bridges = 0
        for u in range(self.n):
            if not on_diameter[u] and len(self.edges[u]) == 1:
                leaf_bridges += 1

        # For k <= diameter_length, bridges = n-1 - k
        # For k > diameter_length, bridges = leaf_bridges - (k - diameter_length)
        # but not less than 0

        result = []
        for k in range(1, self.n):
            if k <= diameter_length:
                bridges = self.n - 1 - k
            else:
                bridges = max(0, leaf_bridges - (k - diameter_length))
            result.append(bridges)
        return result


class OutputFormatter:
    """Class responsible for formatting and outputting results."""

    @staticmethod
    def format_output(results: List[List[int]]) -> None:
        """
        Prints the results to sys.stdout.

        Args:
            results: List of lists, each inner list is the answer for a testcase.
        """
        for res in results:
            print(' '.join(map(str, res)))


class Main:
    """Main class to orchestrate the program flow."""

    @staticmethod
    def main() -> None:
        """
        Main function to run the program.
        """
        testcases = InputParser.parse_input()
        all_results: List[List[int]] = []
        for n, edges in testcases:
            minimizer = TreeBridgesMinimizer(n, edges)
            minimizer.compute_subtree_sizes()
            bridges_list = minimizer.min_bridges_for_all_k()
            all_results.append(bridges_list)
        OutputFormatter.format_output(all_results)


if __name__ == "__main__":
    threading.Thread(target=Main.main).start()
