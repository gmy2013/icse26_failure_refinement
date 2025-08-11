## main.py
from typing import List, Tuple


class DigitSumMultiplierCounter:
    """Class to count integers n in [10^l, 10^r) such that D(k*n) = k*D(n),
    where D(x) is the sum of digits of x.
    """

    def __init__(self) -> None:
        """Initializes the DigitSumMultiplierCounter."""
        pass

    def count_valid_n(self, l: int, r: int, k: int) -> int:
        """Counts the number of valid n in [10^l, 10^r) such that D(k*n) = k*D(n).

        Args:
            l (int): The lower exponent (inclusive), i.e., n >= 10^l.
            r (int): The upper exponent (exclusive), i.e., n < 10^r.
            k (int): The multiplier.

        Returns:
            int: The count of valid n.
        """
        repunits = self._generate_repunits(l, r)
        count = 0
        for n in repunits:
            if self._is_valid(n, k):
                count += 1
        return count

    def _is_valid(self, n: int, k: int) -> bool:
        """Checks if D(k*n) == k*D(n).

        Args:
            n (int): The integer to check.
            k (int): The multiplier.

        Returns:
            bool: True if D(k*n) == k*D(n), False otherwise.
        """
        digit_sum_n = self._digit_sum(n)
        k_digit_sum_n = k * digit_sum_n
        k_n = k * n
        digit_sum_k_n = self._digit_sum(k_n)
        return digit_sum_k_n == k_digit_sum_n

    def _generate_repunits(self, l: int, r: int) -> List[int]:
        """Generates all repunit numbers in [10^l, 10^r).

        Args:
            l (int): The lower exponent (inclusive).
            r (int): The upper exponent (exclusive).

        Returns:
            List[int]: List of repunit numbers in the range.
        """
        repunits = []
        for length in range(l, r):
            base = 10 ** length
            for digit in range(1, 10):
                # Repunit: digit repeated 'length' times
                n = int(str(digit) * length)
                if base <= n < 10 ** (length + 1):
                    repunits.append(n)
        return repunits

    def _digit_sum(self, n: int) -> int:
        """Calculates the sum of digits of n.

        Args:
            n (int): The integer.

        Returns:
            int: The sum of digits.
        """
        return sum(int(d) for d in str(n))


class Main:
    """Main class for input parsing and program flow."""

    def __init__(self) -> None:
        """Initializes the Main class."""
        self.counter = DigitSumMultiplierCounter()

    def parse_input(self) -> Tuple[int, List[Tuple[int, int, int]]]:
        """Parses input from standard input.

        Returns:
            Tuple[int, List[Tuple[int, int, int]]]: Number of test cases and list of (l, r, k) tuples.
        """
        import sys

        input_lines = sys.stdin.read().splitlines()
        t = int(input_lines[0])
        test_cases = []
        for i in range(1, t + 1):
            l_str, r_str, k_str = input_lines[i].strip().split()
            l = int(l_str)
            r = int(r_str)
            k = int(k_str)
            test_cases.append((l, r, k))
        return t, test_cases

    def run(self) -> None:
        """Runs the main program logic."""
        t, test_cases = self.parse_input()
        results = []
        for l, r, k in test_cases:
            count = self.counter.count_valid_n(l, r, k)
            results.append(str(count))
        print('\n'.join(results))


if __name__ == "__main__":
    main = Main()
    main.run()
