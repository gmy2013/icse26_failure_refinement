## main.py

"""CLIHandler for string partitioning problem.

This module implements the CLIHandler class, which provides a command-line interface
for counting and displaying valid substrings t (t ≠ 'a') such that the input string s
can be partitioned into substrings where each substring is either t or 'a', and at least
one substring is t.

Dependencies:
    - argparse (for CLI argument parsing)
    - string_partition_counter.StringPartitionCounter
    - typing
"""

import argparse
from typing import Set
from string_partition_counter import StringPartitionCounter


class CLIHandler:
    """Command-line interface handler for the string partitioning problem."""

    def __init__(self, counter: StringPartitionCounter) -> None:
        """Initialize the CLIHandler with a StringPartitionCounter instance.

        Args:
            counter (StringPartitionCounter): The core algorithm instance.
        """
        self.counter = counter

    def parse_args(self) -> str:
        """Parse command-line arguments to get the input string.

        Returns:
            str: The input string s.
        """
        parser = argparse.ArgumentParser(
            description=(
                "Count the number of valid substrings t (t ≠ 'a') such that "
                "the input string s can be partitioned into substrings where each "
                "substring is either t or 'a', and at least one substring is t."
            )
        )
        parser.add_argument(
            "s",
            type=str,
            help="Input string s (nonempty, lowercase Latin letters only)."
        )
        args = parser.parse_args()
        return args.s

    def display_result(self, count: int, t_set: Set[str]) -> None:
        """Display the result to the user.

        Args:
            count (int): The number of valid t substrings.
            t_set (Set[str]): The set of valid t substrings.
        """
        print(f"Number of valid t substrings: {count}")
        if count > 0:
            print("Valid t substrings:")
            for t in sorted(t_set):
                print(f"- {t}")
        else:
            print("No valid t substrings found.")

    def run(self) -> None:
        """Run the CLI handler: parse input, compute, and display result."""
        s: str = self.parse_args()
        count: int = self.counter.count_valid_t(s)
        t_set: Set[str] = self.counter.get_valid_t(s)
        self.display_result(count, t_set)


if __name__ == "__main__":
    counter = StringPartitionCounter()
    cli = CLIHandler(counter)
    cli.run()
