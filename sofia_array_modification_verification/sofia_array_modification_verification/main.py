## main.py

import sys
from collections import Counter
from typing import List, Dict


class SofiaArrayVerifier:
    """Class to verify if the found array can be obtained from the original array
    using the given modification values."""

    def verify_test_case(
        self,
        n: int,
        a: List[int],
        b: List[int],
        m: int,
        d: List[int]
    ) -> bool:
        """Verify a single test case.

        Args:
            n: Length of the original and found arrays.
            a: The original array.
            b: The found array.
            m: Number of modification values.
            d: The list of modification values.

        Returns:
            True if the found array can be obtained, False otherwise.
        """
        # Calculate the required modifications for each index
        required_modifications = []
        for i in range(n):
            diff = b[i] - a[i]
            if diff < 0:
                # Cannot decrease values, only increase
                return False
            if diff > 0:
                required_modifications.append(diff)

        # Count the required modifications
        required_counter = Counter(required_modifications)
        # Count the available modification values
        available_counter = Counter(d)

        # For each required modification, check if enough modifications are available
        for mod_value, count in required_counter.items():
            if available_counter[mod_value] < count:
                return False

        return True

    def batch_verify(self, test_cases: List[Dict]) -> List[str]:
        """Verify a batch of test cases.

        Args:
            test_cases: List of test case dictionaries.

        Returns:
            List of 'YES' or 'NO' for each test case.
        """
        results = []
        for case in test_cases:
            n = case['n']
            a = case['a']
            b = case['b']
            m = case['m']
            d = case['d']
            if self.verify_test_case(n, a, b, m, d):
                results.append('YES')
            else:
                results.append('NO')
        return results


class CLI:
    """Command-line interface for the SofiaArrayVerifier."""

    @staticmethod
    def read_input() -> List[Dict]:
        """Reads input from stdin and parses test cases.

        Returns:
            List of test case dictionaries.
        """
        input_lines = sys.stdin.read().splitlines()
        test_cases = []
        idx = 0
        t = int(input_lines[idx])
        idx += 1
        for _ in range(t):
            n = int(input_lines[idx])
            idx += 1
            a = list(map(int, input_lines[idx].split()))
            idx += 1
            b = list(map(int, input_lines[idx].split()))
            idx += 1
            m = int(input_lines[idx])
            idx += 1
            d = list(map(int, input_lines[idx].split()))
            idx += 1
            test_cases.append({
                'n': n,
                'a': a,
                'b': b,
                'm': m,
                'd': d
            })
        return test_cases

    @staticmethod
    def print_output(results: List[str]) -> None:
        """Prints the results to stdout.

        Args:
            results: List of 'YES' or 'NO' strings.
        """
        sys.stdout.write('\n'.join(results) + '\n')

    @staticmethod
    def main() -> None:
        """Main entry point for the CLI."""
        test_cases = CLI.read_input()
        verifier = SofiaArrayVerifier()
        results = verifier.batch_verify(test_cases)
        CLI.print_output(results)


if __name__ == '__main__':
    CLI.main()
