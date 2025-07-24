## main.py

from collections import defaultdict, deque
import sys
from typing import List, Tuple, Dict, Optional

class TestCase:
    """Represents a single test case with graph data."""

    def __init__(self, n: int, m: int, edges: List[Tuple[int, int, int]]) -> None:
        """
        Args:
            n: Number of houses (nodes).
            m: Number of roads (edges).
            edges: List of edges, each as (u, v, c) where c is 1 if NPC road, 0 otherwise.
        """
        self.n: int = n
        self.m: int = m
        self.edges: List[Tuple[int, int, int]] = edges


class NPCRoadGraph:
    """Graph representation for NPC roads, with Eulerian circuit utilities."""

    def __init__(self, n: int) -> None:
        """
        Args:
            n: Number of nodes in the graph.
        """
        self.n: int = n
        # Adjacency list: node -> list of (neighbor, edge_id)
        self.adj: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
        # edge_id -> used flag
        self.edge_used: Dict[int, bool] = dict()
        # edge_id -> (u, v)
        self.edge_map: Dict[int, Tuple[int, int]] = dict()

    def add_edge(self, u: int, v: int, edge_id: int) -> None:
        """
        Adds an undirected edge to the graph.

        Args:
            u: One endpoint.
            v: Other endpoint.
            edge_id: Unique identifier for the edge.
        """
        self.adj[u].append((v, edge_id))
        self.adj[v].append((u, edge_id))
        self.edge_used[edge_id] = False
        self.edge_map[edge_id] = (u, v)

    def is_eulerian(self) -> bool:
        """
        Checks if the graph has an Eulerian circuit.

        Returns:
            True if the graph is connected (on non-isolated nodes) and all degrees are even.
        """
        degree: Dict[int, int] = defaultdict(int)
        for u in self.adj:
            degree[u] = len(self.adj[u])

        # Find a node with degree > 0 to start DFS
        start: Optional[int] = None
        for u in range(1, self.n + 1):
            if degree[u] > 0:
                start = u
                break

        if start is None:
            # No edges in the graph, treat as Eulerian (trivial circuit)
            return True

        # Check all degrees are even
        for u in range(1, self.n + 1):
            if degree[u] % 2 != 0:
                return False

        # Check connectivity (only among nodes with degree > 0)
        visited: set = set()
        stack: List[int] = [start]
        while stack:
            u = stack.pop()
            if u in visited:
                continue
            visited.add(u)
            for v, _ in self.adj[u]:
                if v not in visited:
                    stack.append(v)

        for u in range(1, self.n + 1):
            if degree[u] > 0 and u not in visited:
                return False

        return True

    def find_eulerian_circuit(self) -> List[int]:
        """
        Constructs an Eulerian circuit using Hierholzer's algorithm.

        Returns:
            List of node ids representing the Eulerian circuit (start and end node are the same).
            Returns empty list if no circuit exists.
        """
        # Find a node with degree > 0 to start
        start: Optional[int] = None
        for u in range(1, self.n + 1):
            if len(self.adj[u]) > 0:
                start = u
                break

        if start is None:
            # No edges, return empty circuit
            return []

        # Copy adjacency list for local modification
        local_adj: Dict[int, List[Tuple[int, int]]] = {u: list(self.adj[u]) for u in self.adj}
        used: Dict[int, bool] = {eid: False for eid in self.edge_used}

        circuit: List[int] = []
        stack: List[int] = [start]


        # For multi-edges, we need to track which edge is used
        # Use a local pointer for each node to avoid O(N^2) removals
        adj_idx: Dict[int, int] = {u: 0 for u in local_adj}

        while stack:
            u = stack[-1]
            while adj_idx.get(u, 0) < len(local_adj.get(u, [])):
                v, eid = local_adj[u][adj_idx[u]]
                adj_idx[u] += 1
                if not used[eid]:
                    used[eid] = True
                    stack.append(v)
                    u = v
                    break
            else:
                # No more unused edges from u
                circuit.append(u)
                stack.pop()

        circuit.reverse()
        return circuit if len(circuit) > 1 else []

class PelicanTownNPCSolver:
    """Solver for the Pelican Town NPC Eulerian circuit problem."""

    def __init__(self, test_cases: List[TestCase]) -> None:
        """
        Args:
            test_cases: List of TestCase objects.
        """
        self.test_cases: List[TestCase] = test_cases

    def solve(self) -> List[Tuple[bool, List[int]]]:
        """
        Solves all test cases.

        Returns:
            List of tuples: (True, route) if Eulerian circuit exists, (False, []) otherwise.
        """
        results: List[Tuple[bool, List[int]]] = []
        for case in self.test_cases:
            graph = NPCRoadGraph(case.n)
            edge_id = 0
            for u, v, c in case.edges:
                if c == 1:
                    graph.add_edge(u, v, edge_id)
                    edge_id += 1
            if graph.is_eulerian():
                route = graph.find_eulerian_circuit()
                # If the circuit is empty but there are edges, it's invalid
                if len(route) > 1 or edge_id == 0:
                    results.append((True, route))
                else:
                    results.append((False, []))
            else:
                results.append((False, []))
        return results

class Main:
    """Main class for input/output and program entry."""

    @staticmethod
    def main() -> None:
        """
        Reads input, processes test cases, and outputs results.
        """
        input_lines = sys.stdin.read().splitlines()
        idx = 0
        t = int(input_lines[idx].strip())
        idx += 1
        test_cases: List[TestCase] = []
        for _ in range(t):
            n, m = map(int, input_lines[idx].strip().split())
            idx += 1
            edges: List[Tuple[int, int, int]] = []
            for _ in range(m):
                u, v, c = map(int, input_lines[idx].strip().split())
                edges.append((u, v, c))
                idx += 1
            test_cases.append(TestCase(n, m, edges))

        solver = PelicanTownNPCSolver(test_cases)
        results = solver.solve()
        for has_circuit, route in results:
            if has_circuit:
                print("YES")
                print(len(route))
                print(' '.join(map(str, route)))
            else:
                print("NO")

if __name__ == "__main__":
    Main.main()
