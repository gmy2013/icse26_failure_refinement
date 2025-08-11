## main.py

from typing import List, Set


class Substring1100Checker:
    """Efficiently checks and updates presence of substring '1100' in a mutable string."""

    def __init__(self, s: str) -> None:
        """Initializes the checker with the given string.

        Args:
            s: The initial binary string.
        """
        self.s: List[str] = list(s)
        self.n: int = len(s)
        # Set of starting indices where '1100' occurs
        self.has_1100: Set[int] = set()
        for i in range(self.n - 3):
            if self._is_1100(i):
                self.has_1100.add(i)

    def update(self, i: int, v: str) -> bool:
        """Updates the character at position i to v and checks for '1100'.

        Args:
            i: The 0-based index to update.
            v: The new character ('0' or '1').

        Returns:
            True if '1100' exists in the string after the update, False otherwise.
        """
        if self.s[i] == v:
            # No change, so no need to update
            return self.contains_1100()
        self.s[i] = v
        # Only substrings starting at i-3, i-2, i-1, i can be affected
        for pos in range(max(0, i - 3), min(self.n - 3, i) + 1):
            self._check_and_update(pos)
        return self.contains_1100()

    def _is_1100(self, pos: int) -> bool:
        """Checks if substring starting at pos is '1100'."""
        return (
            pos >= 0 and
            pos + 3 < self.n and
            self.s[pos] == '1' and
            self.s[pos + 1] == '1' and
            self.s[pos + 2] == '0' and
            self.s[pos + 3] == '0'
        )

    def _check_and_update(self, pos: int) -> None:
        """Updates the has_1100 set for the substring starting at pos."""
        if self._is_1100(pos):
            self.has_1100.add(pos)
        else:
            self.has_1100.discard(pos)

    def contains_1100(self) -> bool:
        """Returns True if '1100' exists in the string, False otherwise."""
        return bool(self.has_1100)


class Main:
    """Handles input/output and test case processing."""

    @staticmethod
    def main() -> None:
        """Main entry point for the program."""
        import sys

        input_lines = sys.stdin.read().splitlines()
        line_idx: int = 0

        t: int = int(input_lines[line_idx])
        line_idx += 1

        for _ in range(t):
            s: str = input_lines[line_idx].strip()
            line_idx += 1
            q: int = int(input_lines[line_idx])
            line_idx += 1

            checker = Substring1100Checker(s)
            for _ in range(q):
                parts = input_lines[line_idx].split()
                line_idx += 1
                i: int = int(parts[0]) - 1  # Convert to 0-based index
                v: str = parts[1]
                result: bool = checker.update(i, v)
                print('YES' if result else 'NO')


if __name__ == "__main__":
    Main.main()
