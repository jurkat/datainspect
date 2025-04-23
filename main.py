"""
DataInspect - Data Visualization Application

Main entry point for the data visualization application. Starts the GUI and
initializes the components.
"""

import os
import sys
import logging
from PyQt6.QtWidgets import QApplication
from src.gui.main_window import MainWindow
from src.utils.logging import setup_logging
from src.config import APP_DIR

def main():
    """Main function to start the application."""
    debug_mode = os.environ.get("DATAINSPECT_DEBUG", "0") in ("1", "true", "True")
    
    # Initialize logging
    setup_logging(debug_mode)
    logger = logging.getLogger(__name__)
    
    try:
        # Ensure application directory exists
        APP_DIR.mkdir(parents=True, exist_ok=True)
        
        # Start GUI application
        logger.info("Starting GUI application...")
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        
        logger.info("Application ready")
        sys.exit(app.exec())
        
    except Exception as e:
        logger.exception("Unhandled exception occurred")
        sys.exit(1)

if __name__ == "__main__":
    main()
