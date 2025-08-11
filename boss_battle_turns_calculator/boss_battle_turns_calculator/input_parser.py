## input_parser.py

"""InputParser module for parsing CLI input for boss battle calculation.

This module provides the InputParser class, which reads and parses standard input
for batch processing of boss battle test cases.

Classes:
    InputParser: Parses input and returns structured test case data.
"""

from typing import List, Tuple


class InputParser:
    """Parses input for the boss battle calculator.

    Methods:
        parse_input(): Reads and parses input, returning test case data.
    """

    def __init__(self) -> None:
        """Initializes the InputParser."""
        pass

    def parse_input(self) -> Tuple[int, List[Tuple[int, int, List[int], List[int]]]]:
        """Parses standard input for batch boss battle test cases.

        Input format (from stdin):
            t
            n1 h1
            d1_1 d1_2 ... d1_n1
            c1_1 c1_2 ... c1_n1
            n2 h2
            d2_1 d2_2 ... d2_n2
            c2_1 c2_2 ... c2_n2
            ...
        Where:
            t: number of test cases
            For each test case:
                n: number of attacks
                h: boss health
                d: damages (n integers)
                c: cooldowns (n integers)

        Returns:
            A tuple (t, test_cases), where test_cases is a list of tuples:
                (n, h, damages, cooldowns)
        """
        import sys

        lines: List[str] = []
        for line in sys.stdin:
            line = line.strip()
            if line:
                lines.append(line)

        if not lines:
            raise ValueError("No input provided.")

        line_idx: int = 0
        t: int = int(lines[line_idx])
        line_idx += 1

        test_cases: List[Tuple[int, int, List[int], List[int]]] = []

        for _ in range(t):
            if line_idx >= len(lines):
                raise ValueError("Insufficient input for test cases.")

            # Parse n and h
            n_h_line: List[str] = lines[line_idx].split()
            if len(n_h_line) != 2:
                raise ValueError(f"Expected two integers for n and h, got: {lines[line_idx]}")
            n: int = int(n_h_line[0])
            h: int = int(n_h_line[1])
            line_idx += 1

            # Parse damages
            if line_idx >= len(lines):
                raise ValueError("Missing damages line for test case.")
            damages_line: List[str] = lines[line_idx].split()
            if len(damages_line) != n:
                raise ValueError(f"Expected {n} damages, got: {lines[line_idx]}")
            damages: List[int] = [int(x) for x in damages_line]
            line_idx += 1

            # Parse cooldowns
            if line_idx >= len(lines):
                raise ValueError("Missing cooldowns line for test case.")
            cooldowns_line: List[str] = lines[line_idx].split()
            if len(cooldowns_line) != n:
                raise ValueError(f"Expected {n} cooldowns, got: {lines[line_idx]}")
            cooldowns: List[int] = [int(x) for x in cooldowns_line]
            line_idx += 1

            test_cases.append((n, h, damages, cooldowns))

        return t, test_cases
