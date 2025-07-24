## game.py

from typing import List, Tuple, Set, Dict
import bisect
from collections import defaultdict

class Game:
    """Encapsulates the logic for a single grid chip-cutting game."""

    def __init__(
        self,
        a: int,
        b: int,
        n: int,
        m: int,
        chips: List[Tuple[int, int]],
        moves: List[Tuple[str, int]]
    ) -> None:
        """
        Initializes the game state.

        Args:
            a: Number of rows in the grid.
            b: Number of columns in the grid.
            n: Number of chips.
            m: Number of moves.
            chips: List of (row, col) positions of chips (1-based).
            moves: List of (direction, index) moves. Direction is 'R' or 'C'.
        """
        self.a: int = a
        self.b: int = b
        self.n: int = n
        self.m: int = m
        self.chips: List[Tuple[int, int]] = chips
        self.moves: List[Tuple[str, int]] = moves

        # Grid boundaries (inclusive)
        self.row_start: int = 1
        self.row_end: int = a
        self.col_start: int = 1
        self.col_end: int = b

        # Set of (row, col) for fast lookup
        self.chip_set: Set[Tuple[int, int]] = set(chips)

        # Map row -> set of columns with chips
        self.row_to_cols: Dict[int, Set[int]] = defaultdict(set)
        # Map col -> set of rows with chips
        self.col_to_rows: Dict[int, Set[int]] = defaultdict(set)

        for r, c in chips:
            self.row_to_cols[r].add(c)
            self.col_to_rows[c].add(r)

        # Sorted list of rows and columns with chips (for bisect)
        self.sorted_rows: List[int] = sorted(self.row_to_cols.keys())
        self.sorted_cols: List[int] = sorted(self.col_to_rows.keys())

        self.alice_score: int = 0
        self.bob_score: int = 0

    def process_moves(self) -> Tuple[int, int]:
        """
        Processes all moves and returns the final scores.

        Returns:
            Tuple of (alice_score, bob_score)
        """
        turn_alice: bool = True  # Alice starts first

        for move in self.moves:
            direction, index = move
            if direction == 'R':
                collected = self._cut_rows(index, index)
            elif direction == 'C':
                collected = self._cut_cols(index, index)
            else:
                # Invalid move direction, skip
                collected = 0

            if turn_alice:
                self.alice_score += collected
            else:
                self.bob_score += collected

            turn_alice = not turn_alice

        return self.alice_score, self.bob_score

    def _cut_rows(self, start: int, end: int) -> int:
        """
        Removes all chips in rows [start, end] within current grid boundaries.

        Args:
            start: Start row (inclusive).
            end: End row (inclusive).

        Returns:
            Number of chips collected in this cut.
        """
        # Only cut if within current grid
        if start < self.row_start or end > self.row_end:
            return 0

        # Find all rows in [start, end] that have chips
        left = bisect.bisect_left(self.sorted_rows, start)
        right = bisect.bisect_right(self.sorted_rows, end)
        rows_to_remove = self.sorted_rows[left:right]

        collected = 0
        for r in rows_to_remove:
            # Only consider columns within current col boundaries
            cols = [c for c in self.row_to_cols[r] if self.col_start <= c <= self.col_end]
            for c in cols:
                self.chip_set.discard((r, c))
                self.col_to_rows[c].discard(r)
                if not self.col_to_rows[c]:
                    # Remove column from sorted_cols if no more chips
                    idx = bisect.bisect_left(self.sorted_cols, c)
                    if idx < len(self.sorted_cols) and self.sorted_cols[idx] == c:
                        self.sorted_cols.pop(idx)
                    del self.col_to_rows[c]
                collected += 1
            # Remove row from row_to_cols and sorted_rows
            self.row_to_cols[r].difference_update(cols)
            if not self.row_to_cols[r]:
                idx = bisect.bisect_left(self.sorted_rows, r)
                if idx < len(self.sorted_rows) and self.sorted_rows[idx] == r:
                    self.sorted_rows.pop(idx)
                del self.row_to_cols[r]

        # Update grid boundary
        if start == self.row_start:
            self.row_start += 1
        elif end == self.row_end:
            self.row_end -= 1
        # If cut is not at the edge, do not update boundaries

        return collected

    def _cut_cols(self, start: int, end: int) -> int:
        """
        Removes all chips in columns [start, end] within current grid boundaries.

        Args:
            start: Start column (inclusive).
            end: End column (inclusive).

        Returns:
            Number of chips collected in this cut.
        """
        # Only cut if within current grid
        if start < self.col_start or end > self.col_end:
            return 0

        # Find all columns in [start, end] that have chips
        left = bisect.bisect_left(self.sorted_cols, start)
        right = bisect.bisect_right(self.sorted_cols, end)
        cols_to_remove = self.sorted_cols[left:right]

        collected = 0
        for c in cols_to_remove:
            # Only consider rows within current row boundaries
            rows = [r for r in self.col_to_rows[c] if self.row_start <= r <= self.row_end]
            for r in rows:
                self.chip_set.discard((r, c))
                self.row_to_cols[r].discard(c)
                if not self.row_to_cols[r]:
                    idx = bisect.bisect_left(self.sorted_rows, r)
                    if idx < len(self.sorted_rows) and self.sorted_rows[idx] == r:
                        self.sorted_rows.pop(idx)
                    del self.row_to_cols[r]
                collected += 1
            # Remove col from col_to_rows and sorted_cols
            self.col_to_rows[c].difference_update(rows)
            if not self.col_to_rows[c]:
                idx = bisect.bisect_left(self.sorted_cols, c)
                if idx < len(self.sorted_cols) and self.sorted_cols[idx] == c:
                    self.sorted_cols.pop(idx)
                del self.col_to_rows[c]

        # Update grid boundary
        if start == self.col_start:
            self.col_start += 1
        elif end == self.col_end:
            self.col_end -= 1
        # If cut is not at the edge, do not update boundaries

        return collected
