## main.py
from typing import List, Tuple


class PermutationSubsegmentMinSum:
    """Class to compute sum of minimums over all subsegments for a permutation,
    and efficiently update the sum after each removal."""

    def __init__(self) -> None:
        pass

    def process_test_case(self, n: int, a: List[int]) -> List[int]:
        """Process a single test case.

        Args:
            n: Length of the permutation.
            a: The permutation as a list of integers.

        Returns:
            List of integers, where the i-th element is f(b) after removing a[i].
        """
        # Precompute left and right boundaries for each element
        left, right, contrib = self.compute_contributions(a)
        total = sum(contrib)
        result = []
        for i in range(n):
            # When removing a[i], subtract its contribution from total
            result.append(total - contrib[i])
        return result

    def compute_f(self, a: List[int]) -> int:
        """Compute f(a): sum of minimums over all subsegments.

        Args:
            a: The permutation as a list of integers.

        Returns:
            The sum as an integer.
        """
        _, _, contrib = self.compute_contributions(a)
        return sum(contrib)

    def compute_contributions(
        self, a: List[int]
    ) -> Tuple[List[int], List[int], List[int]]:
        """Compute left/right boundaries and contribution for each element.

        For each a[i], find:
            - left[i]: index of previous element less than a[i] (exclusive), or -1
            - right[i]: index of next element less than a[i] (exclusive), or n
            - contrib[i]: a[i] * (i - left[i]) * (right[i] - i)

        Args:
            a: The permutation as a list of integers.

        Returns:
            Tuple of (left, right, contrib) lists.
        """
        n = len(a)
        left = [-1] * n
        right = [n] * n
        stack = []

        # Compute left boundaries
        for i in range(n):
            while stack and a[stack[-1]] > a[i]:
                stack.pop()
            left[i] = stack[-1] if stack else -1
            stack.append(i)

        # Compute right boundaries
        stack.clear()
        for i in range(n - 1, -1, -1):
            while stack and a[stack[-1]] >= a[i]:
                stack.pop()
            right[i] = stack[-1] if stack else n
            stack.append(i)

        # Compute contributions
        contrib = [0] * n
        for i in range(n):
            left_count = i - left[i]
            right_count = right[i] - i
            contrib[i] = a[i] * left_count * right_count

        return left, right, contrib

    def solve(
        self, t: int, test_cases: List[Tuple[int, List[int]]]
    ) -> List[List[int]]:
        """Solve all test cases.

        Args:
            t: Number of test cases.
            test_cases: List of (n, a) tuples.

        Returns:
            List of results, each a list of integers for a test case.
        """
        results = []
        for n, a in test_cases:
            results.append(self.process_test_case(n, a))
        return results


class InputParser:
    """Class to handle input reading and parsing."""

    def __init__(self) -> None:
        pass

    def read_input(self) -> Tuple[int, List[Tuple[int, List[int]]]]:
        """Read input from stdin.

        Returns:
            Tuple of (t, test_cases), where test_cases is a list of (n, a).
        """
        import sys

        input_lines = sys.stdin.read().splitlines()
        idx = 0
        t = int(input_lines[idx])
        idx += 1
        test_cases = []
        for _ in range(t):
            n = int(input_lines[idx])
            idx += 1
            a = list(map(int, input_lines[idx].split()))
            idx += 1
            test_cases.append((n, a))
        return t, test_cases


class OutputFormatter:
    """Class to handle output formatting and printing."""

    def __init__(self) -> None:
        pass

    def format_output(self, results: List[List[int]]) -> None:
        """Print results to stdout.

        Args:
            results: List of results, each a list of integers for a test case.
        """
        for res in results:
            print(" ".join(map(str, res)))


def main() -> None:
    """Main function to orchestrate input, processing, and output."""
    parser = InputParser()
    t, test_cases = parser.read_input()
    solver = PermutationSubsegmentMinSum()
    results = solver.solve(t, test_cases)
    formatter = OutputFormatter()
    formatter.format_output(results)


if __name__ == "__main__":
    main()
