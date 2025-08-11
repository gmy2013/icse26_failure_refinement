## main.py

from typing import List, Tuple


class CarpetLayerCounter:
    """Provides methods to extract matrix layers and count '1543' occurrences."""

    @staticmethod
    def count_1543_in_layers(matrix: List[List[str]]) -> int:
        """Counts all (overlapping) occurrences of '1543' in all layers of the matrix.

        Args:
            matrix: 2D list of single-character strings representing the matrix.

        Returns:
            Total count of '1543' substrings in all layers.
        """
        layers = CarpetLayerCounter.extract_layers(matrix)
        total_count = 0
        for layer_str in layers:
            total_count += CarpetLayerCounter.count_substring(layer_str, '1543')
        return total_count

    @staticmethod
    def extract_layers(matrix: List[List[str]]) -> List[str]:
        """Extracts all layers of the matrix in clockwise order as strings.

        Args:
            matrix: 2D list of single-character strings.

        Returns:
            List of strings, each representing a layer in clockwise order.
        """
        if not matrix or not matrix[0]:
            return []

        n = len(matrix)
        m = len(matrix[0])
        layers = []
        num_layers = (min(n, m) + 1) // 2

        for layer in range(num_layers):
            layer_chars = []

            # Top row (left to right)
            for col in range(layer, m - layer):
                layer_chars.append(matrix[layer][col])

            # Right column (top to bottom, excluding top)
            for row in range(layer + 1, n - layer):
                if m - layer - 1 >= layer:
                    layer_chars.append(matrix[row][m - layer - 1])

            # Bottom row (right to left, excluding rightmost if not same as top)
            if n - layer - 1 != layer:
                for col in range(m - layer - 2, layer - 1, -1):
                    layer_chars.append(matrix[n - layer - 1][col])

            # Left column (bottom to top, excluding bottom and top)
            if m - layer - 1 != layer:
                for row in range(n - layer - 2, layer, -1):
                    layer_chars.append(matrix[row][layer])

            layers.append(''.join(layer_chars))

        return layers

    @staticmethod
    def count_substring(s: str, sub: str) -> int:
        """Counts overlapping occurrences of substring 'sub' in string 's'.

        Args:
            s: The string to search in.
            sub: The substring to search for.

        Returns:
            The number of (overlapping) occurrences of sub in s.
        """
        count = 0
        sub_len = len(sub)
        for i in range(len(s) - sub_len + 1):
            if s[i:i + sub_len] == sub:
                count += 1
        return count


class InputHandler:
    """Handles input parsing from stdin."""

    @staticmethod
    def read_input() -> Tuple[int, List[Tuple[int, int, List[List[str]]]]]:
        """Reads input from stdin.

        Returns:
            A tuple containing:
                - t: number of test cases
                - test_cases: list of tuples (n, m, matrix)
        """
        import sys

        lines = []
        for line in sys.stdin:
            if line.strip() == '':
                continue
            lines.append(line.rstrip('\n'))

        idx = 0
        t = int(lines[idx])
        idx += 1
        test_cases = []

        for _ in range(t):
            n_m = lines[idx].split()
            n = int(n_m[0])
            m = int(n_m[1])
            idx += 1
            matrix = []
            for _ in range(n):
                row = list(lines[idx].strip())
                matrix.append(row)
                idx += 1
            test_cases.append((n, m, matrix))

        return t, test_cases


class OutputHandler:
    """Handles output to stdout."""

    @staticmethod
    def print_results(results: List[int]) -> None:
        """Prints the results, one per line.

        Args:
            results: List of integer results to print.
        """
        for res in results:
            print(res)


class Main:
    """Main application class."""

    @staticmethod
    def main() -> None:
        """Main entry point for the program."""
        t, test_cases = InputHandler.read_input()
        results: List[int] = []
        for _, _, matrix in test_cases:
            count = CarpetLayerCounter.count_1543_in_layers(matrix)
            results.append(count)
        OutputHandler.print_results(results)


if __name__ == "__main__":
    Main.main()
