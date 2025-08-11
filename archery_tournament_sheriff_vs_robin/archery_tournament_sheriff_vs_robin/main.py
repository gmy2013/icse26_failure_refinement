## main.py

import sys
from typing import List, Tuple
import numpy as np

from archery_game import ArcheryGame, QueryProcessor


class MainApp:
    """Main application class for the Archery Game CLI."""

    def run(self) -> None:
        """Runs the main application loop.

        Reads input from stdin, processes test cases and queries,
        and prints results to stdout.
        """
        input_lines: List[str] = sys.stdin.read().splitlines()
        line_idx: int = 0

        # Read number of test cases
        if line_idx >= len(input_lines):
            print("No input provided.")
            return
        try:
            t: int = int(input_lines[line_idx].strip())
        except ValueError:
            print("Invalid number of test cases.")
            return
        line_idx += 1

        for test_case in range(t):
            # Read number of targets and number of queries
            if line_idx >= len(input_lines):
                print("Insufficient input for test case.")
                return
            try:
                n_q: List[int] = list(map(int, input_lines[line_idx].strip().split()))
                n: int = n_q[0]
                q: int = n_q[1]
            except (IndexError, ValueError):
                print("Invalid input for n and q.")
                return
            line_idx += 1

            # Read targets
            if line_idx >= len(input_lines):
                print("Insufficient input for targets.")
                return
            try:
                targets: List[int] = list(map(int, input_lines[line_idx].strip().split()))
                if len(targets) != n:
                    print(f"Expected {n} targets, got {len(targets)}.")
                    return
            except ValueError:
                print("Invalid input for targets.")
                return
            line_idx += 1

            # Read queries
            queries: List[Tuple[int, int]] = []
            for _ in range(q):
                if line_idx >= len(input_lines):
                    print("Insufficient input for queries.")
                    return
                try:
                    l_r: List[int] = list(map(int, input_lines[line_idx].strip().split()))
                    if len(l_r) != 2:
                        print("Each query must have two integers.")
                        return
                    l: int = l_r[0]
                    r: int = l_r[1]
                    queries.append((l, r))
                except ValueError:
                    print("Invalid input for query.")
                    return
                line_idx += 1

            # Initialize game and processor
            game: ArcheryGame = ArcheryGame(targets)
            processor: QueryProcessor = QueryProcessor(game)
            results: List[bool] = processor.process_queries(queries)

            # Output results
            for res in results:
                print("YES" if res else "NO")



if __name__ == "__main__":
    app: MainApp = MainApp()
    app.run()
