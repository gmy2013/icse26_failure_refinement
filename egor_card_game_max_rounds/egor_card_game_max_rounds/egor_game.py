## egor_game.py

from typing import List


class EgorGame:
    """Implements the logic for the Egor card game.

    Provides a method to compute the maximum number of contiguous, non-overlapping
    segments (rounds) such that the sum of each segment is within [l, r].
    """

    @staticmethod
    def max_winning_rounds(
        n: int, l: int, r: int, cards: List[int], verbose: bool = False
    ) -> int:
        """Calculates the maximum number of winning rounds.

        Args:
            n: Number of cards in the deck.
            l: Lower bound of the sum for a valid round.
            r: Upper bound of the sum for a valid round.
            cards: List of integers representing the card values.
            verbose: If True, prints step-by-step window movements and segment choices.

        Returns:
            The maximum number of rounds that can be won.
        """
        left: int = 0
        right: int = 0
        current_sum: int = 0
        rounds: int = 0

        while left < n:
            # Expand the window to include at least one card
            if right < left:
                right = left
                current_sum = 0

            # Expand right pointer to reach at least l
            while right < n and current_sum < l:
                current_sum += cards[right]
                right += 1
                if verbose:
                    print(
                        f"Expanding window: left={left}, right={right}, "
                        f"current_sum={current_sum}"
                    )

            # If current_sum is within [l, r], we found a valid segment
            if l <= current_sum <= r:
                rounds += 1
                if verbose:
                    print(
                        f"Found valid segment: [{left}, {right - 1}], "
                        f"sum={current_sum}, total_rounds={rounds}"
                    )
                left = right
                current_sum = 0
            # If current_sum > r, need to shrink from the left
            elif current_sum > r:
                if verbose:
                    print(
                        f"Sum exceeded r: current_sum={current_sum} > r={r}, "
                        f"shrinking window from left"
                    )
                current_sum -= cards[left]
                left += 1
            # If we reached the end and can't form a valid segment
            else:
                break

        if verbose:
            print(f"Total rounds won: {rounds}")
        return rounds
