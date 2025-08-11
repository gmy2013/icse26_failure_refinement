## casino.py

from typing import List, Optional


class Game:
    """Represents a single casino game with probability and winnings.

    Attributes:
        p (int): Probability of winning (1-100).
        w (int): Winnings if the game is won.
    """

    def __init__(self, p: int, w: int) -> None:
        """Initializes a Game instance.

        Args:
            p (int): Probability of winning (1-100).
            w (int): Winnings if the game is won.
        """
        self.p: int = p
        self.w: int = w

    def prob(self) -> float:
        """Returns the probability of winning as a float in [0, 1].

        Returns:
            float: Probability of winning.
        """
        return self.p / 100.0

    def expected_value(self) -> float:
        """Returns the expected value of this game.

        Returns:
            float: Expected value (w * p/100).
        """
        return self.w * self.prob()


class CasinoMaxExpectedValue:
    """Encapsulates logic to maximize expected value from a set of games.

    Attributes:
        games (List[Game]): List of Game instances.
    """

    def __init__(self, games: List[Game]) -> None:
        """Initializes with a list of games.

        Args:
            games (List[Game]): List of Game instances.
        """
        self.games: List[Game] = games

    def max_expected_value(self) -> float:
        """Computes the maximum expected value achievable by selecting a subset of games.

        Returns:
            float: The maximum expected value.
        """
        if not self.games:
            return 0.0

        # Sort games by decreasing w_i * (p_i/100) / (1 - p_i/100)
        # To avoid division by zero, handle p_i == 100 separately (always win)
        def sort_key(game: Game) -> float:
            prob = game.prob()
            if prob >= 1.0:
                return float('inf')
            return game.w * prob / (1.0 - prob)

        sorted_games = sorted(self.games, key=sort_key, reverse=True)

        max_ev: float = 0.0
        current_prob: float = 1.0
        current_sum: float = 0.0

        for game in sorted_games:
            prob = game.prob()
            current_prob *= prob
            current_sum += game.w
            ev = current_prob * current_sum
            if ev > max_ev:
                max_ev = ev
            else:
                # Adding this game does not increase expected value; stop.
                break

        return max_ev

    def select_optimal_subset(self) -> List[int]:
        """Returns the indices (in the original games list) of the optimal subset.

        Returns:
            List[int]: List of indices of selected games.
        """
        if not self.games:
            return []

        # Sort games and keep track of original indices
        indexed_games = list(enumerate(self.games))
        def sort_key(item) -> float:
            game = item[1]
            prob = game.prob()
            if prob >= 1.0:
                return float('inf')
            return game.w * prob / (1.0 - prob)

        sorted_indexed_games = sorted(indexed_games, key=sort_key, reverse=True)

        selected_indices: List[int] = []
        current_prob: float = 1.0
        current_sum: float = 0.0
        max_ev: float = 0.0

        for idx, game in sorted_indexed_games:
            prob = game.prob()
            current_prob *= prob
            current_sum += game.w
            ev = current_prob * current_sum
            if ev > max_ev:
                selected_indices.append(idx)
                max_ev = ev
            else:
                break

        # Return indices in the order as in the original input
        selected_indices.sort()
        return selected_indices
