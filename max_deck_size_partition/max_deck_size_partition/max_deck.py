## max_deck.py


from typing import List, Tuple

class MaxDeckSolver:
    """Solver for the maximum deck size problem."""

    def solve(self, test_cases: List[Tuple[int, int, List[int]]]) -> List[int]:
        """Solves all test cases and returns a list of maximum deck sizes.

        Args:
            test_cases: A list of tuples, each containing:
                - n: number of card types
                - k: number of cards that can be purchased
                - a: list of counts of each card type

        Returns:
            A list of integers, each representing the maximum deck size for a test case.
        """
        results: List[int] = []
        for n, k, a in test_cases:
            max_size = self._max_deck_size(n, k, a)
            results.append(max_size)
        return results

    def _max_deck_size(self, n: int, k: int, a: List[int]) -> int:
        """Finds the maximum possible deck size using binary search.

        Args:
            n: Number of card types.
            k: Number of cards that can be purchased.
            a: List of counts of each card type.

        Returns:
            The maximum deck size that can be formed.
        """
        left: int = 1
        right: int = sum(a) + k
        answer: int = 0

        while left <= right:
            mid: int = (left + right) // 2
            if self._can_form_decks(mid, n, k, a):
                answer = mid
                left = mid + 1
            else:
                right = mid - 1
        return answer

    def _can_form_decks(self, d: int, n: int, k: int, a: List[int]) -> bool:
        """Checks if it is possible to form d decks with the given cards and purchases.

        Args:
            d: Target deck size.
            n: Number of card types.
            k: Number of cards that can be purchased.
            a: List of counts of each card type.

        Returns:
            True if possible, False otherwise.
        """
        # For each card type, the maximum number of cards that can be used in d decks is at most d
        # (since no deck can have duplicate card values).
        # For each card type, if a[i] < d, we need (d - a[i]) more cards of this type.
        # The total number of extra cards needed must not exceed k.
        total_needed: int = 0
        for count in a:
            if count < d:
                total_needed += d - count
        return total_needed <= k

