## main.py

import sys
from road_leveling import RoadLevelingSystem


def main() -> None:
    """Main entry point for the road leveling CLI application.

    Reads input from stdin, processes the test cases, and outputs results.
    """
    input_data: str = sys.stdin.read()
    system: RoadLevelingSystem = RoadLevelingSystem()
    system.load_input(input_data)
    results = system.process()
    system.output(results)


if __name__ == "__main__":
    main()
