## main.py
import argparse
from ordered_pairs_calculator import OrderedPairsCalculator

def parse_arguments():
    """
    Parse command-line arguments for the program.

    Returns:
        argparse.Namespace: Parsed arguments containing n and m.
    """
    parser = argparse.ArgumentParser(
        description="Calculate the number of valid ordered pairs (a, b) such that gcd(a, b) == 1."
    )
    parser.add_argument(
        "--n",
        type=int,
        default=10,
        help="Upper limit for the first element of the pair (default: 10)."
    )
    parser.add_argument(
        "--m",
        type=int,
        default=10,
        help="Upper limit for the second element of the pair (default: 10)."
    )
    return parser.parse_args()

def main():
    """
    Main function to initialize OrderedPairsCalculator and display results.
    """
    # Parse command-line arguments
    args = parse_arguments()
    n = args.n
    m = args.m

    try:
        # Initialize OrderedPairsCalculator
        calculator = OrderedPairsCalculator(n, m)

        # Calculate valid ordered pairs
        valid_pairs_count = calculator.calculate_valid_pairs()

        # Display results
        print(f"The number of valid ordered pairs (a, b) for n={n} and m={m} is: {valid_pairs_count}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
