## main.py

from typing import Tuple, Dict, Any
from battle import BattleSimulator


class Main:
    """Handles user interaction, query parsing, and output display for the battle simulator."""

    def __init__(self) -> None:
        """Initializes the Main class with a BattleSimulator instance."""
        self.simulator: BattleSimulator = BattleSimulator()

    def run(self) -> None:
        """Runs the main loop, processing user queries and displaying results."""
        print("Battle Simulator Started.")
        print("Commands:")
        print("  1 <health>    - Add hero with given health")
        print("  2 <durability> - Add artifact with given durability")
        print("Type 'exit' to quit.\n")

        while True:
            try:
                query: str = input("Enter query: ").strip()
                if query.lower() == "exit":
                    print("Exiting Battle Simulator.")
                    break

                t_i, v_i = self._parse_query(query)
                if t_i == 1:
                    self.simulator.add_hero(v_i)
                elif t_i == 2:
                    self.simulator.add_artifact(v_i)
                else:
                    print("Invalid query type. Use 1 for hero, 2 for artifact.")
                    continue

                rounds: int = self.simulator.max_survivable_rounds()
                state: Dict[str, Any] = self.simulator.get_army_state()
                self._display_state(state, rounds)
            except ValueError as ve:
                print(f"Input error: {ve}")
            except Exception as e:
                print(f"Unexpected error: {e}")

    def _parse_query(self, query: str) -> Tuple[int, int]:
        """Parses a user query string into command type and value.

        Args:
            query (str): The input query string.

        Returns:
            tuple: (t_i, v_i) where t_i is the command type and v_i is the value.

        Raises:
            ValueError: If the query is not in the correct format.
        """
        parts = query.split()
        if len(parts) != 2:
            raise ValueError("Query must be in the format '<type> <value>'.")

        t_i: int = int(parts[0])
        v_i: int = int(parts[1])
        if t_i not in (1, 2):
            raise ValueError("Type must be 1 (hero) or 2 (artifact).")
        if v_i <= 0:
            raise ValueError("Value must be a positive integer.")
        return t_i, v_i

    def _display_state(self, state: Dict[str, Any], rounds: int) -> None:
        """Displays the current army state and survivable rounds.

        Args:
            state (dict): The current state of the army.
            rounds (int): The maximum number of survivable rounds.
        """
        print("\n--- Army State ---")
        print(f"Heroes ({len(state['heroes'])}): {state['heroes']}")
        print(f"Artifacts ({len(state['artifacts'])}): {state['artifacts']}")
        print(f"Max survivable rounds: {rounds}\n")


if __name__ == "__main__":
    main = Main()
    main.run()
