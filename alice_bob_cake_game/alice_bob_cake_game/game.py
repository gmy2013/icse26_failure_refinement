## game.py

from typing import List


class CakeGame:
    """Class to simulate the Alice and Bob cake game.

    Alice always picks the smallest available cake that is strictly greater than any she has previously eaten.
    Bob removes the most 'dangerous' cake (the one that would allow Alice to continue her sequence).
    """

    def __init__(self, cakes: List[int]) -> None:
        """Initializes the CakeGame with a list of cake sizes.

        Args:
            cakes: List of integers representing cake sizes.
        """
        self.cakes = sorted(cakes)

    def compute_alice_max_cakes(self) -> int:
        """Computes the maximum number of cakes Alice can eat under optimal play.

        Returns:
            The maximum number of cakes Alice can eat.
        """
        n = len(self.cakes)
        max_cakes = 0

        # Try every possible starting cake for Alice
        for start_idx in range(n):
            # Alice starts with cakes[start_idx]
            used = [False] * n
            used[start_idx] = True
            last_eaten = self.cakes[start_idx]
            alice_count = 1

            # Remaining cakes (indices not used)
            remaining_indices = set(i for i in range(n) if not used[i])

            while True:
                # Find the smallest cake strictly greater than last_eaten
                next_cake_idx = -1
                for i in range(n):
                    if not used[i] and self.cakes[i] > last_eaten:
                        next_cake_idx = i
                        break

                if next_cake_idx == -1:
                    # No more cakes Alice can eat
                    break

                # Bob's turn: remove the most dangerous cake for Alice
                # That is, the smallest cake strictly greater than last_eaten
                # If there are multiple, Bob removes the first one
                bob_remove_idx = -1
                for i in range(n):
                    if not used[i] and self.cakes[i] > last_eaten:
                        bob_remove_idx = i
                        break

                if bob_remove_idx == -1:
                    # No more cakes for Bob to remove, Alice can eat next
                    used[next_cake_idx] = True
                    last_eaten = self.cakes[next_cake_idx]
                    alice_count += 1
                    continue

                # Bob removes the cake
                used[bob_remove_idx] = True

                # After Bob's removal, check if Alice can still eat
                next_cake_idx = -1
                for i in range(n):
                    if not used[i] and self.cakes[i] > last_eaten:
                        next_cake_idx = i
                        break

                if next_cake_idx == -1:
                    # No more cakes Alice can eat
                    break

                # Alice eats the next available cake
                used[next_cake_idx] = True
                last_eaten = self.cakes[next_cake_idx]
                alice_count += 1

            if alice_count > max_cakes:
                max_cakes = alice_count

        return max_cakes
