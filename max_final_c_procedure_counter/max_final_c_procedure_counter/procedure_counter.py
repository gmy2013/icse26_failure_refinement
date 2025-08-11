## procedure_counter.py

from typing import List, Dict
from collections import defaultdict

class ProcedureCounter:
    """Class to count the number of unique procedures that result in the maximum final value of c."""

    MOD: int = 10**9 + 7

    @staticmethod
    def count_max_procedures(a: List[int]) -> int:
        """Counts the number of unique procedures that result in the maximum final value of c.

        Args:
            a (List[int]): The list of integers representing the sequence.

        Returns:
            int: The number of unique procedures (modulo MOD) that result in the maximum final value of c.
        """
        # DP state: maps current value of c to number of ways to reach it
        dp: Dict[int, int] = defaultdict(int)
        dp[0] = 1  # Start with c = 0, one way

        for ai in a:
            next_dp: Dict[int, int] = defaultdict(int)
            for c_val, count in dp.items():
                # Option 1: c + a_i
                new_c1 = c_val + ai
                next_dp[new_c1] = (next_dp[new_c1] + count) % ProcedureCounter.MOD

                # Option 2: |c + a_i|
                new_c2 = abs(c_val + ai)
                next_dp[new_c2] = (next_dp[new_c2] + count) % ProcedureCounter.MOD
            dp = next_dp

        if not dp:
            return 0

        max_c = max(dp.keys())
        return dp[max_c] % ProcedureCounter.MOD
