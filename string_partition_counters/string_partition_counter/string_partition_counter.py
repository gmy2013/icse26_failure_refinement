## string_partition_counter.py

"""StringPartitionCounter class for counting valid t substrings in string partitioning problem.

This module implements the StringPartitionCounter class, which provides methods to:
- Count the number of valid substrings t (t ≠ 'a') such that the input string s can be partitioned into substrings where each substring is either t or 'a', and at least one substring is t.
- Retrieve the set of all such valid t substrings.
- Check if a given t is a valid partition substring for s.

Dependencies:
    - utils.py (for utility functions)
"""

from typing import Set, Tuple
from utils import get_candidate_t, partition_string, is_all_a, is_valid_input


class StringPartitionCounter:
    """Class for counting and retrieving valid t substrings for string partitioning."""

    def __init__(self) -> None:
        """Initialize the StringPartitionCounter."""
        pass

    def count_valid_t(self, s: str) -> int:
        """Count the number of valid t substrings for the given string s.

        Args:
            s (str): The input string.

        Returns:
            int: The number of valid t substrings.
        """
        valid_t_set = self.get_valid_t(s)
        return len(valid_t_set)

    def get_valid_t(self, s: str) -> Set[str]:
        """Get the set of all valid t substrings for the given string s.

        Args:
            s (str): The input string.

        Returns:
            Set[str]: Set of valid t substrings.
        """
        if not is_valid_input(s):
            return set()
        if is_all_a(s):
            # No valid t if s is all 'a'
            return set()
        candidate_t_set = get_candidate_t(s)
        valid_t_set: Set[str] = set()
        for t in candidate_t_set:
            if self.is_valid_partition(s, t):
                valid_t_set.add(t)
        return valid_t_set

    def is_valid_partition(self, s: str, t: str) -> bool:
        """Check if s can be partitioned into substrings of t and 'a', with at least one t.

        Args:
            s (str): The input string.
            t (str): The candidate substring t (t != 'a').

        Returns:
            bool: True if s can be partitioned as required, False otherwise.
        """
        if t == 'a' or not t:
            return False
        partition = partition_string(s, t)
        if not partition:
            return False
        # At least one t must be present in the partition
        return any(sub == t for sub in partition)
