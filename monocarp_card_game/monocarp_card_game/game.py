## game.py

from collections import Counter
from bisect import bisect_left, bisect_right
from typing import List, Tuple


class CardGame:
    """Encapsulates the logic for maximizing the number of cards Monocarp can take.

    Attributes:
        n (int): Number of cards.
        k (int): Maximum number of distinct numbers Monocarp can take.
        cards (List[int]): List of card numbers.
    """

    def __init__(self, n: int, k: int, cards: List[int]) -> None:
        """Initializes the CardGame with the given parameters.

        Args:
            n (int): Number of cards.
            k (int): Maximum number of distinct numbers Monocarp can take.
            cards (List[int]): List of card numbers.
        """
        self.n: int = n
        self.k: int = k
        self.cards: List[int] = cards

    def max_cards(self) -> int:
        """Calculates the maximum number of cards Monocarp can take.

        Returns:
            int: The maximum number of cards that can be taken.
        """
        if self.k == 0 or self.n == 0:
            return 0

        freq_counter: Counter = Counter(self.cards)
        unique_numbers: List[int] = sorted(freq_counter.keys())
        freq_list: List[int] = [freq_counter[num] for num in unique_numbers]
        total_unique: int = len(unique_numbers)

        max_sum: int = 0
        window_sum: int = 0
        left: int = 0

        for right in range(total_unique):
            # Expand window to include unique_numbers[right]
            window_sum += freq_list[right]

            # Shrink window from the left if window size exceeds k
            while right - left + 1 > self.k:
                window_sum -= freq_list[left]
                left += 1

            # Check if the window is valid (consecutive numbers)
            if unique_numbers[right] - unique_numbers[left] == right - left:
                max_sum = max(max_sum, window_sum)

        return max_sum


class GameManager:
    """Manages multiple test cases for the card game."""

    def __init__(self) -> None:
        """Initializes the GameManager."""
        pass

    def process_test_cases(
        self, test_cases: List[Tuple[int, int, List[int]]]
    ) -> List[int]:
        """Processes multiple test cases.

        Args:
            test_cases (List[Tuple[int, int, List[int]]]): List of test cases, each as (n, k, cards).

        Returns:
            List[int]: List of results for each test case.
        """
        results: List[int] = []
        for n, k, cards in test_cases:
            game = CardGame(n, k, cards)
            result = game.max_cards()
            results.append(result)
        return results
