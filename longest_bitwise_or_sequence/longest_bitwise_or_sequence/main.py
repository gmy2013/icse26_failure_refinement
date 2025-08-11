## main.py

from typing import List


class SequenceGenerator:
    """Generates the longest strictly increasing sequence a for a given n,
    such that for all i >= 2, a_i | a_{i-1} == n, a_i > a_{i-1}, and a_i <= n.
    The sequence is constructed to be lexicographically smallest.
    """

    def generate_sequence(self, n: int) -> List[int]:
        """Generate the required sequence for a given n.

        Args:
            n (int): The target integer.

        Returns:
            List[int]: The generated sequence.
        """
        # Find all bit positions set in n (from least to most significant)
        bit_positions = []
        for bit in range(n.bit_length()):
            if (n >> bit) & 1:
                bit_positions.append(bit)

        # Build the sequence by setting bits from least to most significant
        sequence = []
        current = 0
        for bit in bit_positions:
            current |= (1 << bit)
            sequence.append(current)
        return sequence


class CLI:
    """Command-line interface for the sequence generator."""

    def __init__(self) -> None:
        """Initialize the CLI with a SequenceGenerator instance."""
        self.sequence_generator = SequenceGenerator()

    def run(self) -> None:
        """Run the CLI, handling user input and output."""
        try:
            t_input = input().strip()
            t = int(t_input)
        except Exception:
            print("Invalid input for number of test cases.")
            return

        n_values: List[int] = []
        for _ in range(t):
            try:
                n_input = input().strip()
                n = int(n_input)
                n_values.append(n)
            except Exception:
                print("Invalid input for n.")
                return

        for n in n_values:
            sequence = self.sequence_generator.generate_sequence(n)
            print(len(sequence))
            print(' '.join(str(num) for num in sequence))


if __name__ == "__main__":
    cli = CLI()
    cli.run()
