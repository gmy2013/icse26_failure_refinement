## attack_plan.py

"""
Attack plan solver module.

Implements the AttackPlanSolver class, which computes the number of minimal-length attack plans
to capture all towers, given their coordinates and geometric rules.

Depends on:
    - geometry.py (Geometry class)
    - numpy (for efficient array operations)
"""

from typing import List, Tuple, Set, FrozenSet, Dict, Optional
import numpy as np
from geometry import Geometry


class AttackPlanSolver:
    """Solver for enumerating minimal-length attack plans for capturing all towers."""

    def __init__(self, points: List[Tuple[float, float]], mod: int = 998244353) -> None:
        """Initialize the solver.

        Args:
            points: List of (x, y) tuples representing tower coordinates.
            mod: Modulo for result (default: 998244353).
        """
        self.n: int = len(points)
        self.points: List[Tuple[float, float]] = points
        self.mod: int = mod
        self.geometry: Geometry = Geometry()
        self._dp_cache: Dict[FrozenSet[int], Tuple[int, List[List[int]]]] = {}

    def count_minimal_attack_plans(self) -> Tuple[int, List[int]]:
        """Count the number of minimal-length attack plans and return a sample plan.

        Returns:
            (num_plans, sample_plan): num_plans is the number of minimal-length plans modulo mod,
            sample_plan is a list of attack steps (each step is a list of 3 indices, 0-based).
            If impossible, returns (0, []).
        """
        # Start with no towers owned
        owned: FrozenSet[int] = frozenset()
        num_steps, plans = self._dp(owned)
        if num_steps == float('inf') or not plans:
            return 0, []
        # Return the number of plans and one sample plan (flattened)
        num_plans = len(plans) % self.mod
        sample_plan = plans[0] if plans else []
        return num_plans, sample_plan

    def _can_capture(self, p_idx: int, q_idx: int, r_idx: int, owned: Set[int]) -> Optional[Set[int]]:
        """Check if attacking triangle (p, q, r) can capture new towers.

        Args:
            p_idx, q_idx, r_idx: Indices of the triangle vertices.
            owned: Set of currently owned tower indices.

        Returns:
            Set of newly captured tower indices if valid, else None.
        """
        triangle = [p_idx, q_idx, r_idx]
        # All three must be owned
        if not all(idx in owned for idx in triangle):
            return None
        # Find all towers strictly inside the triangle and not yet owned
        captured = set()
        a, b, c = self.points[p_idx], self.points[q_idx], self.points[r_idx]
        for idx in range(self.n):
            if idx in owned or idx in triangle:
                continue
            p = self.points[idx]
            if self.geometry.is_in_triangle(a, b, c, p):
                captured.add(idx)
        if not captured:
            return None  # Must capture at least one new tower
        # Check circumcircle: no other unowned tower is strictly inside
        try:
            center, radius = self.geometry.circumcircle(a, b, c)
        except ValueError:
            return None  # Degenerate triangle
        for idx in range(self.n):
            if idx in owned or idx in triangle or idx in captured:
                continue
            p = self.points[idx]
            if self.geometry.is_in_circle(a, b, c, p):
                return None  # Some other unowned tower is inside circumcircle
        return captured

    def _dp(self, owned: FrozenSet[int]) -> Tuple[int, List[List[int]]]:
        """Dynamic programming to compute minimal steps and plans from current owned set.

        Args:
            owned: frozenset of owned tower indices.

        Returns:
            (min_steps, plans): min_steps is the minimal number of steps to capture all towers,
            plans is a list of plans (each plan is a list of attack steps, each step is [p, q, r]).
        """
        if owned in self._dp_cache:
            return self._dp_cache[owned]

        if len(owned) == self.n:
            # All towers owned: done
            return 0, [[]]

        min_steps = float('inf')
        all_plans: List[List[int]] = []

        # Try all possible triangles formed by three owned towers
        owned_list = list(owned)
        if len(owned_list) < 3:
            # Not enough owned towers to form a triangle: impossible
            self._dp_cache[owned] = (float('inf'), [])
            return float('inf'), []

        for i in range(len(owned_list)):
            for j in range(i + 1, len(owned_list)):
                for k in range(j + 1, len(owned_list)):
                    p_idx, q_idx, r_idx = owned_list[i], owned_list[j], owned_list[k]
                    captured = self._can_capture(p_idx, q_idx, r_idx, set(owned))
                    if captured is None:
                        continue
                    # Proceed to next state
                    new_owned = frozenset(set(owned) | captured)
                    steps, plans = self._dp(new_owned)
                    if steps + 1 < min_steps:
                        min_steps = steps + 1
                        all_plans = []
                    if steps + 1 == min_steps:
                        # For each plan, prepend this attack step
                        for plan in plans:
                            all_plans.append([[p_idx, q_idx, r_idx]] + plan)

        self._dp_cache[owned] = (min_steps, all_plans)
        return min_steps, all_plans
