## main.py

from typing import List, Tuple


class MochaArrayMedianMagic:
    """Class to process array median magic operations."""

    @staticmethod
    def process_test_cases(
        test_cases: List[Tuple[int, List[int]]]
    ) -> List[int]:
        """Process multiple test cases and return results.

        Args:
            test_cases: List of tuples, each containing (n, a) where
                        n is the length of the array and a is the array.

        Returns:
            List of integers, each representing the answer for a test case.
        """
        results: List[int] = []
        for n, a in test_cases:
            result = MochaArrayMedianMagic.find_max_uniform_value(a)
            results.append(result)
        return results

    @staticmethod
    def find_max_uniform_value(a: List[int]) -> int:
        """Find the maximum value that can be made uniform in the array.

        Args:
            a: List of integers representing the array.

        Returns:
            The maximum value that can be made uniform via the allowed operation.
        """
        n: int = len(a)
        max_value: int = max(a)
        count: int = 0
        first_pos: int = -1
        last_pos: int = -1

        for idx, val in enumerate(a):
            if val == max_value:
                count += 1
                if first_pos == -1:
                    first_pos = idx
                last_pos = idx

        # If the maximum value appears at least twice, we can make the whole array max_value
        if count >= 2:
            return max_value
        # If it appears only once, but at the ends, we can also make the whole array max_value
        if first_pos == 0 or last_pos == n - 1:
            return max_value

        # Otherwise, need to find the next largest value that appears at least twice or at the ends
        # Remove all max_value and repeat the process
        candidates: List[int] = [val for val in a if val != max_value]
        if not candidates:
            return max_value  # All elements are max_value

        next_max: int = max(candidates)
        count_next: int = 0
        first_next: int = -1
        last_next: int = -1
        for idx, val in enumerate(a):
            if val == next_max:
                count_next += 1
                if first_next == -1:
                    first_next = idx
                last_next = idx
        if count_next >= 2 or first_next == 0 or last_next == n - 1:
            return next_max

        # Fallback: return the next maximum value found
        return next_max


class Main:
    """Main class for input/output and program flow."""

    @staticmethod
    def read_input() -> List[Tuple[int, List[int]]]:
        """Reads input from stdin.

        Returns:
            List of test cases, each as a tuple (n, a).
        """
        import sys

        input_lines = sys.stdin.read().splitlines()
        test_cases: List[Tuple[int, List[int]]] = []
        idx: int = 0
        t: int = int(input_lines[idx])
        idx += 1
        for _ in range(t):
            n: int = int(input_lines[idx])
            idx += 1
            a: List[int] = list(map(int, input_lines[idx].split()))
            idx += 1
            test_cases.append((n, a))
        return test_cases

    @staticmethod
    def print_output(results: List[int]) -> None:
        """Prints the results to stdout.

        Args:
            results: List of integers to print, one per line.
        """
        for res in results:
            print(res)

    @staticmethod
    def main() -> None:
        """Main program entry point."""
        test_cases = Main.read_input()
        results = MochaArrayMedianMagic.process_test_cases(test_cases)
        Main.print_output(results)


if __name__ == "__main__":
    Main.main()
