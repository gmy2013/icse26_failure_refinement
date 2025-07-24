## main.py
"""
Efficient bitmask-based subset solver with intersection constraints.

Classes:
    SetEncoder: Provides set<->int bijection and popcount utility.
    ConstraintChecker: Checks if a subset S satisfies all intersection constraints.
    Solver: Finds all valid subsets S.
    Main: Handles input/output and program entry point.

Requires:
    numpy>=1.21.0
"""

import sys
import numpy as np
from typing import Set, List, Optional


class SetEncoder:
    """Utility for encoding/decoding sets as integers and popcount."""

    @staticmethod
    def encode(s: Set[int]) -> int:
        """Encodes a set of integers as a bitmask integer.

        Args:
            s: Set of integers (elements in 0..n-1).

        Returns:
            Integer bitmask representation.
        """
        result: int = 0
        for x in s:
            if x < 0:
                raise ValueError("Set elements must be non-negative integers.")
            result |= 1 << x
        return result

    @staticmethod
    def decode(x: int) -> Set[int]:
        """Decodes an integer bitmask to a set of integers.

        Args:
            x: Integer bitmask.

        Returns:
            Set of integers corresponding to set bits in x.
        """
        result: Set[int] = set()
        idx: int = 0
        while x:
            if x & 1:
                result.add(idx)
            x >>= 1
            idx += 1
        return result

    @staticmethod
    def popcount(x: int) -> int:
        """Counts the number of set bits (population count).

        Args:
            x: Integer.

        Returns:
            Number of set bits in x.
        """
        # Use numpy for fast popcount
        return int(np.binary_repr(x).count('1'))


class ConstraintChecker:
    """Checks if a subset S satisfies all intersection constraints."""

    def __init__(self, n: int, v_list: List[int]) -> None:
        """Initializes the checker.

        Args:
            n: Size of the ground set (elements 0..n-1).
            v_list: List of 2^n integers, each encoding allowed intersection sizes for subset T.
        """
        self.n: int = n
        self.V: List[Set[int]] = []
        self._precompute_allowed_sizes(v_list)

    def _precompute_allowed_sizes(self, v_list: List[int]) -> None:
        """Precomputes allowed intersection sizes for each T.

        Args:
            v_list: List of 2^n integers, each as a bitmask of allowed sizes.
        """
        for v in v_list:
            allowed: Set[int] = set()
            for k in range(self.n + 1):
                if (v >> k) & 1:
                    allowed.add(k)
            self.V.append(allowed)

    def is_valid(self, S: int) -> bool:
        """Checks if subset S (as bitmask) satisfies all constraints.

        Args:
            S: Subset encoded as integer bitmask.

        Returns:
            True if S is valid, False otherwise.
        """
        # For all non-empty T in 1..2^n-1
        for T in range(1, 1 << self.n):
            intersection_size: int = SetEncoder.popcount(S & T)
            allowed_sizes: Set[int] = self.V[T]
            if intersection_size not in allowed_sizes:
                return False
        return True


class Solver:
    """Finds all valid subsets S."""

    def __init__(self, n: int, v_list: List[int]) -> None:
        """Initializes the solver.

        Args:
            n: Size of the ground set.
            v_list: List of 2^n integers encoding allowed intersection sizes.
        """
        self.n: int = n
        self.V: List[int] = v_list
        self.checker: ConstraintChecker = ConstraintChecker(n, v_list)

    def find_valid_subsets(self) -> List[int]:
        """Finds all valid subsets S.

        Returns:
            List of valid subsets S, each as an integer bitmask.
        """
        valid_subsets: List[int] = []
        for S in range(1 << self.n):
            if self.checker.is_valid(S):
                valid_subsets.append(S)
        return valid_subsets


class Main:
    """Handles input/output and program entry point."""

    @staticmethod
    def main() -> None:
        """Main entry point. Reads input, runs solver, prints output."""
        # Read input from stdin
        n: Optional[int] = None
        v_list: List[int] = []

        # Input format:
        # First line: n (integer)
        # Next 2^n lines: v_i (integer, bitmask of allowed intersection sizes for T=i)
        lines = [line.strip() for line in sys.stdin if line.strip()]
        if not lines:
            print("No input provided.", file=sys.stderr)
            sys.exit(1)
        n = int(lines[0])
        expected_lines = (1 << n)
        if len(lines) != expected_lines + 1:
            print(f"Expected {expected_lines} v_i lines after n, got {len(lines)-1}.", file=sys.stderr)
            sys.exit(1)
        for i in range(1, expected_lines + 1):
            v = int(lines[i])
            v_list.append(v)

        solver = Solver(n, v_list)
        valid_subsets = solver.find_valid_subsets()

        # Output: print each valid S as an integer, one per line
        for S in valid_subsets:
            print(S)


if __name__ == "__main__":
    Main.main()
