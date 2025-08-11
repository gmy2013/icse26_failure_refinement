## battle_calculator.py

"""BattleCalculator module for efficient boss battle turn calculation.

This module provides the BattleCalculator class, which computes the minimum
number of turns required to defeat a boss given a set of attacks, each with
individual damage and cooldown values.

Classes:
    BattleCalculator: Core logic for boss battle calculation.
"""

import heapq
from typing import List


class BattleCalculator:
    """Calculates the minimum number of turns to defeat a boss.

    Methods:
        min_turns_to_defeat(h, damages, cooldowns): Returns minimum turns needed.
    """

    def __init__(self) -> None:
        """Initializes the BattleCalculator."""
        pass

    def min_turns_to_defeat(
        self,
        h: int,
        damages: List[int],
        cooldowns: List[int]
    ) -> int:
        """Calculates the minimum number of turns to defeat the boss.

        Args:
            h: The initial health of the boss.
            damages: List of attack damages.
            cooldowns: List of attack cooldowns (in turns).

        Returns:
            The minimum number of turns required to reduce the boss's health to zero or below.
        """
        if h <= 0:
            return 0
        if not damages or not cooldowns or len(damages) != len(cooldowns):
            raise ValueError("Damages and cooldowns must be non-empty and of equal length.")

        num_attacks: int = len(damages)
        # Each attack is represented as (next_available_turn, attack_index)
        # At the start, all attacks are available at turn 1.
        attack_heap: List[tuple[int, int]] = [
            (1, idx) for idx in range(num_attacks)
        ]
        heapq.heapify(attack_heap)

        # Track the next available turn for each attack.
        next_available_turns: List[int] = [1] * num_attacks

        current_turn: int = 1
        boss_health: int = h

        # To avoid unnecessary simulation, we process events in order of next available turn.
        while boss_health > 0:
            # Find the earliest turn when at least one attack is available.
            if not attack_heap:
                # Should not happen, as attacks always become available again.
                break
            current_turn = attack_heap[0][0]

            # Collect all attacks available at this turn.
            available_attacks: List[int] = []
            while attack_heap and attack_heap[0][0] == current_turn:
                _, attack_idx = heapq.heappop(attack_heap)
                available_attacks.append(attack_idx)

            # Sum the damage of all available attacks.
            total_damage: int = sum(damages[idx] for idx in available_attacks)
            boss_health -= total_damage

            if boss_health <= 0:
                return current_turn

            # Update the next available turn for each used attack and push back to heap.
            for idx in available_attacks:
                next_turn = current_turn + cooldowns[idx]
                next_available_turns[idx] = next_turn
                heapq.heappush(attack_heap, (next_turn, idx))

        # If the loop exits, boss is defeated at current_turn.
        return current_turn
