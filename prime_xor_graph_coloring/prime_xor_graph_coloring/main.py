## main.py

from typing import List


class PrimeSieve:
    """Sieve of Eratosthenes for prime number queries up to max_n."""

    def __init__(self, max_n: int) -> None:
        """Initializes the sieve up to max_n (inclusive).

        Args:
            max_n: The maximum number up to which to compute primes.
        """
        self.max_n: int = max_n
        self.is_prime: List[bool] = [False, False] + [True] * (self.max_n - 1)
        for i in range(2, int(self.max_n ** 0.5) + 1):
            if self.is_prime[i]:
                for j in range(i * i, self.max_n + 1, i):
                    self.is_prime[j] = False

    def get_primes(self) -> List[int]:
        """Returns a list of all primes up to max_n.

        Returns:
            List of prime numbers up to max_n.
        """
        return [i for i, val in enumerate(self.is_prime) if val]

    def is_prime_number(self, x: int) -> bool:
        """Checks if x is a prime number.

        Args:
            x: The number to check.

        Returns:
            True if x is prime, False otherwise.
        """
        if 0 <= x <= self.max_n:
            return self.is_prime[x]
        return False


class GraphColoringSolver:
    """Solver for the XOR-prime graph coloring problem."""

    def __init__(self, max_n: int) -> None:
        """Initializes the solver with a prime sieve up to 2*max_n.

        Args:
            max_n: The maximum n for which the solver will be used.
        """
        # The maximum possible XOR value is up to 2*max_n for n up to max_n.
        self.sieve: PrimeSieve = PrimeSieve(2 * max_n)

    def min_colors(self, n: int) -> int:
        """Determines the minimum number of colors needed for the XOR-prime graph.

        Args:
            n: The number of vertices in the graph.

        Returns:
            The chromatic number (minimum number of colors needed).
        """
        if n == 1:
            return 1
        if n == 2:
            # Only one edge: 1 XOR 2 = 3 (prime), so need 2 colors.
            return 2
        # For n >= 3, the graph is always bipartite (2-colorable).
        return 2

    def coloring(self, n: int) -> List[int]:
        """Returns a valid coloring for the XOR-prime graph with n vertices.

        Args:
            n: The number of vertices in the graph.

        Returns:
            A list of colors (1-based) for each vertex from 1 to n.
        """
        if n == 1:
            return [1]
        if n == 2:
            return [1, 2]
        # For n >= 3, alternate colors: 1, 2, 1, 2, ...
        return [1 + (i % 2) for i in range(n)]


class Main:
    """Main class to handle input/output and orchestrate the solution."""

    def run(self) -> None:
        """Reads input, processes test cases, and prints the results."""
        import sys

        input_lines = sys.stdin.read().splitlines()
        t = int(input_lines[0])
        ptr = 1
        n_list: List[int] = []
        max_n: int = 0

        for _ in range(t):
            n = int(input_lines[ptr])
            n_list.append(n)
            max_n = max(max_n, n)
            ptr += 1

        solver = GraphColoringSolver(max_n)

        for n in n_list:
            k = solver.min_colors(n)
            coloring = solver.coloring(n)
            print(k)
            print(' '.join(map(str, coloring)))


if __name__ == "__main__":
    Main().run()
