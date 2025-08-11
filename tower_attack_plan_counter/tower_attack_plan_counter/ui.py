## ui.py

"""
UI module for the minimal-length attack plan system.

Implements the UI class, which provides:
- run(): Launches the Streamlit web interface for user interaction.
- parse_input(input_str): Parses user input into a list of (x, y) tuples.
- display_result(num_plans, sample_plan): Displays the result in the UI.
- display_impossible(): Displays an error message for impossible cases.

Depends on:
    - streamlit (for web UI)
    - attack_plan.py (AttackPlanSolver)
"""

from typing import List, Tuple
import streamlit as st
from attack_plan import AttackPlanSolver


class UI:
    """User interface class for the attack plan system."""

    def run(self) -> None:
        """Run the Streamlit web UI."""
        st.set_page_config(page_title="Minimal Attack Plan Solver", layout="centered")
        st.title("Minimal-Length Attack Plan Solver")
        st.markdown(
            """
            Enter the coordinates of the towers (one per line, format: x y), and the system will compute
            the number of minimal-length attack plans to capture all towers according to the geometric rules.
            """
        )

        default_input = "0 0\n1 0\n0 1\n1 1"
        input_str = st.text_area(
            "Tower coordinates (one per line, format: x y):",
            value=default_input,
            height=150,
            key="input_area"
        )

        mod = st.number_input(
            "Modulo (for result):",
            min_value=1,
            max_value=10**9 + 7,
            value=998244353,
            step=1,
            key="mod_input"
        )

        if st.button("Compute Minimal Attack Plans"):
            try:
                points = self.parse_input(input_str)
                if len(points) < 4:
                    st.error("Please enter at least 4 towers (points).")
                    return
                # By default, the first three towers are considered initially owned
                initial_owned = {0, 1, 2}
                solver = AttackPlanSolver(points, mod)
                # Patch: set the initial owned towers in the DP cache
                solver._dp_cache[frozenset(initial_owned)] = (0, [[]])
                num_plans, sample_plan = solver.count_minimal_attack_plans()
                if num_plans == 0 or not sample_plan:
                    self.display_impossible()
                else:
                    self.display_result(num_plans, sample_plan)
            except Exception as e:
                st.error(f"Error: {e}")

    @staticmethod
    def parse_input(input_str: str) -> List[Tuple[float, float]]:
        """Parse user input into a list of (x, y) tuples.

        Args:
            input_str: Multiline string, each line is 'x y'.

        Returns:
            List of (x, y) tuples.

        Raises:
            ValueError: If input is invalid.
        """
        points: List[Tuple[float, float]] = []
        lines = input_str.strip().splitlines()
        for idx, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 2:
                raise ValueError(f"Line {idx + 1}: Each line must have exactly two numbers.")
            try:
                x, y = float(parts[0]), float(parts[1])
            except ValueError:
                raise ValueError(f"Line {idx + 1}: Invalid number format.")
            points.append((x, y))
        return points

    @staticmethod
    def display_result(num_plans: int, sample_plan: List[int]) -> None:
        """Display the result in the UI.

        Args:
            num_plans: Number of minimal-length attack plans.
            sample_plan: A sample plan (list of attack steps, each step is [p, q, r]).
        """
        st.success(f"Number of minimal-length attack plans: **{num_plans}**")
        st.markdown("### Sample Plan (sequence of attack steps):")
        if not sample_plan:
            st.info("No sample plan available.")
            return
        for step_idx, step in enumerate(sample_plan, 1):
            if isinstance(step, list) and len(step) == 3:
                st.write(f"Step {step_idx}: Attack triangle with towers (indices): {step[0]}, {step[1]}, {step[2]}")
            else:
                st.write(f"Step {step_idx}: {step}")

    @staticmethod
    def display_impossible() -> None:
        """Display an error message for impossible cases."""
        st.error("Impossible to capture all towers with the given rules and initial configuration.")
