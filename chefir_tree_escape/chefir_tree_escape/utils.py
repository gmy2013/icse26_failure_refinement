## utils.py

from typing import List, Tuple, Any, Optional
import sys

class InputParser:
    """Utility class for parsing input for the tree query system."""

    @staticmethod
    def parse_input() -> Tuple[List[Any], List[List[Tuple[int, int]]]]:
        """Parses input from stdin in a competitive programming style.

        Returns:
            Tuple[List[Any], List[List[Tuple[int, int]]]]:
                - List of tree data (each as a tuple: (n, edge_list))
                - List of queries for each tree (each as a list of (v, stamina) tuples)
        """
        input_lines = sys.stdin.read().splitlines()
        idx: int = 0
        num_cases: int = 1  # Default to 1 test case unless specified

        # Check if the first line is the number of test cases
        if input_lines and input_lines[0].isdigit():
            num_cases = int(input_lines[0])
            idx += 1

        trees: List[Tuple[int, List[Tuple[int, int]]]] = []
        all_queries: List[List[Tuple[int, int]]] = []

        for _ in range(num_cases):
            # Parse number of nodes
            n: int = int(input_lines[idx])
            idx += 1

            # Parse edges
            edge_list: List[Tuple[int, int]] = []
            for _ in range(n - 1):
                u_str, v_str = input_lines[idx].split()
                u, v = int(u_str), int(v_str)
                edge_list.append((u, v))
                idx += 1

            trees.append((n, edge_list))

            # Parse number of queries
            q: int = int(input_lines[idx])
            idx += 1

            queries: List[Tuple[int, int]] = []
            for _ in range(q):
                v_str, stamina_str = input_lines[idx].split()
                v, stamina = int(v_str), int(stamina_str)
                queries.append((v, stamina))
                idx += 1

            all_queries.append(queries)

        return trees, all_queries


class OutputFormatter:
    """Utility class for formatting and printing output."""

    @staticmethod
    def format_output(results: List[List[int]]) -> None:
        """Prints the results for all test cases.

        Args:
            results (List[List[int]]): List of results per test case, each as a list of integers.
        """
        for case_results in results:
            for res in case_results:
                print(res)
