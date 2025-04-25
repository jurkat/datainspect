"""Central application configuration."""
from pathlib import Path
from typing import Final, List

# Application data directory (for logs, config, etc.)
APP_DIR: Final[Path] = Path.home() / ".datainspect"
APP_DIR.mkdir(parents=True, exist_ok=True)

# UI settings
WINDOW_MIN_WIDTH: Final[int] = 800
WINDOW_MIN_HEIGHT: Final[int] = 600
WINDOW_DEFAULT_WIDTH: Final[int] = 640  # Width for start screen
WINDOW_DEFAULT_HEIGHT: Final[int] = 400  # Height for start screen
WINDOW_PROJECT_WIDTH: Final[int] = 1280  # Width when project is open
WINDOW_TITLE: Final[str] = "DataInspect"
LEFT_PANEL_WIDTH: Final[int] = 280

# Data import settings
SUPPORTED_FORMATS: Final[List[str]] = ['.csv', '.xlsx', '.json']
MAX_FILE_SIZE: Final[int] = 100 * 1024 * 1024  # 100 MB

# Project file settings
PROJECT_FILE_EXTENSION: Final[str] = '.dinsp'

