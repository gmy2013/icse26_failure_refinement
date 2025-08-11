## main.py

import sys
from typing import List, Tuple

from conquest_counter import ConquestCounter

class Main:
    """
    Main class to handle input parsing, invoking the core logic, and output formatting.
    """

    @staticmethod
    def main() -> None:
        """
        Main entry point for the program.
        Reads input, processes each test case, and prints the results.
        """
        input_lines = sys.stdin.read().splitlines()
        input_iter = iter(input_lines)
        t: int = int(next(input_iter))
        test_cases: List[Tuple[int, int]] = []
        for _ in range(t):
            n_str, p_str = next(input_iter).strip().split()
            n, p = int(n_str), int(p_str)
            test_cases.append((n, p))

        results: List[List[int]] = []
        for n, p in test_cases:
            counter = ConquestCounter(n, p)
            ans = counter.count_valid_arrays()
            results.append(ans)

        for ans in results:
            print(' '.join(str(x) for x in ans))

if __name__ == "__main__":
    Main.main()
