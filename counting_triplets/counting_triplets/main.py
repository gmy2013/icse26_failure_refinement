## main.py

from typing import List, Tuple
from triplet_counter import TripletCounter


class InputHandler:
    """Handles reading input from standard input."""

    def read_input(self) -> Tuple[List[Tuple[int, int]], int]:
        """Reads input for multiple test cases.

        Returns:
            A tuple containing:
                - A list of (n, x) tuples for each test case.
                - The number of test cases.
        """
        import sys

        lines: List[str] = []
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                if line.strip() == '':
                    continue
                lines.append(line.strip())
            except EOFError:
                break

        if not lines:
            return [], 0

        t: int = int(lines[0])
        test_cases: List[Tuple[int, int]] = []
        for i in range(1, t + 1):
            n_str, x_str = lines[i].split()
            n: int = int(n_str)
            x: int = int(x_str)
            test_cases.append((n, x))
        return test_cases, t


class OutputHandler:
    """Handles writing output to standard output."""

    def write_output(self, results: List[int]) -> None:
        """Writes the results for each test case to standard output.

        Args:
            results: A list of integers, each representing the answer for a test case.
        """
        for result in results:
            print(result)


class MainApp:
    """Main application class orchestrating the triplet counting process."""

    def __init__(self) -> None:
        self.triplet_counter: TripletCounter = TripletCounter()
        self.input_handler: InputHandler = InputHandler()
        self.output_handler: OutputHandler = OutputHandler()

    def run(self) -> None:
        """Runs the main application logic."""
        test_cases, t = self.input_handler.read_input()
        results: List[int] = []
        for n, x in test_cases:
            result: int = self.triplet_counter.count_triplets(n, x)
            results.append(result)
        self.output_handler.write_output(results)


if __name__ == "__main__":
    app: MainApp = MainApp()
    app.run()
