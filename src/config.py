"""Central application configuration."""
from pathlib import Path
from typing import Final, List, Dict, Any

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
RIGHT_PANEL_WIDTH: Final[int] = 300  # Width for properties panel

# UI colors
UI_COLORS: Final[Dict[str, str]] = {
    # Base colors
    'background': '#1e1e1e',
    'background_light': '#252525',
    'background_lighter': '#2d2d2d',
    'foreground': '#e0e0e0',
    'foreground_dim': '#aaaaaa',
    'border': '#444444',
    'border_light': '#555555',

    # Accent colors
    'accent_primary': '#4a86e8',
    'accent_secondary': '#6aa84f',
    'accent_tertiary': '#e69138',

    # UI element colors
    'header_bg': '#3d3d3d',
    'table_alternate_row': '#3a3a3a',
    'button_bg': '#3d3d3d',
    'button_hover': '#4d4d4d',
    'button_pressed': '#2a2a2a',
    'tab_active': '#4a86e8',
    'tab_inactive': '#3d3d3d',
    'selection': '#3a3a3a',
}

# Data import settings
SUPPORTED_FORMATS: Final[List[str]] = ['.csv', '.xlsx', '.json']
MAX_FILE_SIZE: Final[int] = 100 * 1024 * 1024  # 100 MB

# Project file settings
PROJECT_FILE_EXTENSION: Final[str] = '.dinsp'

# Visualization types
VISUALIZATION_TYPES: Final[Dict[str, Dict[str, Any]]] = {
    'bar': {
        'name': 'Balkendiagramm',
        'icon': '📊',
        'description': 'Vergleicht Werte über verschiedene Kategorien',
        'supports_multiple_y': True
    },
    'line': {
        'name': 'Liniendiagramm',
        'icon': '📈',
        'description': 'Zeigt Trends über einen Zeitraum oder eine Sequenz',
        'supports_multiple_y': True
    },
    'pie': {
        'name': 'Kreisdiagramm',
        'icon': '🥧',
        'description': 'Zeigt Anteile am Gesamtwert',
        'supports_multiple_y': False
    },
    'scatter': {
        'name': 'Streudiagramm',
        'icon': '🔵',
        'description': 'Zeigt Beziehungen zwischen zwei Variablen',
        'supports_multiple_y': False
    },
    'heatmap': {
        'name': 'Heatmap',
        'icon': '🔥',
        'description': 'Visualisiert Daten als farbige Matrix',
        'supports_multiple_y': False
    }
}

# Visualization colors
VISUALIZATION_COLORS: Final[Dict[str, Dict[str, str]]] = {
    'Grau': {
        'hell': '#CCCCCC',
        'mittel': '#999999',
        'dunkel': '#666666'
    },
    'Blau': {
        'hell': '#A4C2F4',
        'mittel': '#6D9EEB',
        'dunkel': '#3D78D6'
    },
    'Rot': {
        'hell': '#F4CCCC',
        'mittel': '#EA9999',
        'dunkel': '#E06666'
    },
    'Grün': {
        'hell': '#D9EAD3',
        'mittel': '#B6D7A8',
        'dunkel': '#93C47D'
    },
    'Gelb': {
        'hell': '#FFF2CC',
        'mittel': '#FFE599',
        'dunkel': '#FFD966'
    },
    'Orange': {
        'hell': '#FCE5CD',
        'mittel': '#F9CB9C',
        'dunkel': '#F6B26B'
    },
    'Lila': {
        'hell': '#D9D2E9',
        'mittel': '#B4A7D6',
        'dunkel': '#8E7CC3'
    }
}

