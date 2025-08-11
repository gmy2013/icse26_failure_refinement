## game.py

from typing import List, Tuple, Dict, Optional

class FractionMod:
    """Fraction under modulo arithmetic."""

    def __init__(self, numerator: int, denominator: int, mod: int) -> None:
        self.numerator = numerator % mod
        self.denominator = denominator % mod
        self.mod = mod

    def value(self) -> int:
        """Return the integer value of the fraction modulo mod."""
        if self.denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero in modular division.")
        return (self.numerator * pow(self.denominator, self.mod - 2, self.mod)) % self.mod

    def mul(self, other: 'FractionMod') -> 'FractionMod':
        """Multiply two fractions under modulo."""
        return FractionMod(
            (self.numerator * other.numerator) % self.mod,
            (self.denominator * other.denominator) % self.mod,
            self.mod
        )

    def add(self, other: 'FractionMod') -> 'FractionMod':
        """Add two fractions under modulo."""
        numerator = (self.numerator * other.denominator + other.numerator * self.denominator) % self.mod
        denominator = (self.denominator * other.denominator) % self.mod
        return FractionMod(numerator, denominator, self.mod)


class DPState:
    """Memoization for DP states."""

    def __init__(self) -> None:
        self.memo: Dict[Tuple[int, int, int, int], Tuple[int, int, int, int]] = {}

    def get(self, state: Tuple[int, int, int, int]) -> Optional[Tuple[int, int, int, int]]:
        return self.memo.get(state, None)

    def set(self, state: Tuple[int, int, int, int], value: Tuple[int, int, int, int]) -> None:
        self.memo[state] = value


class Game:
    """
    Game logic for Alice and Bob's special balls game.

    Attributes:
        n: Number of balls.
        k: Number of special balls.
        values: List of ball values.
        mod: Modulo for arithmetic.
    """

    def __init__(self, n: int, k: int, values: List[int], mod: int = 10 ** 9 + 7) -> None:
        self.n = n
        self.k = k
        self.values = values
        self.mod = mod
        self.dp_state = DPState()
        self.total_sum = sum(values) % mod

    def expected_scores(self) -> Tuple[int, int]:
        """
        Compute expected scores for Alice and Bob.

        Returns:
            Tuple of (alice_score, bob_score), both modulo self.mod.
        """
        # balls_mask: bitmask of remaining balls (1 means present)
        # turn: 0 for Alice, 1 for Bob
        # special_mask: bitmask of special balls (1 means special)
        # extra_turn: 1 if current player has an extra turn, else 0

        # For efficiency, we use a compressed state:
        # (balls_mask, turn, extra_turn)
        # Since the special balls are always the first k balls, we can check if a ball is special by index.

        # To avoid TLE for large n, we use a DP with memoization and only store states that are reached.

        def dp(balls_mask: int, turn: int, extra_turn: int) -> Tuple[int, int]:
            # Returns (alice_score, bob_score) as expected sum for each player
            state = (balls_mask, turn, extra_turn, 0)
            memoized = self.dp_state.get(state)
            if memoized is not None:
                return memoized[:2]

            remaining = [i for i in range(self.n) if (balls_mask >> i) & 1]
            if not remaining:
                # No balls left
                return (0, 0)

            num_balls = len(remaining)
            inv_num_balls = pow(num_balls, self.mod - 2, self.mod)

            alice_total = 0
            bob_total = 0

            for idx in remaining:
                value = self.values[idx]
                is_special = idx < self.k

                next_mask = balls_mask ^ (1 << idx)
                # If special, current player gets another turn
                if is_special:
                    next_turn = turn
                    next_extra = 1
                else:
                    next_turn = 1 - turn
                    next_extra = 0

                next_alice, next_bob = dp(next_mask, next_turn, next_extra)
                if turn == 0:
                    # Alice's turn
                    alice_score = (value + next_alice) % self.mod
                    bob_score = next_bob
                else:
                    alice_score = next_alice
                    bob_score = (value + next_bob) % self.mod

                alice_total = (alice_total + alice_score) % self.mod
                bob_total = (bob_total + bob_score) % self.mod

            # Take expected value over all choices
            alice_exp = (alice_total * inv_num_balls) % self.mod
            bob_exp = (bob_total * inv_num_balls) % self.mod

            self.dp_state.set(state, (alice_exp, bob_exp, 0, 0))
            return (alice_exp, bob_exp)

        # All balls present at start
        full_mask = (1 << self.n) - 1
        alice_score, bob_score = dp(full_mask, 0, 0)
        return (alice_score, bob_score)
