## main.py

import sys
from typing import List

from olympiad_dp import OlympiadDP


def main() -> None:
    """
    Main function to parse input, process each test case, and print results.

    Reads from standard input. For each test case, reads n, a, b,
    computes the maximum score using OlympiadDP, and prints the result.
    """
    input_lines = sys.stdin.read().splitlines()
    line_idx: int = 0

    t: int = int(input_lines[line_idx])
    line_idx += 1

    results: List[int] = []

    for _ in range(t):
        n: int = int(input_lines[line_idx])
        line_idx += 1

        a: List[int] = list(map(int, input_lines[line_idx].split()))
        line_idx += 1

        b: List[int] = list(map(int, input_lines[line_idx].split()))
        line_idx += 1

        olympiad_dp = OlympiadDP(a, b)
        max_score: int = olympiad_dp.compute_max_score()
        results.append(max_score)

    for res in results:
        print(res)


if __name__ == "__main__":
    main()
