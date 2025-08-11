## fenwick_tree.py
from typing import List

class FenwickTree:
    """
    Fenwick Tree (Binary Indexed Tree) implementation for modular arithmetic.
    Provides efficient methods for updating and querying prefix sums.
    """
    def __init__(self, size: int, modulus: int) -> None:
        """
        Initializes the Fenwick Tree with a given size and modulus.

        Args:
            size (int): The size of the Fenwick Tree.
            modulus (int): The modulus for modular arithmetic.
        """
        self.modulus = modulus
        self.tree = [0] * (size + 1)  # Fenwick Tree is 1-indexed

    def lowbit(self, x: int) -> int:
        """
        Returns the lowest bit of x.

        Args:
            x (int): The input integer.

        Returns:
            int: The lowest bit of x.
        """
        return x & -x

    def update(self, index: int, value: int) -> None:
        """
        Updates the Fenwick Tree at a specific index with a given value.

        Args:
            index (int): The index to update (1-indexed).
            value (int): The value to add (modulus applied).
        """
        while index < len(self.tree):
            self.tree[index] = (self.tree[index] + value) % self.modulus
            index += self.lowbit(index)

    def query(self, index: int) -> int:
        """
        Queries the prefix sum up to a specific index.

        Args:
            index (int): The index to query (1-indexed).

        Returns:
            int: The prefix sum modulo the modulus.
        """
        result = 0
        while index > 0:
            result = (result + self.tree[index]) % self.modulus
            index -= self.lowbit(index)
        return result

    def build(self, array: List[int]) -> None:
        """
        Builds the Fenwick Tree from an input array.

        Args:
            array (List[int]): The input array (0-indexed).
        """
        for i, value in enumerate(array, start=1):  # Convert to 1-indexed
            self.update(i, value)
## main.py
from typing import List

class FenwickTreeSolver:
    """
    Solver class that utilizes FenwickTree for modular arithmetic operations
    and efficient array transformations.
    """
    def __init__(self, modulus: int = 1000000007) -> None:
        """
        Initializes the solver with a given modulus.

        Args:
            modulus (int): The modulus for modular arithmetic. Default is 1000000007.
        """
        self.modulus = modulus

    def compute_a(self, b: List[int], k: int) -> List[int]:
        """
        Computes the transformed array 'a' based on input array 'b' and integer 'k'.

        Args:
            b (List[int]): The input array.
            k (int): The number of transformations to apply.

        Returns:
            List[int]: The transformed array 'a'.
        """
        # Initialize Fenwick Tree
        fenwick_tree = FenwickTree(len(b), self.modulus)
        fenwick_tree.build(b)

        # Apply transformations iteratively
        for _ in range(k):
            b = self.apply_f(b, fenwick_tree)

        return b

    def apply_f(self, array: List[int], fenwick_tree: FenwickTree) -> List[int]:
        """
        Applies a single transformation to the array using Fenwick Tree.

        Args:
            array (List[int]): The input array.
            fenwick_tree (FenwickTree): The Fenwick Tree instance.

        Returns:
            List[int]: The transformed array.
        """
        transformed = []
        for i in range(1, len(array) + 1):  # 1-indexed for Fenwick Tree
            prefix_sum = fenwick_tree.query(i)
            transformed.append(prefix_sum)
        return transformed

    def apply_fk(self, array: List[int], k: int) -> List[int]:
        """
        Applies 'k' transformations to the array using Fenwick Tree.

        Args:
            array (List[int]): The input array.
            k (int): The number of transformations to apply.

        Returns:
            List[int]: The transformed array after 'k' transformations.
        """
        fenwick_tree = FenwickTree(len(array), self.modulus)
        fenwick_tree.build(array)

        for _ in range(k):
            array = self.apply_f(array, fenwick_tree)

        return array


class Main:
    """
    Main class to manage program execution.
    """
    def __init__(self) -> None:
        """
        Initializes the Main class with a FenwickTreeSolver instance.
        """
        self.solver = FenwickTreeSolver()

    def main(self) -> None:
        """
        Main method to execute the program logic.
        """
        # Example input
        b = [1, 2, 3, 4, 5]
        k = 2

        # Compute transformed array 'a'
        a = self.solver.compute_a(b, k)

        # Print results
        print("Transformed array:", a)


# Entry point for the program
if __name__ == "__main__":
    main_instance = Main()
    main_instance.main()
