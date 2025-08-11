## main.py

from typing import List, Tuple
from beautiful_triples import BeautifulTriples

def main() -> None:
    """
    Main function to initialize BeautifulTriples and execute the program flow.
    """
    # Default test cases for demonstration purposes
    test_cases: List[Tuple[int, List[int]]] = [
        (5, [1, 2, 3, 4, 5]),
        (6, [1, 3, 5, 7, 9, 11]),
        (4, [1, 1, 1, 1])
    ]

    # Initialize BeautifulTriples with test cases
    beautiful_triples = BeautifulTriples(test_cases)

    # Find the number of beautiful pairs for each test case
    results: List[int] = beautiful_triples.find_beautiful_pairs()

    # Print the results
    print("Results for each test case:")
    for i, result in enumerate(results):
        print(f"Test case {i + 1}: {result}")

# Entry point for the program
if __name__ == "__main__":
    main()
