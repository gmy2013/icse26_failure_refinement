## main.py

from typing import List
import sys
from procedure_counter import ProcedureCounter

class Main:
    """Main class to handle input parsing, procedure counting, and output."""

    def run(self) -> None:
        """Reads input, processes each test case, and outputs results."""
        input_lines = sys.stdin.read().splitlines()
        idx: int = 0
        t: int = int(input_lines[idx].strip())
        idx += 1
        results: List[int] = []

        for _ in range(t):
            if idx >= len(input_lines):
                break
            n: int = int(input_lines[idx].strip())
            idx += 1
            if idx >= len(input_lines):
                break
            a_str: List[str] = input_lines[idx].strip().split()
            a: List[int] = [int(x) for x in a_str]
            idx += 1
            result: int = ProcedureCounter.count_max_procedures(a)
            results.append(result)

        for res in results:
            print(res)

if __name__ == "__main__":
    Main().run()
