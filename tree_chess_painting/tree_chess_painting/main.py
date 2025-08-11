## main.py

import sys
import threading
from collections import deque
from typing import List, Tuple, Dict

class TreeChessPainter:
    """Class to compute the minimum steps to paint all vertices blue in a tree."""

    def __init__(self, n: int, a: int, b: int, edges: List[Tuple[int, int]]) -> None:
        """
        Initializes the tree and the starting positions of the two chess pieces.

        Args:
            n: Number of vertices in the tree.
            a: Starting vertex of P_A (1-based index).
            b: Starting vertex of P_B (1-based index).
            edges: List of edges, each as a tuple (u, v).
        """
        self.n: int = n
        self.a: int = a
        self.b: int = b
        self.adj: Dict[int, List[int]] = {i: [] for i in range(1, n + 1)}
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)

    def bfs(self, start: int) -> Tuple[List[int], int]:
        """
        Performs BFS from the given start node.

        Args:
            start: The starting vertex for BFS.

        Returns:
            A tuple containing:
                - dist: List where dist[i] is the distance from start to vertex i (1-based).
                - farthest_node: The vertex farthest from start.
        """
        dist: List[int] = [-1] * (self.n + 1)
        queue: deque = deque()
        queue.append(start)
        dist[start] = 0
        farthest_node: int = start

        while queue:
            u = queue.popleft()
            for v in self.adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    queue.append(v)
                    if dist[v] > dist[farthest_node]:
                        farthest_node = v
        return dist, farthest_node

    def min_steps_to_paint_blue(self) -> int:
        """
        Computes the minimum number of steps required to paint all vertices blue.

        Returns:
            The minimum number of steps as an integer.
        """
        # Step 1: Find the farthest node from P_A's starting position.
        dist_a, farthest_from_a = self.bfs(self.a)
        # Step 2: Find the farthest node from that node (tree diameter).
        dist_far, _ = self.bfs(farthest_from_a)
        tree_diameter: int = max(dist_far[1:])

        # Step 3: Compute the distance from P_A to P_B's starting position.
        dist_a_to_b: int = dist_a[self.b]

        # The minimum steps is the maximum of:
        # - The time for P_A to reach the farthest node (tree_diameter)
        # - The time for P_B to catch up with P_A (dist_a_to_b)
        # Since P_B can only paint blue after P_A paints red, the answer is
        # min(tree_diameter, dist_a_to_b * 2)
        # But in the problem, the optimal is to take the minimum of tree_diameter and 2*dist_a_to_b,
        # because if P_B can catch up before P_A reaches the farthest node, the process is limited by P_B's speed.

        return min(tree_diameter, dist_a_to_b * 2)

class Main:
    """Main class to handle input/output and invoke the solution."""

    @staticmethod
    def main() -> None:
        """
        Main function to parse input, process test cases, and print results.
        """
        import sys

        sys.setrecursionlimit(1 << 25)
        input = sys.stdin.readline

        t_line = ''
        while t_line.strip() == '':
            t_line = input()
        t = int(t_line.strip())
        results: List[int] = []

        for _ in range(t):
            # Read n, a, b
            while True:
                line = input()
                if line.strip():
                    n_a_b = list(map(int, line.strip().split()))
                    if len(n_a_b) == 3:
                        break
            n, a, b = n_a_b
            edges: List[Tuple[int, int]] = []
            edge_count = 0
            while edge_count < n - 1:
                line = input()
                if line.strip():
                    u, v = map(int, line.strip().split())
                    edges.append((u, v))
                    edge_count += 1
            painter = TreeChessPainter(n, a, b, edges)
            result = painter.min_steps_to_paint_blue()
            results.append(result)

        for res in results:
            print(res)


if __name__ == "__main__":
    threading.Thread(target=Main.main).start()
