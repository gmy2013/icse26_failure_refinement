## main.py

"""Main module for counting balanced binary substrings in all subranges.

This script reads a binary string from standard input, uses the
GachaBinarySubstringCounter class to count the total number of balanced
substrings in all subranges, and prints the result.

Dependencies:
    - numpy>=1.18.0
"""

import sys
from gacha_counter import GachaBinarySubstringCounter


def main() -> None:
    """Main function to handle input/output and invoke the counter logic.

    Reads a binary string from standard input, computes the total number of
    balanced substrings in all subranges, and prints the result.
    """
    # Read input string (strip to remove any trailing newline/whitespace)
    s: str = sys.stdin.readline().strip()

    # Validate input: ensure only '0' and '1' are present
    if not all(ch in {'0', '1'} for ch in s):
        print("Error: Input string must contain only '0' and '1'.", file=sys.stderr)
        return

    # Compute the answer using the GachaBinarySubstringCounter
    answer: int = GachaBinarySubstringCounter.count_balanced_substrings_all_ranges(s)

    # Output the result
    print(answer)


if __name__ == "__main__":
    main()
