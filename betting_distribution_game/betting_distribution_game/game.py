## game.py

from typing import List, Union


class BettingGame:
    """Core logic for finding valid bet distributions in the betting game."""

    def __init__(self) -> None:
        """Initialize the BettingGame instance."""
        pass

    def find_bet_distribution(
        self, n: int, multipliers: List[int]
    ) -> Union[List[int], int]:
        """
        Find a valid bet distribution for the given multipliers.

        Args:
            n: Number of outcomes.
            multipliers: List of integer multipliers for each outcome.

        Returns:
            A list of integer bets (length n) if a valid distribution exists,
            or -1 if impossible.
        """
        # If all multipliers are 2, it's impossible
        if all(k == 2 for k in multipliers):
            return -1

        # Find the index of the maximum multiplier
        max_k = max(multipliers)
        max_idx = multipliers.index(max_k)

        # Set all bets to 1 initially
        bets = [1] * n

        # Calculate the sum of all bets except the one with the largest multiplier
        sum_others = n - 1

        # For the outcome with the largest multiplier, set its bet to the minimal value
        # such that for all i: k_i * x_i > sum(x_j for all j)
        # For i == max_idx: k_max * x_max > sum_others + x_max
        # => (k_max - 1) * x_max > sum_others
        # => x_max > sum_others / (k_max - 1)
        # We take the minimal integer greater than this value

        if max_k == 1:
            # If any multiplier is 1, it's impossible (since 1 * x <= sum(x_j))
            return -1

        x_max = sum_others // (max_k - 1) + 1
        bets[max_idx] = x_max

        # Now, check for all i that k_i * x_i > sum(bets)
        total_bets = sum(bets)
        for i in range(n):
            if multipliers[i] * bets[i] <= total_bets:
                return -1

        return bets
