"""Styles for the DataInspect application.

This module provides consistent styling for the application's UI components.
"""
from src.config import UI_COLORS

# Base styles for the entire application
BASE_STYLE = f"""
QWidget {{
    background-color: {UI_COLORS['background']};
    color: {UI_COLORS['foreground']};
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}}

QLabel {{
    color: {UI_COLORS['foreground']};
    background-color: transparent;
    border: none;
    padding: 0px;
    margin: 0px;
}}

QLabel[title="true"] {{
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 4px;
}}

QLabel[subtitle="true"] {{
    font-size: 14px;
    font-weight: bold;
    margin-top: 4px;
    margin-bottom: 2px;
}}

QLabel[dimmed="true"] {{
    color: {UI_COLORS['foreground_dim']};
}}

QPushButton {{
    background-color: {UI_COLORS['button_bg']};
    color: {UI_COLORS['foreground']};
    border: none;
    border-radius: 2px;
    padding: 2px 4px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: {UI_COLORS['button_hover']};
    border-color: {UI_COLORS['border_light']};
}}

QPushButton:pressed {{
    background-color: {UI_COLORS['button_pressed']};
}}

QPushButton[accent="primary"] {{
    background-color: {UI_COLORS['accent_primary']};
    border-color: {UI_COLORS['accent_primary']};
}}

QPushButton[accent="primary"]:hover {{
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {UI_COLORS['accent_primary']}, stop:1 #3a76d8);
}}

QPushButton[accent="secondary"] {{
    background-color: {UI_COLORS['accent_secondary']};
    border-color: {UI_COLORS['accent_secondary']};
}}

QPushButton[accent="tertiary"] {{
    background-color: {UI_COLORS['accent_tertiary']};
    border-color: {UI_COLORS['accent_tertiary']};
}}

QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
    background-color: {UI_COLORS['background_lighter']};
    color: {UI_COLORS['foreground']};
    border: 1px solid {UI_COLORS['border']};
    border-radius: 4px;
    padding: 4px;
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
    border-color: {UI_COLORS['accent_primary']};
}}

QComboBox::drop-down {{
    border: none;
    width: 20px;
}}

QComboBox::down-arrow {{
    image: url(:/icons/dropdown.png);
}}

QComboBox QAbstractItemView {{
    background-color: {UI_COLORS['background_lighter']};
    color: {UI_COLORS['foreground']};
    border: 1px solid {UI_COLORS['border']};
    selection-background-color: {UI_COLORS['accent_primary']};
}}

QGroupBox {{
    background-color: {UI_COLORS['background_lighter']};
    border: 1px solid {UI_COLORS['border']};
    border-radius: 4px;
    padding-top: 15px;
    margin-top: 10px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
    color: {UI_COLORS['foreground']};
}}

QTabWidget::pane {{
    border: 1px solid {UI_COLORS['border']};
    border-radius: 4px;
    background-color: {UI_COLORS['background_lighter']};
}}

QTabBar::tab {{
    background-color: {UI_COLORS['tab_inactive']};
    color: {UI_COLORS['foreground']};
    border: none;
    border-top-left-radius: 2px;
    border-top-right-radius: 2px;
    padding: 2px 6px;
    margin-right: 1px;
}}

QTabBar::tab:selected {{
    background-color: {UI_COLORS['tab_active']};
    border-bottom: none;
}}

QTabBar::tab:!selected {{
    margin-top: 2px;
}}

QTableWidget {{
    background-color: {UI_COLORS['background_lighter']};
    alternate-background-color: {UI_COLORS['table_alternate_row']};
    color: {UI_COLORS['foreground']};
    gridline-color: {UI_COLORS['border']};
    border: 1px solid {UI_COLORS['border']};
    border-radius: 4px;
}}

QHeaderView::section {{
    background-color: {UI_COLORS['header_bg']};
    color: {UI_COLORS['foreground']};
    padding: 4px;
    border: 1px solid {UI_COLORS['border']};
}}

QScrollBar:vertical {{
    background-color: {UI_COLORS['background']};
    width: 12px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background-color: {UI_COLORS['button_bg']};
    min-height: 20px;
    border-radius: 6px;
    margin: 2px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {UI_COLORS['button_hover']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background-color: {UI_COLORS['background']};
    height: 12px;
    margin: 0px;
}}

QScrollBar::handle:horizontal {{
    background-color: {UI_COLORS['button_bg']};
    min-width: 20px;
    border-radius: 6px;
    margin: 2px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {UI_COLORS['button_hover']};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

QSplitter::handle {{
    background-color: {UI_COLORS['border']};
}}

QSplitter::handle:horizontal {{
    width: 2px;
}}

QSplitter::handle:vertical {{
    height: 2px;
}}

QStatusBar {{
    background-color: {UI_COLORS['background_lighter']};
    color: {UI_COLORS['foreground']};
    border-top: 1px solid {UI_COLORS['border']};
}}

QToolBar {{
    background-color: {UI_COLORS['background_lighter']};
    border-bottom: 1px solid {UI_COLORS['border']};
    spacing: 2px;
}}

QToolButton {{
    background-color: transparent;
    border: none;
    border-radius: 2px;
    padding: 1px;
}}

QToolButton:hover {{
    background-color: {UI_COLORS['button_hover']};
    border-color: {UI_COLORS['border']};
}}

QToolButton:pressed {{
    background-color: {UI_COLORS['button_pressed']};
}}

QMenu {{
    background-color: {UI_COLORS['background_lighter']};
    color: {UI_COLORS['foreground']};
    border: 1px solid {UI_COLORS['border']};
}}

QMenu::item {{
    padding: 2px 8px 2px 8px;
}}

QMenu::item:selected {{
    background-color: {UI_COLORS['accent_primary']};
}}

QMenuBar {{
    background-color: {UI_COLORS['background_lighter']};
    color: {UI_COLORS['foreground']};
}}

QMenuBar::item {{
    padding: 2px 4px;
    background-color: transparent;
}}

QMenuBar::item:selected {{
    background-color: {UI_COLORS['button_hover']};
}}
"""

