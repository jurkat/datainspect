"""
DataInspect - Data Visualization Application

Main entry point for the data visualization application. Starts the GUI and
initializes the components.
"""

import sys
from PyQt6.QtWidgets import QApplication
from src.gui.main_window import MainWindow


def main():
    """Main function to start the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
