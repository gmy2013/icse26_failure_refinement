## input_validator.py

"""Input validation utilities for the hidden array solver.

This module provides the InputValidator class, which validates the input
parameters for the hidden array problem. It checks the types, ranges, and
consistency of the input values and raises ValueError with descriptive
messages if any validation fails.

Classes:
    InputValidator: Validates n, m, b, s for the hidden array problem.
"""

from typing import List


class InputValidator:
    """Validates input for the hidden array solver.

    Methods:
        validate(n, m, b, s): Validates the input parameters.
    """

    def __init__(self) -> None:
        """Initializes the InputValidator."""
        pass

    def validate(self, n: int, m: int, b: List[int], s: str) -> None:
        """Validates the input parameters for the hidden array problem.

        Args:
            n (int): The length of the array and string.
            m (int): The maximum absolute value allowed for elements in array a.
            b (List[int]): The list of prefix/suffix sum constraints.
            s (str): The string with digits and '?'.

        Raises:
            ValueError: If any input is invalid.
        """
        # Check types
        if not isinstance(n, int):
            raise ValueError("n must be an integer.")
        if not isinstance(m, int):
            raise ValueError("m must be an integer.")
        if not isinstance(b, list):
            raise ValueError("b must be a list of integers.")
        if not isinstance(s, str):
            raise ValueError("s must be a string.")

        # Check n and m ranges
        if n <= 0:
            raise ValueError("n must be a positive integer.")
        if m < 0:
            raise ValueError("m must be a non-negative integer.")

        # Check b length and element types
        if len(b) != n:
            raise ValueError(f"b must have length n={n}, but got {len(b)}.")
        for idx, val in enumerate(b):
            if not isinstance(val, int):
                raise ValueError(f"b[{idx}] is not an integer: {val}")

        # Check s length and allowed characters
        if len(s) != n:
            raise ValueError(f"s must have length n={n}, but got {len(s)}.")
        for idx, ch in enumerate(s):
            if not (ch.isdigit() or ch == '?'):
                raise ValueError(
                    f"s contains invalid character at position {idx}: '{ch}'. "
                    "Allowed: digits '0'-'9' and '?'."
                )

        # Check that digits in s are within allowed range for a_i
        for idx, ch in enumerate(s):
            if ch.isdigit():
                digit = int(ch)
                if digit < -m or digit > m:
                    raise ValueError(
                        f"s[{idx}] = '{ch}' is out of allowed range [-m, m] = [{-m}, {m}]."
                    )

        # Check that b values are within possible sum range
        min_sum = -m * n
        max_sum = m * n
        for idx, val in enumerate(b):
            if val < min_sum or val > max_sum:
                raise ValueError(
                    f"b[{idx}] = {val} is out of possible sum range [{min_sum}, {max_sum}]."
                )
