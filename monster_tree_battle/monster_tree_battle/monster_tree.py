## monster_tree.py
from typing import List, Tuple, Dict


class MonsterTree:
    """Class representing a monster tree and DP logic for minimum health decrement."""

    def __init__(self, n: int, attack_points: List[int], edges: List[Tuple[int, int]]) -> None:
        """Initializes the MonsterTree.

        Args:
            n: Number of monsters (nodes).
            attack_points: List of attack points for each monster (0-indexed).
            edges: List of edges, each as a tuple (u, v) with 1-based indices.
        """
        self.n: int = n
        self.attack_points: List[int] = attack_points
        self.edges: List[List[int]] = [[] for _ in range(n)]
        for u, v in edges:
            # Convert to 0-based index
            self.edges[u - 1].append(v - 1)
            self.edges[v - 1].append(u - 1)

    def min_health_decrement(self) -> int:
        """Computes the minimum total health decrement to kill all monsters.

        Returns:
            The minimum possible health decrement (int).
        """
        dp_with, dp_without = self._dfs(0, -1)
        return min(dp_with, dp_without)

    def _dfs(self, u: int, parent: int) -> Tuple[int, int]:
        """Performs DP on the tree to compute min health decrement.

        Args:
            u: Current node index.
            parent: Parent node index.

        Returns:
            A tuple (with_u, without_u):
                with_u: Minimum health decrement if u is killed in this round.
                without_u: Minimum health decrement if u is not killed in this round.
        """
        with_u: int = self.attack_points[u]
        without_u: int = 0

        for v in self.edges[u]:
            if v == parent:
                continue
            child_with, child_without = self._dfs(v, u)
            # If u is killed, children cannot be killed in this round
            with_u += child_without
            # If u is not killed, children can be killed or not, take min
            without_u += min(child_with, child_without)

        return with_u, without_u
