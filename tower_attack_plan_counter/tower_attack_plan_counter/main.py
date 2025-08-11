## main.py

"""
Main entry point for the Minimal-Length Attack Plan Solver system.

This script initializes and runs the Streamlit-based UI for user interaction.
It imports the UI class from ui.py and calls its run() method.

Dependencies:
    - ui.py (UI class)
    - streamlit (for web UI)
"""

from ui import UI

def main() -> None:
    """Main function to launch the UI."""
    ui = UI()
    ui.run()

if __name__ == "__main__":
    main()
