## beautiful_triples.py

from typing import List, Tuple

class BeautifulTriples:
    """
    A class to calculate the number of beautiful pairs of triples from given test cases.
    """

    def __init__(self, test_cases: List[Tuple[int, List[int]]]) -> None:
        """
        Initializes the BeautifulTriples class with test cases.

        Args:
            test_cases (List[Tuple[int, List[int]]]): A list of test cases, where each test case is a tuple
                                                      containing an integer and a list of integers.
        """
        self.test_cases = test_cases

    def find_beautiful_pairs(self) -> List[int]:
        """
        Finds the number of beautiful pairs for each test case.

        Returns:
            List[int]: A list of integers representing the count of beautiful pairs for each test case.
        """
        results = []
        for _, array in self.test_cases:
            count = self._count_beautiful_pairs(array)
            results.append(count)
        return results

    def _count_beautiful_pairs(self, array: List[int]) -> int:
        """
        Counts the number of beautiful pairs directly without generating all triples.

        Args:
            array (List[int]): A list of integers.

        Returns:
            int: The count of beautiful pairs.
        """
        count = 0
        n = len(array)
        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                k = j + (array[j] - array[i])  # Calculate k directly based on the condition
                if k < n and array[k] - array[j] == array[j] - array[i]:
                    count += 1
        return count
