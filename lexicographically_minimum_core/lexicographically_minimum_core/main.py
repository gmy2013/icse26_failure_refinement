## main.py

from typing import List, Tuple


class LexMinCoreSolver:
    """Solver for finding the lexicographically minimal core substring."""

    def __init__(self) -> None:
        """Initializes the LexMinCoreSolver."""
        pass

    def find_min_core(self, s: str) -> str:
        """Finds the minimal core substring for the given string.

        The minimal core is defined as the suffix of the sorted string
        starting from the first occurrence of the largest character.

        Args:
            s: The input string.

        Returns:
            The minimal core substring.
        """
        sorted_s: str = ''.join(sorted(s))
        max_char: str = sorted_s[-1]
        first_max_idx: int = sorted_s.find(max_char)
        return sorted_s[first_max_idx:]

    def process_batch(self, test_cases: List[Tuple[int, str]]) -> List[str]:
        """Processes a batch of test cases.

        Args:
            test_cases: A list of tuples, each containing the length of the string and the string itself.

        Returns:
            A list of minimal core substrings, one for each test case.
        """
        results: List[str] = []
        for _, s in test_cases:
            min_core: str = self.find_min_core(s)
            results.append(min_core)
        return results


class MainApp:
    """Main application class for running the LexMinCoreSolver."""

    def __init__(self) -> None:
        """Initializes the MainApp and its solver."""
        self.solver: LexMinCoreSolver = LexMinCoreSolver()

    def run(self) -> None:
        """Runs the application: reads input, processes test cases, and prints results."""
        import sys

        input_lines: List[str] = sys.stdin.read().splitlines()
        if not input_lines:
            return

        t: int = int(input_lines[0])
        test_cases: List[Tuple[int, str]] = []
        idx: int = 1
        for _ in range(t):
            if idx + 1 > len(input_lines):
                break
            n: int = int(input_lines[idx])
            s: str = input_lines[idx + 1]
            test_cases.append((n, s))
            idx += 2

        results: List[str] = self.solver.process_batch(test_cases)
        print('\n'.join(results))


if __name__ == "__main__":
    app: MainApp = MainApp()
    app.run()
