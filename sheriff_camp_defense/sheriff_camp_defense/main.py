## main.py

from typing import List, Tuple
import sys
import threading


class CampDefenseSolver:
    """Solver for the 'maximum gold in surviving camps' problem using tree DP."""

    def __init__(self) -> None:
        """Initializes the CampDefenseSolver."""
        pass

    def solve(self, test_cases: List[Tuple[int, int, List[int], List[Tuple[int, int]]]]) -> List[int]:
        """
        Solves multiple test cases.

        Args:
            test_cases: A list of tuples, each containing:
                - n: number of camps (nodes)
                - c: gold cost to strengthen a camp's neighbor
                - gold: list of gold in each camp
                - edges: list of (u, v) tuples representing edges

        Returns:
            List of maximum gold values for each test case.
        """
        results: List[int] = []
        for n, c, gold, edges in test_cases:
            result = self._tree_dp(n, c, gold, edges)
            results.append(result)
        return results

    def _tree_dp(self, n: int, c: int, gold: List[int], edges: List[Tuple[int, int]]) -> int:
        """
        Performs tree DP to compute the maximum gold.

        Args:
            n: Number of camps (nodes)
            c: Gold cost to strengthen a camp's neighbor
            gold: List of gold in each camp
            edges: List of (u, v) tuples representing edges

        Returns:
            Maximum gold that can be obtained.
        """
        sys.setrecursionlimit(max(100000, n + 10))

        # Build adjacency list
        adj: List[List[int]] = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        # dp[node][0]: max gold if node is NOT strengthened
        # dp[node][1]: max gold if node IS strengthened
        dp: List[List[int]] = [[0, 0] for _ in range(n)]

        def dfs(u: int, parent: int) -> None:
            # If u is not strengthened, its children may or may not be
            dp[u][0] = 0
            # If u is strengthened, its children cannot be
            dp[u][1] = gold[u]
            for v in adj[u]:
                if v == parent:
                    continue
                dfs(v, u)
                # If u is not strengthened, take the best of strengthening or not strengthening v
                dp[u][0] += max(dp[v][0], dp[v][1])
                # If u is strengthened, v cannot be strengthened, and v loses c gold
                dp[u][1] += dp[v][0] - c

        dfs(0, -1)
        return max(dp[0][0], dp[0][1])

class Main:
    """Main class to handle input/output and orchestrate the solution."""

    @staticmethod
    def main() -> None:
        """
        Reads input, processes test cases, and prints results.
        """
        def read_input() -> List[Tuple[int, int, List[int], List[Tuple[int, int]]]]:
            input_lines = sys.stdin.read().splitlines()
            t = int(input_lines[0])
            idx = 1
            test_cases: List[Tuple[int, int, List[int], List[Tuple[int, int]]]] = []
            for _ in range(t):
                n_c = input_lines[idx].split()
                n = int(n_c[0])
                c = int(n_c[1])
                idx += 1
                gold = list(map(int, input_lines[idx].split()))
                idx += 1
                edges: List[Tuple[int, int]] = []
                for _ in range(n - 1):
                    u_v = input_lines[idx].split()
                    u = int(u_v[0]) - 1  # Convert to 0-based index
                    v = int(u_v[1]) - 1
                    edges.append((u, v))
                    idx += 1
                test_cases.append((n, c, gold, edges))
            return test_cases

        test_cases = read_input()
        solver = CampDefenseSolver()
        results = solver.solve(test_cases)
        for res in results:
            print(res)

if __name__ == "__main__":
    threading.Thread(target=Main.main).start()
