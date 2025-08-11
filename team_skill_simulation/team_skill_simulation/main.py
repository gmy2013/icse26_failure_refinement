## main.py
from bisect import bisect_left, insort_left
from typing import List, Tuple


class Candidate:
    """Data structure representing a candidate with programming and testing skills."""

    def __init__(self, idx: int, prog_skill: int, test_skill: int) -> None:
        self.idx: int = idx
        self.prog_skill: int = prog_skill
        self.test_skill: int = test_skill

    def __repr__(self) -> str:
        return f"Candidate(idx={self.idx}, prog={self.prog_skill}, test={self.test_skill})"


class TeamSkillSimulator:
    """Core simulation logic for team skill assignment and exclusion."""

    def simulate(
        self, n: int, m: int, prog_skills: List[int], test_skills: List[int]
    ) -> List[int]:
        """
        Simulate the process for a single test case.

        Args:
            n: Number of candidates.
            m: Number of programmers to select.
            prog_skills: List of programming skills.
            test_skills: List of testing skills.

        Returns:
            List of maximum team skills for each candidate exclusion.
        """
        candidates = [
            Candidate(idx, prog_skills[idx], test_skills[idx]) for idx in range(n)
        ]
        return self._exclude_and_simulate(candidates, n, m)

    def _assign_roles(
        self, candidates: List[Candidate], n: int, m: int
    ) -> Tuple[List[int], int]:
        """
        Assign roles to candidates to maximize team skill.

        Args:
            candidates: List of Candidate objects (length n).
            n: Number of candidates.
            m: Number of programmers to select.

        Returns:
            Tuple of (assignment list, total team skill).
            assignment[i] = 1 if candidate i is programmer, 0 if tester.
        """
        # For each candidate, compute diff = prog_skill - test_skill
        # Sort by diff descending: those with largest diff are better as programmers
        diff_list = [
            (cand.prog_skill - cand.test_skill, cand.idx, cand.prog_skill, cand.test_skill)
            for cand in candidates
        ]
        diff_list.sort(reverse=True)

        assignment = [0] * n  # 1 for programmer, 0 for tester
        total_skill = 0

        # Assign top m as programmers
        for i in range(m):
            _, idx, prog, _ = diff_list[i]
            assignment[idx] = 1
            total_skill += prog

        # Assign rest as testers
        for i in range(m, n):
            _, idx, _, test = diff_list[i]
            assignment[idx] = 0
            total_skill += test

        return assignment, total_skill

    def _exclude_and_simulate(
        self, candidates: List[Candidate], n: int, m: int
    ) -> List[int]:
        """
        For each candidate, exclude them and compute the maximum team skill.

        Args:
            candidates: List of Candidate objects.
            n: Number of candidates.
            m: Number of programmers to select.

        Returns:
            List of maximum team skills for each exclusion.
        """
        # Precompute the sorted diff list for the full set
        diff_list = [
            (cand.prog_skill - cand.test_skill, cand.idx, cand.prog_skill, cand.test_skill)
            for cand in candidates
        ]
        diff_list.sort(reverse=True)

        # Precompute prefix sums for programming and testing skills
        sorted_by_diff = [cand for _, _, _, cand in diff_list]
        prog_skills_sorted = []
        test_skills_sorted = []
        idx_to_pos = {}
        for pos, (_, idx, prog, test) in enumerate(diff_list):
            prog_skills_sorted.append(prog)
            test_skills_sorted.append(test)
            idx_to_pos[idx] = pos

        # For each exclusion, efficiently recalculate the assignment
        result: List[int] = [0] * n
        for exclude_idx in range(n):
            # Remove the excluded candidate from diff_list
            # Find their position
            pos = idx_to_pos[exclude_idx]
            # Build new diff_list without the excluded candidate
            new_diff_list = diff_list[:pos] + diff_list[pos + 1 :]
            # Assign roles
            assignment, total_skill = self._assign_roles_for_exclusion(
                new_diff_list, n - 1, m
            )
            result[exclude_idx] = total_skill
        return result

    def _assign_roles_for_exclusion(
        self, diff_list: List[Tuple[int, int, int, int]], n: int, m: int
    ) -> Tuple[List[int], int]:
        """
        Assign roles for the exclusion case.

        Args:
            diff_list: List of (diff, idx, prog, test) for n candidates.
            n: Number of candidates (after exclusion).
            m: Number of programmers to select.

        Returns:
            Tuple of (assignment list, total team skill).
        """
        assignment = [0] * n  # Not used, but kept for interface compatibility
        total_skill = 0

        # Assign top m as programmers
        for i in range(m):
            _, _, prog, _ = diff_list[i]
            total_skill += prog

        # Assign rest as testers
        for i in range(m, n):
            _, _, _, test = diff_list[i]
            total_skill += test

        return assignment, total_skill


class InputParser:
    """Handles input parsing."""

    @staticmethod
    def parse_input() -> Tuple[int, List[Tuple[int, int, List[int], List[int]]]]:
        """
        Parse input from stdin.

        Returns:
            Tuple of (number of test cases, list of test case tuples).
            Each test case tuple: (n, m, prog_skills, test_skills)
        """
        import sys

        input_lines = sys.stdin.read().splitlines()
        t = int(input_lines[0])
        test_cases = []
        idx = 1
        for _ in range(t):
            n_m = input_lines[idx].split()
            n = int(n_m[0])
            m = int(n_m[1])
            prog_skills = list(map(int, input_lines[idx + 1].split()))
            test_skills = list(map(int, input_lines[idx + 2].split()))
            test_cases.append((n, m, prog_skills, test_skills))
            idx += 3
        return t, test_cases


class OutputFormatter:
    """Handles output formatting."""

    @staticmethod
    def format_output(results: List[List[int]]) -> None:
        """
        Print the results in the required format.

        Args:
            results: List of result lists, one per test case.
        """
        for res in results:
            print(" ".join(map(str, res)))


def main() -> None:
    """Main entry point."""
    parser = InputParser()
    t, test_cases = parser.parse_input()
    simulator = TeamSkillSimulator()
    all_results: List[List[int]] = []
    for n, m, prog_skills, test_skills in test_cases:
        result = simulator.simulate(n, m, prog_skills, test_skills)
        all_results.append(result)
    OutputFormatter.format_output(all_results)


if __name__ == "__main__":
    main()
