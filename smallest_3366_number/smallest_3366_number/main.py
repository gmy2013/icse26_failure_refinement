## main.py
from collections import deque
from typing import List, Tuple, Dict


class Smallest3366NumberSolver:
    """Solver for finding the smallest n-digit number using only 3 and 6, divisible by 66."""

    def solve(self, test_cases: List[int]) -> List[str]:
        """Solves the problem for multiple test cases.

        Args:
            test_cases: List of integers, each representing the required number length n.

        Returns:
            List of strings, each the smallest valid number for the corresponding n,
            or '-1' if no such number exists.
        """
        results: List[str] = []
        for n in test_cases:
            result = self._bfs(n)
            results.append(result)
        return results

    def _bfs(self, n: int) -> str:
        """Performs BFS to find the smallest n-digit number using only 3 and 6, divisible by 66.

        Args:
            n: The required number length.

        Returns:
            The smallest such number as a string, or '-1' if impossible.
        """
        if n <= 0:
            return '-1'

        # State: (length, sum_mod3, alt_sum_mod11, last_digit)
        # We only need to keep the smallest number for each unique state.
        queue: deque = deque()
        visited: Dict[Tuple[int, int, int, int], str] = {}

        # Initial states: first digit cannot be '0', so only '3' or '6'
        for first_digit in ('3', '6'):
            digit = int(first_digit)
            length = 1
            sum_mod3 = digit % 3
            alt_sum_mod11 = digit % 11  # First digit is at position 1 (odd)
            last_digit = digit
            number_str = first_digit
            state = (length, sum_mod3, alt_sum_mod11, last_digit)
            queue.append((state, number_str))
            visited[state] = number_str

        while queue:
            (length, sum_mod3, alt_sum_mod11, last_digit), number_str = queue.popleft()

            if length == n:
                # Check divisibility constraints
                if (last_digit == 6 and
                        sum_mod3 == 0 and
                        alt_sum_mod11 == 0):
                    return number_str
                continue

            # Next digit can be '3' or '6'
            for next_digit_char in ('3', '6'):
                next_digit = int(next_digit_char)
                next_length = length + 1
                next_sum_mod3 = (sum_mod3 + next_digit) % 3

                # Alternating sum: odd positions +, even positions -
                # If next position is odd: add, if even: subtract
                if next_length % 2 == 1:
                    next_alt_sum_mod11 = (alt_sum_mod11 + next_digit) % 11
                else:
                    next_alt_sum_mod11 = (alt_sum_mod11 - next_digit) % 11

                next_last_digit = next_digit
                next_number_str = number_str + next_digit_char
                next_state = (next_length, next_sum_mod3, next_alt_sum_mod11, next_last_digit)

                # Only keep the lex smallest number for each state
                if next_state not in visited or next_number_str < visited[next_state]:
                    visited[next_state] = next_number_str
                    queue.append((next_state, next_number_str))

        return '-1'


class Main:
    """Main class to handle input/output and invoke the solver."""

    @staticmethod
    def main() -> None:
        """Reads input, processes test cases, and prints results."""
        import sys

        # Read input
        lines = [line.strip() for line in sys.stdin if line.strip()]
        if not lines:
            return

        t = int(lines[0])
        test_cases: List[int] = []
        for i in range(1, t + 1):
            test_cases.append(int(lines[i]))

        solver = Smallest3366NumberSolver()
        results = solver.solve(test_cases)
        for res in results:
            print(res)


if __name__ == "__main__":
    Main.main()
