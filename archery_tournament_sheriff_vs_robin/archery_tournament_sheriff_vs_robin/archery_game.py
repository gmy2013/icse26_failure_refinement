## archery_game.py

from typing import List, Tuple
import numpy as np



class ArcheryGame:
    """Manages the archery game logic and provides query support.

    Attributes:
        _targets (np.ndarray): The array of target scores.
        _prefix_sums (np.ndarray): Prefix sums for fast subarray sum calculation.
    """

    def __init__(self, targets: List[int]) -> None:
        """Initializes the ArcheryGame with the given targets.

        Args:
            targets (List[int]): The list of target scores.
        """
        self._targets: np.ndarray = np.array(targets, dtype=np.int64)
        self._prefix_sums: np.ndarray = np.zeros(len(targets) + 1, dtype=np.int64)
        np.cumsum(self._targets, out=self._prefix_sums[1:])

    def can_sheriff_avoid_losing(self, l: int, r: int) -> bool:
        """Determines if the Sheriff can avoid losing in the subarray [l, r].

        Both players pick alternately from the subarray, starting with Robin.
        Each picks the highest remaining value. Sheriff avoids losing if his
        total is at least Robin's.

        Args:
            l (int): Left index (1-based, inclusive).
            r (int): Right index (1-based, inclusive).

        Returns:
            bool: True if Sheriff can avoid losing, False otherwise.
        """
        # Convert to 0-based indices
        left: int = l - 1
        right: int = r
        subarray: np.ndarray = self._targets[left:right]
        n: int = subarray.size

        if n == 0:
            # No targets to pick, Sheriff cannot lose
            return True

        # Sort in descending order for optimal pick sequence
        sorted_targets: np.ndarray = np.sort(subarray)[::-1]

        # Robin picks first, then Sheriff, alternate
        robin_total: int = np.sum(sorted_targets[0:n:2])
        sheriff_total: int = np.sum(sorted_targets[1:n:2])

        return sheriff_total >= robin_total


class QueryProcessor:
    """Processes a batch of queries for the ArcheryGame.

    Attributes:
        _game (ArcheryGame): The archery game instance.
    """

    def __init__(self, game: ArcheryGame) -> None:
        """Initializes the QueryProcessor with a game instance.

        Args:
            game (ArcheryGame): The archery game instance.
        """
        self._game: ArcheryGame = game

    def process_queries(self, queries: List[Tuple[int, int]]) -> List[bool]:
        """Processes a list of queries and returns the results.

        Args:
            queries (List[Tuple[int, int]]): List of (l, r) queries (1-based, inclusive).

        Returns:
            List[bool]: List of results for each query (True if Sheriff avoids losing).
        """
        results: List[bool] = []
        for l, r in queries:
            result: bool = self._game.can_sheriff_avoid_losing(l, r)
            results.append(result)
        return results
