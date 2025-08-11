## main.py

from typing import List, Tuple, Any
from tree_query import Tree, QueryProcessor
from utils import InputParser, OutputFormatter

def main() -> None:
    """Entry point for the tree query system.

    Parses input, processes queries for each tree, and outputs results.
    """
    # Parse input using InputParser
    trees_data: List[Tuple[int, List[Tuple[int, int]]]]
    all_queries: List[List[Tuple[int, int]]]
    trees_data, all_queries = InputParser.parse_input()

    all_results: List[List[int]] = []

    # For each test case (tree)
    for case_idx, ((n, edge_list), queries) in enumerate(zip(trees_data, all_queries)):
        # Build the tree
        tree = Tree(n)
        for u, v in edge_list:
            tree.add_edge(u, v)
        tree.preprocess()

        # Process queries
        query_processor = QueryProcessor(tree)
        case_results = query_processor.process_queries(queries)
        all_results.append(case_results)

    # Output results
    OutputFormatter.format_output(all_results)

if __name__ == "__main__":
    main()
