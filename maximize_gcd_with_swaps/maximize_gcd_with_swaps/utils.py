## utils.py
import os
from typing import List, Tuple

class Utils:
    """
    Utility class for handling input and output operations.
    """

    @staticmethod
    def read_input(file_path: str) -> Tuple[List[int], List[int], List[int], List[int], List[int]]:
        """
        Reads input from a file and parses it into required data structures.

        Args:
            file_path (str): Path to the input file.

        Returns:
            Tuple[List[int], List[int], List[int], List[int], List[int]]:
                - a: List of integers representing array A.
                - b: List of integers representing array B.
                - c: List of integers representing swap costs.
                - budgets: List of integers representing budget constraints.
                - additional_data: List of integers for any additional data (if needed).
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")

        a, b, c, budgets, additional_data = [], [], [], [], []

        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if len(lines) < 4:
                    raise ValueError("Input file must contain at least four lines.")

                # Parse array A
                a = list(map(int, lines[0].strip().split()))
                # Parse array B
                b = list(map(int, lines[1].strip().split()))
                # Parse swap costs
                c = list(map(int, lines[2].strip().split()))
                # Parse budgets
                budgets = list(map(int, lines[3].strip().split()))

                # Parse additional data if present
                if len(lines) > 4:
                    additional_data = list(map(int, lines[4].strip().split()))

        except Exception as e:
            raise ValueError(f"Error reading input file: {e}")

        return a, b, c, budgets, additional_data

    @staticmethod
    def write_output(results: List[int], file_path: str) -> None:
        """
        Writes the results to an output file.

        Args:
            results (List[int]): List of integers representing the results to be written.
            file_path (str): Path to the output file.

        Returns:
            None
        """
        try:
            with open(file_path, 'w') as file:
                for result in results:
                    file.write(f"{result}\n")
        except Exception as e:
            raise ValueError(f"Error writing to output file: {e}")

    @staticmethod
    def validate_input_data(a: List[int], b: List[int], c: List[int], budgets: List[int]) -> None:
        """
        Validates the input data to ensure it meets expected constraints.

        Args:
            a (List[int]): Array A.
            b (List[int]): Array B.
            c (List[int]): Swap costs.
            budgets (List[int]): Budget constraints.

        Returns:
            None

        Raises:
            ValueError: If any input data is invalid.
        """
        if not all(isinstance(x, int) for x in a):
            raise ValueError("Array A must contain only integers.")
        if not all(isinstance(x, int) for x in b):
            raise ValueError("Array B must contain only integers.")
        if not all(isinstance(x, int) for x in c):
            raise ValueError("Swap costs must contain only integers.")
        if not all(isinstance(x, int) for x in budgets):
            raise ValueError("Budgets must contain only integers.")

        if len(a) != len(b):
            raise ValueError("Array A and Array B must have the same length.")
        if len(c) != len(a):
            raise ValueError("Swap costs must have the same length as Array A.")

    @staticmethod
    def log_message(message: str, log_file: str = "utils.log") -> None:
        """
        Logs a message to a specified log file.

        Args:
            message (str): The message to log.
            log_file (str): Path to the log file. Defaults to "utils.log".

        Returns:
            None
        """
        try:
            with open(log_file, 'a') as file:
                file.write(f"{message}\n")
        except Exception as e:
            raise ValueError(f"Error writing to log file: {e}")