# Styles for specific widgets
DATA_SOURCE_ITEM_STYLE = f"""
QFrame {{
    background-color: {UI_COLORS['background_lighter']};
    border: none;
    border-radius: 2px;
    color: {UI_COLORS['foreground']};
    padding: 0px;
    margin: 1px 0px;
}}

QFrame:hover {{
    background-color: {UI_COLORS['background_light']};
}}

QFrame[selected="true"] {{
    background-color: {UI_COLORS['accent_primary']};
}}

QFrame[selected="true"]:hover {{
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {UI_COLORS['accent_primary']}, stop:1 #3a76d8);
}}

QFrame[selected="true"] QLabel {{
    color: white;
}}

QLabel {{
    color: {UI_COLORS['foreground']};
    background-color: transparent;
    border: none;
    padding: 0px;
}}

QLabel[styleSheet*="font-weight: bold"] {{
    color: {UI_COLORS['foreground']};
}}

QLabel[styleSheet*="color: #666"] {{
    color: {UI_COLORS['foreground_dim']};
}}
"""

DROP_ZONE_STYLE = f"""
QFrame {{
    background-color: {UI_COLORS['background_light']};
    border: 2px dashed {UI_COLORS['border']};
    border-radius: 8px;
    min-height: 80px;
}}

QFrame:hover {{
    border-color: {UI_COLORS['border_light']};
    background-color: {UI_COLORS['background_lighter']};
}}

QLabel {{
    color: {UI_COLORS['foreground_dim']};
    font-size: 13px;
    padding: 10px;
    white-space: pre-wrap;
    background-color: transparent;
}}
"""

START_SCREEN_STYLE = f"""
QWidget {{
    background-color: {UI_COLORS['background']};
}}

QLabel {{
    color: {UI_COLORS['foreground_dim']};
    background-color: transparent;
}}

QPushButton {{
    background-color: {UI_COLORS['button_bg']};
    color: {UI_COLORS['foreground']};
    border: none;
    border-radius: 4px;
    padding: 10px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: {UI_COLORS['button_hover']};
}}

QPushButton:pressed {{
    background-color: {UI_COLORS['button_pressed']};
}}
"""

# Function to get a consistent style for cards/panels
def get_card_style(accent_color=None):
    """Get a style for a card/panel widget.

    Args:
        accent_color: Optional accent color for the card

    Returns:
        str: CSS style for the card
    """
    accent_color if accent_color else UI_COLORS['border']

    return f"""
    QFrame {{
        background-color: {UI_COLORS['background_lighter']};
        border: none;
        border-radius: 2px;
        padding: 2px;
    }}

    QLabel {{
        background-color: transparent;
        border: none;
        padding: 0px;
        margin: 0px;
    }}

    QLabel[title="true"] {{
        font-size: 14px;
        font-weight: bold;
        color: {UI_COLORS['foreground']};
    }}
    """
