## dsu.py

from typing import List

class DSU:
    """Disjoint Set Union (Union-Find) data structure with path compression and union by size.

    Attributes:
        _parent (List[int]): Parent of each node.
        _size (List[int]): Size of the set for each root node.
    """

    def __init__(self, n: int) -> None:
        """Initializes DSU for n elements (0-indexed).

        Args:
            n (int): Number of elements.
        """
        self._parent: List[int] = list(range(n))
        self._size: List[int] = [1] * n

    def find(self, x: int) -> int:
        """Finds the representative (root) of the set containing x.

        Args:
            x (int): Element to find.

        Returns:
            int: Root of the set containing x.
        """
        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])  # Path compression
        return self._parent[x]

    def union(self, x: int, y: int) -> bool:
        """Unites the sets containing x and y.

        Args:
            x (int): First element.
            y (int): Second element.

        Returns:
            bool: True if union was successful (sets were separate), False otherwise.
        """
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root == y_root:
            return False
        # Union by size: attach smaller tree to larger tree
        if self._size[x_root] < self._size[y_root]:
            x_root, y_root = y_root, x_root
        self._parent[y_root] = x_root
        self._size[x_root] += self._size[y_root]
        return True

    def count_components(self) -> int:
        """Counts the number of connected components.

        Returns:
            int: Number of connected components.
        """
        # A node is a root if parent[node] == node
        return sum(1 for i, p in enumerate(self._parent) if i == p)
