## main.py

from typing import List, Tuple
import sys
import itertools

class BoxPlacementSolver:
    """Solver for finding the maximum number of box placements."""

    def __init__(self) -> None:
        """Initializes the BoxPlacementSolver."""
        pass

    def max_placements(self, x: int, y: int, z: int, k: int) -> int:
        """Calculates the number of valid (a, b, c) placements.

        Args:
            x (int): Maximum length along the first dimension.
            y (int): Maximum length along the second dimension.
            z (int): Maximum length along the third dimension.
            k (int): The product constraint a * b * c = k.

        Returns:
            int: The number of valid placements.
        """
        triplets = self._divisor_triplets(k, x, y, z)
        return len(triplets)

    def _divisor_triplets(
        self, k: int, x: int, y: int, z: int
    ) -> List[Tuple[int, int, int]]:
        """Generates all valid (a, b, c) triplets such that a * b * c = k and
        1 <= a <= x, 1 <= b <= y, 1 <= c <= z.

        Args:
            k (int): The product constraint.
            x (int): Maximum for a.
            y (int): Maximum for b.
            z (int): Maximum for c.

        Returns:
            List[Tuple[int, int, int]]: List of valid (a, b, c) triplets.
        """
        valid_triplets = []
        # Enumerate all divisors a of k such that 1 <= a <= x
        for a in self._divisors_up_to(k, x):
            k1 = k // a
            # Enumerate all divisors b of k1 such that 1 <= b <= y
            for b in self._divisors_up_to(k1, y):
                c = k1 // b
                if 1 <= c <= z and a * b * c == k:
                    # Each permutation of (a, b, c) is a distinct placement
                    for triplet in set(itertools.permutations((a, b, c), 3)):
                        # Check if the triplet fits in (x, y, z) in order
                        if (
                            1 <= triplet[0] <= x
                            and 1 <= triplet[1] <= y
                            and 1 <= triplet[2] <= z
                        ):
                            valid_triplets.append(triplet)
                    # Also include the (a, b, c) itself if not all values are distinct
                    # (itertools.permutations with r=3 omits repeated values for r < n)
                    if (a, b, c) not in valid_triplets:
                        if (
                            1 <= a <= x
                            and 1 <= b <= y
                            and 1 <= c <= z
                        ):
                            valid_triplets.append((a, b, c))
        # Remove duplicates (can occur if a==b==c or two values are equal)
        unique_triplets = list(set(valid_triplets))
        return unique_triplets

    def _divisors_up_to(self, n: int, limit: int) -> List[int]:
        """Finds all divisors of n up to a given limit.

        Args:
            n (int): The number to find divisors of.
            limit (int): The upper bound for divisors.

        Returns:
            List[int]: List of divisors of n not exceeding limit.
        """
        divisors = set()
        i = 1
        while i * i <= n:
            if n % i == 0:
                if i <= limit:
                    divisors.add(i)
                if n // i <= limit:
                    divisors.add(n // i)
            i += 1
        return list(divisors)


class MainApp:
    """Main application class for running the box placement solver."""

    def __init__(self) -> None:
        """Initializes the MainApp."""
        self.solver = BoxPlacementSolver()

    def run(self) -> None:
        """Runs the main application loop."""
        try:
            t = self._read_int("Enter number of test cases: ")
            for case_num in range(1, t + 1):
                x, y, z, k = self._read_case(case_num)
                result = self.solver.max_placements(x, y, z, k)
                print(result)
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)

    def _read_int(self, prompt: str) -> int:
        """Reads an integer from input with a prompt.

        Args:
            prompt (str): The prompt to display.

        Returns:
            int: The integer read.
        """
        while True:
            try:
                value = int(input(prompt))
                if value < 1:
                    raise ValueError("Value must be at least 1.")
                return value
            except ValueError as ve:
                print(f"Invalid input: {ve}")

    def _read_case(self, case_num: int) -> Tuple[int, int, int, int]:
        """Reads a single test case.

        Args:
            case_num (int): The test case number.

        Returns:
            Tuple[int, int, int, int]: The values x, y, z, k.
        """
        while True:
            try:
                line = input(
                    f"Test case {case_num}: Enter x y z k (space-separated): "
                )
                parts = line.strip().split()
                if len(parts) != 4:
                    raise ValueError("Exactly four integers required.")
                x, y, z, k = map(int, parts)
                if min(x, y, z, k) < 1:
                    raise ValueError("All values must be at least 1.")
                return x, y, z, k
            except ValueError as ve:
                print(f"Invalid input: {ve}")


if __name__ == "__main__":
    app = MainApp()
    app.run()
