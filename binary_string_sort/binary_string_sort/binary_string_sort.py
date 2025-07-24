## binary_string_sort.py


class BinaryStringSort:
    def __init__(self, test_cases: list[str]) -> None:
        self.test_cases = test_cases

    def min_cuts(self, s: str) -> int:
        # This function calculates the minimum number of cuts needed to rearrange
        # the binary string into a sorted binary string using a greedy algorithm.
        count_0 = s.count('0')
        count_1 = len(s) - count_0
        min_cuts = min(count_0, count_1)
        return min_cuts

    def process_test_cases(self) -> list[int]:
        # This function processes all test cases and returns a list of minimum cuts
        results = []
        for s in self.test_cases:
            results.append(self.min_cuts(s))
        return results

if __name__ == "__main__":
    # Example test cases
    test_cases = ["1100", "0011", "010101", "111000"]
    binary_string_sort = BinaryStringSort(test_cases)
    results = binary_string_sort.process_test_cases()
    for result in results:
        print(result)
