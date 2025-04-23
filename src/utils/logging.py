"""Logging configuration for the application."""
import logging
import sys
from pathlib import Path
from typing import Final
from ..config import APP_DIR

# Constants
LOG_FORMAT: Final[str] = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT: Final[str] = '%Y-%m-%d %H:%M:%S'
LOG_FILE: Final[Path] = APP_DIR / 'logs' / 'datainspect.log'

def setup_logging(debug_mode: bool = False) -> None:
    """
    Set up logging configuration.
    
    Args:
        debug_mode: If True, set log level to DEBUG, otherwise INFO
    """
    # Create logs directory if it doesn't exist
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT))
    root_logger.addHandler(console_handler)
    
    # File handler
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT))
    root_logger.addHandler(file_handler)
    
    # Log startup information
    root_logger.info("DataInspect starting up")
    root_logger.info(f"Log file: {LOG_FILE}")
    root_logger.info(f"Debug mode: {debug_mode}")
