## main.py

import numpy as np
from algorithm import Algorithm

class Main:
    def main(self) -> None:
        """
        Main function to execute the program flow.
        """
        # Example input array
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        
        # Create an instance of Algorithm class
        algorithm = Algorithm()
        
        # Find the lexicographically smallest array
        smallest_array = algorithm.find_lexicographically_smallest_array(arr)
        
        # Print the result
        print("Lexicographically smallest array:", smallest_array)

if __name__ == "__main__":
    main_instance = Main()
    main_instance.main()
