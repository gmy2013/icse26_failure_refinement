## main.py

from typing import List, Dict
import sys

class AncientLanguageCaseCounter:
    """Class to compute the minimum number of cases (distinct possible word endings)
    required to segment the text according to the given constraints."""

    def process_test_cases(self, test_cases: List[Dict]) -> List[int]:
        """Process all test cases and return the minimum number of cases for each.

        Args:
            test_cases: List of dictionaries, each containing 'n', 'c', 'k', and 'text'.

        Returns:
            List of integers, each representing the minimum number of cases for a test case.
        """
        results = []
        for case in test_cases:
            n = case['n']
            c = case['c']
            k = case['k']
            text = case['text']
            result = self._min_cases(n, c, k, text)
            results.append(result)
        return results

    def _min_cases(self, n: int, c: int, k: int, text: str) -> int:
        """Compute the minimum number of cases for a single test case.

        Args:
            n: Length of the text.
            c: Size of the alphabet (number of possible last letters).
            k: Maximum word length.
            text: The text string.

        Returns:
            The minimum number of cases (distinct possible word endings).
        """
        # Use bitsets for fast set operations if c <= 18 (fits in 18 bits)
        use_bitset = c <= 18

        # Map each character to an integer in [0, c-1]
        # Assume the alphabet is the set of unique letters in the text, sorted
        unique_letters = sorted(set(text))
        letter_to_idx = {ch: idx for idx, ch in enumerate(unique_letters)}
        text_idx = [letter_to_idx[ch] for ch in text]

        # DP: dp[i] = set of possible last letters for segmenting text[:i]
        # dp[0] = set() (empty prefix)
        if use_bitset:
            # Each dp[i] is an integer bitmask of length c
            dp = [0] * (n + 1)
            dp[0] = 0  # No last letter for empty prefix

            for i in range(1, n + 1):
                mask = 0
                for l in range(1, min(k, i) + 1):
                    prev = i - l
                    if prev == 0 or dp[prev] != 0:
                        # The last letter of this word is text_idx[i-1]
                        mask |= 1 << text_idx[i - 1]
                dp[i] = mask

            # The answer is the number of bits set in dp[n]
            return bin(dp[n]).count('1')
        else:
            # Each dp[i] is a set of last letters (integers)
            dp = [set() for _ in range(n + 1)]
            dp[0] = set()

            for i in range(1, n + 1):
                last_letters = set()
                for l in range(1, min(k, i) + 1):
                    prev = i - l
                    if prev == 0 or dp[prev]:
                        last_letters.add(text_idx[i - 1])
                dp[i] = last_letters

            return len(dp[n])


class InputParser:
    """Class to parse input from stdin."""

    def parse_input(self) -> List[Dict]:
        """Parse input from stdin.

        Returns:
            List of dictionaries, each containing 'n', 'c', 'k', and 'text'.
        """
        test_cases = []
        lines = []
        for line in sys.stdin:
            line = line.strip()
            if line:
                lines.append(line)
        idx = 0
        while idx < len(lines):
            # Each test case: n c k
            nck = lines[idx].split()
            if len(nck) != 3:
                idx += 1
                continue  # Skip invalid lines
            n, c, k = map(int, nck)
            idx += 1
            if idx >= len(lines):
                break
            text = lines[idx]
            idx += 1
            test_cases.append({
                'n': n,
                'c': c,
                'k': k,
                'text': text
            })
        return test_cases


class OutputFormatter:
    """Class to format and print output."""

    def format_output(self, results: List[int]) -> None:
        """Print the results, one per line.

        Args:
            results: List of integers to print.
        """
        for res in results:
            print(res)


def main() -> None:
    """Main function to coordinate input parsing, processing, and output formatting."""
    parser = InputParser()
    test_cases = parser.parse_input()
    counter = AncientLanguageCaseCounter()
    results = counter.process_test_cases(test_cases)
    formatter = OutputFormatter()
    formatter.format_output(results)


if __name__ == "__main__":
    main()
