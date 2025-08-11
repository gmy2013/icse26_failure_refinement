## output_formatter.py

"""OutputFormatter module for formatting boss battle calculation results.

This module provides the OutputFormatter class, which formats the results
of batch boss battle calculations for standard output.

Classes:
    OutputFormatter: Formats output for batch processing results.
"""

from typing import List


class OutputFormatter:
    """Formats output for the boss battle calculator.

    Methods:
        format_output(results): Formats a list of results for output.
    """

    def __init__(self) -> None:
        """Initializes the OutputFormatter."""
        pass

    def format_output(self, results: List[int]) -> str:
        """Formats the list of results for output.

        Each result is printed on a separate line.

        Args:
            results: List of integers, each representing the minimum number of turns
                     to defeat the boss for a test case.

        Returns:
            A string with each result on its own line, suitable for printing.
        """
        if not results:
            return ""
        return "\n".join(str(result) for result in results)
