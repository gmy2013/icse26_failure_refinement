## berland_card_game.py

from typing import List
from combinatorics import Combinatorics

class BerlandCardGame:
    """Implements logic for the Berland card game combinatorial problem.

    Attributes:
        n (int): Number of distinct card values.
        m (int): Number of cards per player (must be even).
        combinatorics (Combinatorics): Instance for combinatorial calculations.
    """

    def __init__(self, n: int, m: int, combinatorics: Combinatorics = None) -> None:
        """Initializes the BerlandCardGame.

        Args:
            n (int): Number of distinct card values.
            m (int): Number of cards per player (must be even).
            combinatorics (Combinatorics, optional): Combinatorics instance. If None, a default is created.
        """
        self.n: int = n
        self.m: int = m
        self.combinatorics: Combinatorics = combinatorics if combinatorics is not None else Combinatorics(max_n=2 * n, mod=10**9 + 7)

    def count_valid_distributions(self) -> int:
        """Counts the number of valid card distributions such that the first player can always beat the second player.

        Returns:
            int: The number of valid distributions modulo combinatorics.mod.
        """
        # The problem is: Given 2n cards (n distinct values, 2 of each), split into two hands of n cards each,
        # such that for every i, the i-th card of the first player is strictly greater than the i-th card of the second player.
        #
        # This is a classic combinatorial problem: the number of ways to split 2n cards (with 2 of each value)
        # into two hands of n cards each, so that the first player's hand is strictly greater than the second's
        # in every position (after sorting both hands).
        #
        # The answer is the n-th Catalan number: C_n = (2n)! / (n! * (n+1)!)
        #
        # For general m (even), and n = m // 2, the answer is Catalan(n).
        #
        # If m is not even, or n < 1, return 0.

        if self.m % 2 != 0 or self.m < 2 or self.n < 1 or self.n != self.m // 2:
            return 0

        catalan_n = self._catalan_number(self.n)
        return catalan_n

    def _catalan_number(self, n: int) -> int:
        """Computes the n-th Catalan number modulo combinatorics.mod.

        Args:
            n (int): The index of the Catalan number.

        Returns:
            int: The n-th Catalan number modulo combinatorics.mod.
        """
        # Catalan(n) = C(2n, n) // (n + 1)
        c_2n_n = self.combinatorics.nCr(2 * n, n)
        mod = self.combinatorics.mod
        inv_n_plus_1 = pow(n + 1, mod - 2, mod)
        catalan = (c_2n_n * inv_n_plus_1) % mod
        return catalan

    def can_first_player_win(self, p1_cards: List[int], p2_cards: List[int]) -> bool:
        """Checks if the first player's hand can always beat the second player's hand.

        Args:
            p1_cards (List[int]): The first player's hand.
            p2_cards (List[int]): The second player's hand.

        Returns:
            bool: True if the first player can always beat the second player, False otherwise.
        """
        # Sort both hands and compare each card
        p1_sorted = sorted(p1_cards)
        p2_sorted = sorted(p2_cards)
        for a, b in zip(p1_sorted, p2_sorted):
            if a <= b:
                return False
        return True
