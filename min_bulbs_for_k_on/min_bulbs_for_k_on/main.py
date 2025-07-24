## main.py

from typing import Optional



class BulbSolver:
    """Solver for the bulb flipping problem.

    Provides a method to compute the smallest n such that after the flipping process,
    exactly k bulbs remain ON.
    """

    @staticmethod
    def get_min_n_for_k(k: int) -> int:
        """Returns the smallest n such that after the flipping process, exactly k bulbs remain ON.

        The mathematical insight is that after the process, bulbs at perfect square positions
        remain ON. Thus, the number of bulbs ON is floor(sqrt(n)). To have exactly k bulbs ON,
        the smallest such n is k * k.

        Args:
            k: The desired number of bulbs that remain ON after the process.

        Returns:
            The smallest integer n such that exactly k bulbs remain ON.
        """
        if k < 0:
            raise ValueError("k must be a non-negative integer.")
        return k * k


class CLI:
    """Command-line interface for the bulb flipping problem.

    Handles user interaction, input validation, and delegates computation to BulbSolver.
    """

    def __init__(self) -> None:
        """Initializes the CLI with a BulbSolver instance."""
        self._solver = BulbSolver()

    def run(self) -> None:
        """Runs the command-line interface loop.

        Prompts the user for the number of test cases and for each test case,
        reads the value of k, computes the result, and prints it.
        """
        print("Bulb Flipping Problem Solver")
        print("For each test case, enter the desired number of bulbs ON (k).")
        print("The program will output the smallest n such that after the flipping process, exactly k bulbs remain ON.\n")

        t: Optional[int] = None
        while t is None:
            try:
                t_input = input("Enter the number of test cases (t): ").strip()
                t = int(t_input)
                if t < 1:
                    print("Number of test cases must be at least 1.")
                    t = None
            except ValueError:
                print("Invalid input. Please enter a positive integer for the number of test cases.")

        for case_num in range(1, t + 1):
            k: Optional[int] = None
            while k is None:
                try:
                    k_input = input(f"Test case {case_num}: Enter k (number of bulbs ON): ").strip()
                    k = int(k_input)
                    if k < 0:
                        print("k must be a non-negative integer.")
                        k = None
                except ValueError:
                    print("Invalid input. Please enter a non-negative integer for k.")

            n = self._solver.get_min_n_for_k(k)
            print(f"Result for test case {case_num}: The smallest n is {n}.\n")


if __name__ == "__main__":
    cli = CLI()
    cli.run()
