## tree_query.py

from collections import defaultdict, deque
from typing import List, Dict

class Tree:
    """Represents a rooted tree with efficient ancestor and distance queries using binary lifting."""

    def __init__(self, n: int) -> None:
        """Initializes the tree with n nodes.

        Args:
            n (int): Number of nodes in the tree (1-indexed).
        """
        self.n: int = n
        self.edges: Dict[int, List[int]] = defaultdict(list)
        self.depth: List[int] = [0] * (n + 1)
        self.parent: List[int] = [0] * (n + 1)
        self.LOGN: int = max(1, (n).bit_length())
        self.up: List[List[int]] = [[0] * (self.LOGN + 1) for _ in range(n + 1)]
        self.max_depth_in_subtree: List[int] = [0] * (n + 1)
        self.farthest_node: List[int] = [0] * (n + 1)
        self._preprocessed: bool = False

    def add_edge(self, u: int, v: int) -> None:
        """Adds an undirected edge between nodes u and v.

        Args:
            u (int): One endpoint of the edge.
            v (int): The other endpoint of the edge.
        """
        self.edges[u].append(v)
        self.edges[v].append(u)

    def preprocess(self) -> None:
        """Preprocesses the tree for ancestor and distance queries.

        Computes depth, parent, binary lifting table, and farthest node in each subtree.
        """
        self._dfs(1, 0)
        self._build_lifting()
        self._compute_farthest(1, 0)
        self._preprocessed = True

    def _dfs(self, u: int, p: int) -> None:
        """Performs DFS to compute depth and parent for each node.

        Args:
            u (int): Current node.
            p (int): Parent of the current node.
        """
        self.parent[u] = p
        for v in self.edges[u]:
            if v != p:
                self.depth[v] = self.depth[u] + 1
                self._dfs(v, u)

    def _build_lifting(self) -> None:
        """Builds the binary lifting table for fast ancestor queries."""
        for v in range(1, self.n + 1):
            self.up[v][0] = self.parent[v]
        for k in range(1, self.LOGN + 1):
            for v in range(1, self.n + 1):
                self.up[v][k] = self.up[self.up[v][k - 1]][k - 1]

    def _compute_farthest(self, u: int, p: int) -> None:
        """Computes the farthest node and its depth in the subtree rooted at u.

        Args:
            u (int): Current node.
            p (int): Parent of the current node.
        """
        self.max_depth_in_subtree[u] = self.depth[u]
        self.farthest_node[u] = u
        for v in self.edges[u]:
            if v != p:
                self._compute_farthest(v, u)
                if self.max_depth_in_subtree[v] > self.max_depth_in_subtree[u]:
                    self.max_depth_in_subtree[u] = self.max_depth_in_subtree[v]
                    self.farthest_node[u] = self.farthest_node[v]

    def is_ancestor(self, u: int, v: int) -> bool:
        """Checks if node u is an ancestor of node v.

        Args:
            u (int): Potential ancestor node.
            v (int): Potential descendant node.

        Returns:
            bool: True if u is ancestor of v, False otherwise.
        """
        # Move v up to the depth of u
        if self.depth[v] < self.depth[u]:
            return False
        v_up = self.get_kth_ancestor(v, self.depth[v] - self.depth[u])
        return v_up == u

    def get_kth_ancestor(self, u: int, k: int) -> int:
        """Finds the k-th ancestor of node u.

        Args:
            u (int): The node to start from.
            k (int): The number of steps to go up.

        Returns:
            int: The k-th ancestor of u, or 0 if it does not exist.
        """
        for i in range(self.LOGN + 1):
            if k & (1 << i):
                u = self.up[u][i]
                if u == 0:
                    break
        return u

    def get_farthest_distance(self, v: int, stamina: int) -> int:
        """Finds the maximum distance Chefir can reach from node v with given stamina.

        Args:
            v (int): Starting node.
            stamina (int): Maximum stamina (number of non-descendant moves allowed).

        Returns:
            int: The maximum distance Chefir can reach from node v.
        """
        if not self._preprocessed:
            raise RuntimeError("Tree must be preprocessed before querying.")

        # 1. Try to go as deep as possible in the subtree of v (costs 0 stamina)
        max_dist = self.max_depth_in_subtree[v] - self.depth[v]

        # 2. Try to move up to ancestors (each move up costs 1 stamina), then go as deep as possible in their subtrees
        u = v
        stamina_left = stamina
        for k in range(self.LOGN, -1, -1):
            if stamina_left >= (1 << k):
                u_ancestor = self.up[u][k]
                if u_ancestor == 0:
                    continue
                # After moving up (1 << k) steps, stamina_left decreases
                u = u_ancestor
                stamina_left -= (1 << k)
        # Now, u is the ancestor we can reach with given stamina
        # For all possible ancestors up to stamina, check the farthest in their subtrees
        u = v
        for used in range(1, stamina + 1):
            u_ancestor = self.get_kth_ancestor(v, used)
            if u_ancestor == 0:
                break
            dist = self.max_depth_in_subtree[u_ancestor] - self.depth[v] + used
            if dist > max_dist:
                max_dist = dist
        return max_dist


class QueryProcessor:
    """Processes queries on a given tree."""

    def __init__(self, tree: Tree) -> None:
        """Initializes the QueryProcessor with a tree.

        Args:
            tree (Tree): The tree to process queries on.
        """
        self.tree: Tree = tree

    def process_query(self, v: int, stamina: int) -> int:
        """Processes a single query.

        Args:
            v (int): Starting node.
            stamina (int): Stamina constraint.

        Returns:
            int: The maximum distance reachable from v with given stamina.
        """
        return self.tree.get_farthest_distance(v, stamina)

    def process_queries(self, queries: List[tuple]) -> List[int]:
        """Processes a list of queries.

        Args:
            queries (List[tuple]): List of (v, stamina) queries.

        Returns:
            List[int]: List of results for each query.
        """
        results: List[int] = []
        for v, stamina in queries:
            results.append(self.process_query(v, stamina))
        return results
