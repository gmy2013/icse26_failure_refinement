## main.py

from typing import Tuple
from matcher import PatternMatcher

## matcher.py

class PatternMatcher:
    """PatternMatcher provides string matching with custom wildcards.

    Wildcards:
        '-' : matches exactly one character.
        '*' : matches any sequence of characters (including empty).
    """

    def __init__(self) -> None:
        """Initializes the PatternMatcher."""
        pass

    def can_match(self, s: str, t: str) -> bool:
        """Determines if s and t can match, considering custom wildcards.

        Args:
            s (str): First string, may contain '-' and '*'.
            t (str): Second string, may contain '-' and '*'.

        Returns:
            bool: True if s and t can match, False otherwise.
        """
        return self._match(s, t)

    def _match(self, s: str, t: str) -> bool:
        """Internal matching logic using two-pointer approach.

        Args:
            s (str): First string.
            t (str): Second string.

        Returns:
            bool: True if s and t can match, False otherwise.
        """
        len_s = len(s)
        len_t = len(t)
        i = j = 0
        star_s = star_t = -1
        match_s = match_t = 0

        while i < len_s or j < len_t:
            # Both pointers in range
            if i < len_s and j < len_t:
                if s[i] == t[j]:
                    if s[i] == '*':
                        # Both are '*', record positions and try to expand both
                        star_s, match_s = i, j
                        star_t, match_t = j, i
                        i += 1
                        j += 1
                    elif s[i] == '-':
                        # Both are '-', match one character
                        i += 1
                        j += 1
                    else:
                        # Both are same character
                        i += 1
                        j += 1
                elif s[i] == '*':
                    # s has '*', try to match zero or more in t
                    star_s, match_s = i, j
                    i += 1
                elif t[j] == '*':
                    # t has '*', try to match zero or more in s
                    star_t, match_t = j, i
                    j += 1
                elif s[i] == '-':
                    # s has '-', match any single character in t
                    i += 1
                    j += 1
                elif t[j] == '-':
                    # t has '-', match any single character in s
                    i += 1
                    j += 1
                else:
                    # Mismatch, try to backtrack if possible
                    if star_s != -1:
                        # Backtrack on s's '*'
                        i = star_s + 1
                        match_s += 1
                        j = match_s
                    elif star_t != -1:
                        # Backtrack on t's '*'
                        j = star_t + 1
                        match_t += 1
                        i = match_t
                    else:
                        return False
            elif i < len_s:
                # Only s remains
                if s[i] == '*':
                    i += 1
                elif s[i] == '-':
                    if j < len_t:
                        i += 1
                        j += 1
                    else:
                        return False
                else:
                    if star_t != -1:
                        # Backtrack on t's '*'
                        j = star_t + 1
                        match_t += 1
                        i = match_t
                    else:
                        return False
            elif j < len_t:
                # Only t remains
                if t[j] == '*':
                    j += 1
                elif t[j] == '-':
                    if i < len_s:
                        i += 1
                        j += 1
                    else:
                        return False
                else:
                    if star_s != -1:
                        # Backtrack on s's '*'
                        i = star_s + 1
                        match_s += 1
                        j = match_s
                    else:
                        return False
            else:
                # Both finished
                break

        # Skip trailing '*' in s
        while i < len_s and s[i] == '*':
            i += 1
        # Skip trailing '*' in t
        while j < len_t and t[j] == '*':
            j += 1

        return i == len_s and j == len_t

class CLI:
    """CLI handles command-line interface for the pattern matcher."""

    def __init__(self) -> None:
        """Initializes the CLI."""
        self.matcher = PatternMatcher()

    def run(self) -> None:
        """Runs the CLI: parses input, processes, and prints result."""
        s, t = self._parse_input()
        result = self.matcher.can_match(s, t)
        self._print_result(result)

    def _parse_input(self) -> Tuple[str, str]:
        """Parses input from stdin.

        Returns:
            Tuple[str, str]: The two input strings to be matched.
        """
        try:
            s = input().rstrip('\n')
            t = input().rstrip('\n')
        except EOFError:
            s = ''
            t = ''
        return s, t

    def _print_result(self, result: bool) -> None:
        """Prints the result to stdout.

        Args:
            result (bool): The result of the pattern match.
        """
        print('Yes' if result else 'No')


if __name__ == '__main__':
    cli = CLI()
    cli.run()
