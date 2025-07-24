## main.py

import sys
from typing import List, Tuple


class BitwiseEquationSolver:
    """Solves the equation (a | b) - (a & c) = d for given b, c, d."""

    def solve_case(self, b: int, c: int, d: int) -> int:
        """Finds an integer a such that (a | b) - (a & c) == d.
        Returns the first such a found, or -1 if impossible.

        Args:
            b (int): The integer b in the equation.
            c (int): The integer c in the equation.
            d (int): The target difference.

        Returns:
            int: The integer a if a solution exists, else -1.
        """
        a = 0
        for i in range(0, 61):  # Since b, c, d <= 1e18, 60 bits suffice
            b_i = (b >> i) & 1
            c_i = (c >> i) & 1
            d_i = (d >> i) & 1

            # For each bit, try to find a_i (0 or 1) such that:
            # (a_i | b_i) - (a_i & c_i) == d_i
            # There are only two possibilities for a_i: 0 or 1
            found = False
            for a_i in (0, 1):
                or_val = a_i | b_i
                and_val = a_i & c_i
                if (or_val - and_val) == d_i:
                    if a_i:
                        a |= (1 << i)
                    found = True
                    break  # Take the first valid a_i (prefer 0 if possible)
            if not found:
                return -1
        return a

    def solve_all(self, cases: List[Tuple[int, int, int]]) -> List[int]:
        """Solves all test cases.

        Args:
            cases (List[Tuple[int, int, int]]): List of (b, c, d) tuples.

        Returns:
            List[int]: List of results for each test case.
        """
        results = []
        for b, c, d in cases:
            result = self.solve_case(b, c, d)
            results.append(result)
        return results


class Main:
    """Handles input/output and orchestrates the solving process."""

    @staticmethod
    def main() -> None:
        """Reads input, processes test cases, and prints results."""
        input_lines = sys.stdin.read().splitlines()
        if not input_lines:
            return
        t = int(input_lines[0])
        cases: List[Tuple[int, int, int]] = []
        for i in range(1, t + 1):
            b_str, c_str, d_str = input_lines[i].strip().split()
            b = int(b_str)
            c = int(c_str)
            d = int(d_str)
            cases.append((b, c, d))
        solver = BitwiseEquationSolver()
        results = solver.solve_all(cases)
        output = '\n'.join(str(res) for res in results)
        sys.stdout.write(output + '\n')


if __name__ == "__main__":
    Main.main()
