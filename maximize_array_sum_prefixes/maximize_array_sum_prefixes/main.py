## main.py

from typing import List
from maximizer import ArraySumMaximizer


def main() -> None:
    """Main entry point for the prefix sum maximization program.

    Reads input, processes the array using ArraySumMaximizer, and prints results.
    """
    import sys

    # Read input from stdin
    input_lines: List[str] = sys.stdin.read().splitlines()
    if not input_lines:
        return

    # First line: number of test cases or array size
    line_idx: int = 0
    if input_lines[0].isdigit():
        n: int = int(input_lines[0])
        line_idx += 1
    else:
        n: int = len(input_lines[0].split())

    # Next line: array elements
    if line_idx < len(input_lines):
        a_str: List[str] = input_lines[line_idx].strip().split()
        a: List[int] = [int(x) for x in a_str]
    else:
        a: List[int] = []

    # If n is given, ensure we only take n elements
    if len(a) > n:
        a = a[:n]

    # Instantiate the maximizer and compute results
    maximizer: ArraySumMaximizer = ArraySumMaximizer()
    result: List[int] = maximizer.maximize_prefix_sums(a)

    # Print results, one per line
    for prefix_sum in result:
        print(prefix_sum)


if __name__ == "__main__":
    main()
