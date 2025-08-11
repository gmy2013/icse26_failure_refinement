## main.py

from typing import List
from sortedcontainers import SortedList
import sys

class SegmentTree:
    """Segment Tree supporting range queries for top 6 largest elements.

    Attributes:
        n (int): Number of elements in the original data.
        tree (List[List[int]]): Segment tree nodes, each storing up to 6 largest elements in its range.
    """

    def __init__(self, data: List[int]) -> None:
        """Initializes the segment tree with the given data.

        Args:
            data (List[int]): The list of stick lengths.
        """
        self.n = len(data)
        self.tree = [list() for _ in range(self.n * 2)]
        # Initialize leaves
        for i in range(self.n):
            self.tree[self.n + i] = [data[i]]
        # Build the tree
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self._merge_top_k(self.tree[i << 1], self.tree[i << 1 | 1], 6)

    def query(self, l: int, r: int) -> List[int]:
        """Queries the range [l, r) for the top 6 largest elements.

        Args:
            l (int): Left index (inclusive, 0-based).
            r (int): Right index (exclusive, 0-based).

        Returns:
            List[int]: Up to 6 largest elements in the range, sorted descending.
        """
        l += self.n
        r += self.n
        res: List[int] = []
        while l < r:
            if l & 1:
                res = self._merge_top_k(res, self.tree[l], 6)
                l += 1
            if r & 1:
                r -= 1
                res = self._merge_top_k(res, self.tree[r], 6)
            l >>= 1
            r >>= 1
        return sorted(res, reverse=True)

    @staticmethod
    def _merge_top_k(a: List[int], b: List[int], k: int) -> List[int]:
        """Merges two sorted lists and returns the top k largest elements.

        Args:
            a (List[int]): First list, sorted descending.
            b (List[int]): Second list, sorted descending.
            k (int): Number of top elements to return.

        Returns:
            List[int]: Merged list of up to k largest elements, sorted descending.
        """
        i, j = 0, 0
        merged: List[int] = []
        while len(merged) < k and (i < len(a) or j < len(b)):
            if i < len(a) and (j >= len(b) or a[i] >= b[j]):
                merged.append(a[i])
                i += 1
            elif j < len(b):
                merged.append(b[j])
                j += 1
        return merged

class TriangleChecker:
    """Checks if two non-degenerate triangles can be formed from 6 distinct sticks in a range.

    Attributes:
        segment_tree (SegmentTree): Segment tree for efficient range queries.
    """

    def __init__(self, stick_lengths: List[int]) -> None:
        """Initializes the TriangleChecker with stick lengths.

        Args:
            stick_lengths (List[int]): List of stick lengths.
        """
        self.segment_tree = SegmentTree(stick_lengths)

    def can_form_two_triangles(self, l: int, r: int) -> bool:
        """Checks if two non-degenerate triangles can be formed from 6 distinct sticks in [l, r).

        Args:
            l (int): Left index (inclusive, 0-based).
            r (int): Right index (exclusive, 0-based).

        Returns:
            bool: True if possible, False otherwise.
        """
        top6 = self.segment_tree.query(l, r)
        if len(top6) < 6:
            return False
        # Try all possible ways to split 6 sticks into two disjoint triplets
        # Each triplet must form a triangle (triangle inequality)
        # There are 20 ways to split 6 elements into two triplets
        indices = [0, 1, 2, 3, 4, 5]
        from itertools import combinations
        triplet_indices = list(combinations(indices, 3))
        used = set()
        for first in triplet_indices:
            first_set = set(first)
            second = tuple(i for i in indices if i not in first_set)
            # To avoid duplicate checking, sort the two triplets
            key = tuple(sorted([tuple(sorted(first)), tuple(sorted(second))]))
            if key in used:
                continue
            used.add(key)
            a = [top6[i] for i in first]
            b = [top6[i] for i in second]
            if self._is_triangle(a) and self._is_triangle(b):
                return True
        return False

    @staticmethod
    def _is_triangle(sides: List[int]) -> bool:
        """Checks if the three sides can form a non-degenerate triangle.

        Args:
            sides (List[int]): List of three side lengths.

        Returns:
            bool: True if they can form a triangle, False otherwise.
        """
        sides = sorted(sides)
        return sides[0] + sides[1] > sides[2]

class MainApp:
    """Main application class for processing input and output."""

    def __init__(self) -> None:
        """Initializes the MainApp."""
        self.triangle_checker: TriangleChecker = None

    def run(self) -> None:
        """Runs the main application loop."""
        input = sys.stdin.readline
        n = int(input())
        stick_lengths = list(map(int, input().split()))
        q = int(input())
        self.triangle_checker = TriangleChecker(stick_lengths)
        for _ in range(q):
            l_str, r_str = input().split()
            l = int(l_str) - 1  # Convert to 0-based index
            r = int(r_str)      # Exclusive
            if r - l < 6:
                print("NO")
                continue
            if self.triangle_checker.can_form_two_triangles(l, r):
                print("YES")
            else:
                print("NO")

if __name__ == "__main__":
    app = MainApp()
    app.run()
