## connect_the_dots_game.py

from typing import Optional
from dsu import DSU

class ConnectTheDotsGame:
    """Class to manage the Connect The Dots game logic.

    Attributes:
        _n (int): Number of points.
        _m (int): Number of operations.
        _dsu (DSU): Disjoint Set Union instance for managing connectivity.
    """

    def __init__(self, n: int, m: int) -> None:
        """Initializes the game with n points and m operations.

        Args:
            n (int): Number of points.
            m (int): Number of operations.
        """
        self._n: int = n
        self._m: int = m
        self._dsu: DSU = DSU(n)

    def process_operation(self, a: int, d: int, k: int) -> None:
        """Processes a single operation, connecting points in an arithmetic progression.

        Args:
            a (int): Starting point (1-indexed).
            d (int): Step size.
            k (int): Number of points in the progression.
        """
        # Convert to 0-based index for internal DSU usage
        indices = [a - 1 + i * d for i in range(k)]
        for i in range(1, len(indices)):
            self._dsu.union(indices[i - 1], indices[i])

    def get_connected_components(self) -> int:
        """Returns the number of connected components.

        Returns:
            int: Number of connected components.
        """
        return self._dsu.count_components()
