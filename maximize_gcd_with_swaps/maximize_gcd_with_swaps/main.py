## main.py
import sys
from typing import List, Tuple
from gcd_optimizer import GCDOptimizer
from swap_cost_manager import SwapCostManager
from utils import Utils

class Main:
    """
    Main class orchestrating the program flow by interacting with GCDOptimizer, SwapCostManager, and Utils classes.
    """

    def __init__(self) -> None:
        self.gcd_optimizer = GCDOptimizer()
        self.swap_cost_manager = SwapCostManager()

    def main(self, input_file: str = "input.txt", output_file: str = "output.txt") -> None:
        """
        Main function to execute the program flow.

        Args:
            input_file (str): Path to the input file. Defaults to "input.txt".
            output_file (str): Path to the output file. Defaults to "output.txt".

        Returns:
            None
        """
        try:
            # Step 1: Read input data
            a, b, c, budgets, _ = Utils.read_input(input_file)

            # Step 2: Validate input data
            Utils.validate_input_data(a, b, c, budgets)

            # Step 3: Calculate swap costs
            swaps = self.swap_cost_manager.calculate_swap_costs(a, b, c)

            # Step 4: Process each budget and maximize GCD
            results = []
            for budget in budgets:
                # Filter swaps based on the current budget
                filtered_swaps = self.swap_cost_manager.filter_swaps_by_budget(swaps, budget)

                # Maximize GCD within the budget
                max_gcd = self.gcd_optimizer.maximize_gcd(a, b, filtered_swaps, budget)
                results.append(max_gcd)

            # Step 5: Write results to output file
            Utils.write_output(results, output_file)

        except Exception as e:
            # Log any errors encountered during execution
            Utils.log_message(f"Error in main execution: {e}", log_file="main.log")
            raise

if __name__ == "__main__":
    # Default input and output file paths
    input_file = "input.txt"
    output_file = "output.txt"

    # Check for command-line arguments
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    # Execute the main program
    main_program = Main()
    main_program.main(input_file=input_file, output_file=output_file)
