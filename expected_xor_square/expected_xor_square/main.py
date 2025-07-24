## main.py

from typing import List, Tuple
import sys
import math


class XORSquareSolver:
    """Solver for expected value of (f(S))^2 where f(S) is XOR of a random multiset S."""

    MOD: int = 10 ** 9 + 7
    INV_10000: int = pow(10000, MOD - 2, MOD)  # Modular inverse of 10000 mod MOD

    def solve(self, test_cases: List[Tuple[int, List[int], List[int]]]) -> List[Tuple[int, int]]:
        """
        Solve all test cases.

        Args:
            test_cases: List of tuples (n, a, p) where
                n: number of elements
                a: list of integers
                p: list of probabilities (in basis points, i.e., 0..10000)

        Returns:
            List of tuples (numerator, denominator) representing the expected value
            as an irreducible fraction modulo MOD.
        """
        results = []
        for n, a, p in test_cases:
            num, den = self._expected_xor_square(n, a, p)
            results.append((num, den))
        return results

    def _expected_xor_square(self, n: int, a: List[int], p: List[int]) -> Tuple[int, int]:
        """
        Compute expected value of (f(S))^2 for one test case.

        Args:
            n: number of elements
            a: list of integers
            p: list of probabilities (in basis points, i.e., 0..10000)

        Returns:
            (numerator, denominator) of the expected value as an irreducible fraction modulo MOD.
        """
        # For each bit position, compute the probability that the bit is set in f(S)
        # Let q_i = p_i / 10000
        # For each bit, the probability that the bit is set in f(S) is:
        #   prod_{i: bit set in a_i} (1 - 2*q_i)
        # The expected value is sum over all bits:
        #   E[(f(S))^2] = sum_{i,j} E[bit_i * bit_j] = sum_{i} 2^{2i} * Pr[bit_i and bit_j set]
        # But since XOR, only diagonal terms survive, so E[(f(S))^2] = sum_{b} 2^{2b} * Pr[bit b is set in f(S)]

        max_bit = 0
        for val in a:
            if val > 0:
                max_bit = max(max_bit, val.bit_length())
        max_bit = max(max_bit, 1)  # At least 1 bit

        # Precompute q_i = p_i / 10000 mod MOD
        q = [(pi * self.INV_10000) % self.MOD for pi in p]

        expected = 0
        for bit in range(max_bit):
            # For this bit, find indices where a[i] has this bit set
            indices = [i for i in range(n) if (a[i] >> bit) & 1]
            if not indices:
                continue
            # Compute product_{i in indices} (1 - 2*q_i) mod MOD
            prod = 1
            for i in indices:
                term = (1 - 2 * q[i]) % self.MOD
                prod = (prod * term) % self.MOD
            # Probability that bit is set in f(S) is (1 - prod) / 2 mod MOD
            prob = ((1 - prod) * self._modinv(2)) % self.MOD
            # Contribution to expected value: (2^bit)^2 * prob
            contrib = (pow(2, 2 * bit, self.MOD) * prob) % self.MOD
            expected = (expected + contrib) % self.MOD

        # The expected value is expected/1, but we must output as irreducible fraction
        # Since all probabilities are rational, the denominator is a power of 2 and/or 10000
        # But since we use modular inverse, the result is already modulo MOD
        # Output as (expected, 1)
        return (expected, 1)

    def _modinv(self, x: int) -> int:
        """
        Compute modular inverse of x modulo MOD.

        Args:
            x: integer

        Returns:
            Modular inverse of x modulo MOD.
        """
        return pow(x, self.MOD - 2, self.MOD)


class InputParser:
    """Handles input parsing for the problem."""

    @staticmethod
    def parse_input() -> List[Tuple[int, List[int], List[int]]]:
        """
        Parse all input from stdin.

        Returns:
            List of test cases, each as (n, a, p)
        """
        input_lines = sys.stdin.read().splitlines()
        idx = 0
        t = int(input_lines[idx].strip())
        idx += 1
        test_cases = []
        for _ in range(t):
            n = int(input_lines[idx].strip())
            idx += 1
            a = list(map(int, input_lines[idx].strip().split()))
            idx += 1
            p = list(map(int, input_lines[idx].strip().split()))
            idx += 1
            test_cases.append((n, a, p))
        return test_cases


class OutputFormatter:
    """Handles formatting and printing of results."""

    @staticmethod
    def format_output(results: List[Tuple[int, int]]) -> None:
        """
        Print results in required modular irreducible fraction format.

        Args:
            results: List of (numerator, denominator) tuples
        """
        for num, den in results:
            # Output as "num/den" modulo MOD, with irreducible fraction
            # If den != 1, reduce fraction modulo MOD
            if den == 1:
                print(num % XORSquareSolver.MOD)
            else:
                # Reduce fraction
                g = math.gcd(num, den)
                num //= g
                den //= g
                # Output num * modinv(den) % MOD
                modinv_den = pow(den, XORSquareSolver.MOD - 2, XORSquareSolver.MOD)
                print((num * modinv_den) % XORSquareSolver.MOD)


class Main:
    """Main program entry point."""

    @staticmethod
    def main() -> None:
        """
        Main function to orchestrate input, computation, and output.
        """
        parser = InputParser()
        solver = XORSquareSolver()
        formatter = OutputFormatter()

        test_cases = parser.parse_input()
        results = solver.solve(test_cases)
        formatter.format_output(results)


if __name__ == "__main__":
    Main.main()
