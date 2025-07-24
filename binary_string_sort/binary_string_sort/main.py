## main.py


from binary_string_sort import BinaryStringSort

def main() -> None:
    # Example test cases
    test_cases = ["1100", "0011", "010101", "111000"]
    
    # Create an instance of BinaryStringSort with the test cases
    binary_string_sort = BinaryStringSort(test_cases)
    
    # Process the test cases to get the minimum cuts required for each
    results = binary_string_sort.process_test_cases()
    
    # Print the results
    for result in results:
        print(result)

if __name__ == "__main__":
    main()
