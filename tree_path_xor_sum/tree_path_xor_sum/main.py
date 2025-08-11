## main.py

from collections import defaultdict, deque
import sys
from typing import List, Dict

sys.setrecursionlimit(1 << 20)


class Tree:
    """Tree structure supporting LCA (Lowest Common Ancestor) and path reconstruction."""

    def __init__(self, n: int, adj: Dict[int, List[int]], a: List[int]) -> None:
        """Initializes the tree.

        Args:
            n: Number of nodes in the tree.
            adj: Adjacency list representing the tree.
            a: List of node values (1-indexed).
        """
        self.n: int = n
        self.adj: Dict[int, List[int]] = adj
        self.a: List[int] = a
        self.max_log: int = (self.n).bit_length()
        self.parent: List[List[int]] = [[-1] * (self.n + 1) for _ in range(self.max_log)]
        self.depth: List[int] = [0] * (self.n + 1)
        self._preprocessed: bool = False

    def preprocess(self, root: int = 1) -> None:
        """Preprocesses the tree for LCA queries using binary lifting.

        Args:
            root: The root node of the tree (default is 1).
        """
        def dfs(u: int, p: int) -> None:
            self.parent[0][u] = p
            for v in self.adj[u]:
                if v != p:
                    self.depth[v] = self.depth[u] + 1
                    dfs(v, u)

        dfs(root, -1)
        for k in range(1, self.max_log):
            for v in range(1, self.n + 1):
                if self.parent[k - 1][v] != -1:
                    self.parent[k][v] = self.parent[k - 1][self.parent[k - 1][v]]
        self._preprocessed = True

    def lca(self, u: int, v: int) -> int:
        """Finds the lowest common ancestor (LCA) of nodes u and v.

        Args:
            u: First node.
            v: Second node.

        Returns:
            The LCA node.
        """
        if not self._preprocessed:
            raise RuntimeError("Tree must be preprocessed before LCA queries.")

        if self.depth[u] < self.depth[v]:
            u, v = v, u
        # Bring u up to depth v
        for k in reversed(range(self.max_log)):
            if self.parent[k][u] != -1 and self.depth[self.parent[k][u]] >= self.depth[v]:
                u = self.parent[k][u]
        if u == v:
            return u
        for k in reversed(range(self.max_log)):
            if self.parent[k][u] != -1 and self.parent[k][u] != self.parent[k][v]:
                u = self.parent[k][u]
                v = self.parent[k][v]
        return self.parent[0][u]

    def get_path(self, u: int, v: int) -> List[int]:
        """Returns the list of nodes along the path from u to v (inclusive).

        Args:
            u: Start node.
            v: End node.

        Returns:
            List of node indices along the path from u to v.
        """
        lca = self.lca(u, v)
        path_u = []
        curr = u
        while curr != lca:
            path_u.append(curr)
            curr = self.parent[0][curr]
        path_u.append(lca)
        path_v = []
        curr = v
        while curr != lca:
            path_v.append(curr)
            curr = self.parent[0][curr]
        path = path_u + path_v[::-1]
        return path


class QueryProcessor:
    """Processes queries on the tree."""

    def __init__(self, tree: Tree) -> None:
        """Initializes the query processor.

        Args:
            tree: The Tree object to process queries on.
        """
        self.tree: Tree = tree

    def process_query(self, x: int, y: int) -> int:
        """Processes a single query: computes sum of (a_{p_i} XOR i) along the path from x to y.

        Args:
            x: Start node.
            y: End node.

        Returns:
            The computed sum.
        """
        path = self.tree.get_path(x, y)
        total = 0
        for idx, node in enumerate(path, 1):
            total += self.tree.a[node] ^ idx
        return total


class MainApp:
    """Main application class for input/output and orchestration."""

    def run(self) -> None:
        """Runs the main application: parses input, processes queries, and outputs results."""
        input = sys.stdin.readline

        n = int(input())
        a_list = [0] + list(map(int, input().split()))
        adj = defaultdict(list)
        for _ in range(n - 1):
            u, v = map(int, input().split())
            adj[u].append(v)
            adj[v].append(u)

        tree = Tree(n, adj, a_list)
        tree.preprocess(root=1)
        query_processor = QueryProcessor(tree)

        q = int(input())
        results = []
        for _ in range(q):
            x, y = map(int, input().split())
            res = query_processor.process_query(x, y)
            results.append(str(res))
        print('\n'.join(results))


if __name__ == "__main__":
    app = MainApp()
    app.run()
