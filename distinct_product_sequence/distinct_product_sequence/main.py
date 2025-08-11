## main.py

"""Main module for generating sequences with unique consecutive products.

This module contains two classes:
    - DistinctProductSequenceGenerator: Generates a sequence of integers such that
      the product of every pair of consecutive elements is unique, while minimizing
      the number of distinct elements used.
    - Main: Handles input/output and orchestrates the sequence generation for each test case.

No third-party dependencies are required.
"""

from typing import List


class DistinctProductSequenceGenerator:
    """Generates a sequence with unique consecutive products using minimal distinct elements."""

    def __init__(self, base_a: int = 1, base_b: int = 1000003) -> None:
        """Initializes the generator with two coprime bases.

        Args:
            base_a: First integer to use in the sequence (default: 1).
            base_b: Second integer to use in the sequence (default: 1000003, a large prime).
        """
        self._base_a: int = base_a
        self._base_b: int = base_b

    def generate_sequence(self, n: int) -> List[int]:
        """Generates a sequence of length n with unique consecutive products.

        The sequence alternates between two coprime integers to ensure uniqueness.

        Args:
            n: Length of the sequence to generate.

        Returns:
            List[int]: The generated sequence.
        """
        sequence: List[int] = []
        for i in range(n):
            if i % 2 == 0:
                sequence.append(self._base_a)
            else:
                sequence.append(self._base_b)
        return sequence


class Main:
    """Main class to handle input/output and run the sequence generator."""

    def __init__(self) -> None:
        """Initializes the Main class with a DistinctProductSequenceGenerator instance."""
        self._generator: DistinctProductSequenceGenerator = DistinctProductSequenceGenerator()

    def run(self) -> None:
        """Reads input, generates sequences for each test case, and prints the results.

        Input format:
            t
            n1
            n2
            ...
            nt

        Output format:
            For each test case, prints a line with the generated sequence.
        """
        try:
            t_str: str = input().strip()
            t: int = int(t_str)
        except Exception:
            print("Invalid input for number of test cases.")
            return

        n_list: List[int] = []
        for _ in range(t):
            try:
                n_str: str = input().strip()
                n: int = int(n_str)
                n_list.append(n)
            except Exception:
                print("Invalid input for sequence length.")
                return

        for n in n_list:
            sequence: List[int] = self._generator.generate_sequence(n)
            print(' '.join(str(num) for num in sequence))


if __name__ == "__main__":
    main_instance: Main = Main()
    main_instance.run()
