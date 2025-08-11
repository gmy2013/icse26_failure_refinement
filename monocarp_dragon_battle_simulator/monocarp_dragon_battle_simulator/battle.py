## battle.py

from typing import List, Dict, Any
from sortedcontainers import SortedList


class BattleSimulator:
    """Simulates battles by optimally assigning artifacts to heroes and computing survivable rounds.

    Attributes:
        heroes (SortedList): Sorted list of hero health values (int).
        artifacts (SortedList): Sorted list of artifact durability values (int).
    """

    def __init__(self) -> None:
        """Initializes the BattleSimulator with empty hero and artifact lists."""
        self.heroes: SortedList[int] = SortedList()
        self.artifacts: SortedList[int] = SortedList()

    def add_hero(self, health: int) -> None:
        """Adds a hero with the specified health to the army.

        Args:
            health (int): The health value of the hero to add.
        """
        self.heroes.add(health)

    def add_artifact(self, durability: int) -> None:
        """Adds an artifact with the specified durability to the collection.

        Args:
            durability (int): The durability value of the artifact to add.
        """
        self.artifacts.add(durability)

    def max_survivable_rounds(self) -> int:
        """Calculates the maximum number of rounds the current army can survive.

        Returns:
            int: The maximum number of rounds survivable (integer, floor).
        """
        left: int = 0
        right: int = 10 ** 18  # Large upper bound for binary search
        answer: int = 0

        while left <= right:
            mid: int = (left + right) // 2
            if self._simulate(mid):
                answer = mid
                left = mid + 1
            else:
                right = mid - 1
        return answer

    def _simulate(self, rounds: int) -> bool:
        """Simulates the battle for a given number of rounds.

        Args:
            rounds (int): Number of rounds to simulate.

        Returns:
            bool: True if all heroes can survive for 'rounds' rounds, False otherwise.
        """
        if not self.heroes or not self.artifacts:
            return False

        num_pairs: int = min(len(self.heroes), len(self.artifacts))
        # Pair strongest heroes with strongest artifacts
        # Both lists are sorted ascending, so take from the end
        for i in range(1, num_pairs + 1):
            hero_health: int = self.heroes[-i]
            artifact_durability: int = self.artifacts[-i]
            if hero_health < rounds or artifact_durability < rounds:
                return False
        return True

    def get_army_state(self) -> Dict[str, Any]:
        """Returns the current state of the army.

        Returns:
            dict: Dictionary with lists of hero healths and artifact durabilities.
        """
        return {
            "heroes": list(self.heroes),
            "artifacts": list(self.artifacts)
        }
