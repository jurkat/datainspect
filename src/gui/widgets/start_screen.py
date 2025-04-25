"""StartScreen widget for DataInspect application."""
from typing import Callable
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton
)
from .drop_zone import ProjectDropZone

class StartScreen(QWidget):
    """Start screen widget shown when no project is open."""

    def __init__(
        self,
        on_new_project: Callable[[], None],
        on_open_project: Callable[[], None],
        on_file_dropped: Callable[[str], None]
    ) -> None:
        super().__init__()
        self.on_new_project = on_new_project
        self.on_open_project = on_open_project

        # Set widget style
        self.setStyleSheet("""
            QLabel {
                color: #666;
            }
        """)

        self.setup_ui(on_file_dropped)

    def setup_ui(self, on_file_dropped: Callable[[str], None]) -> None:
        """Set up the user interface."""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Create drop zone
        drop_zone = ProjectDropZone(on_file_dropped)
        layout.addWidget(drop_zone)

        # Create buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # Create and style buttons
        new_button = QPushButton("Neues Projekt")
        _ = new_button.clicked.connect(self.on_new_project)
        new_button.setFixedHeight(40)
        new_button.setStyleSheet("""
            QPushButton {
                background-color: #2c2c2c;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #3c3c3c;
            }
            QPushButton:pressed {
                background-color: #1c1c1c;
            }
        """)

        open_button = QPushButton("Projekt öffnen")
        _ = open_button.clicked.connect(self.on_open_project)
        open_button.setFixedHeight(40)
        open_button.setStyleSheet("""
            QPushButton {
                background-color: #2c2c2c;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #3c3c3c;
            }
            QPushButton:pressed {
                background-color: #1c1c1c;
            }
        """)

        button_layout.addWidget(new_button, 1)  # Stretch factor 1
        button_layout.addWidget(open_button, 1)  # Stretch factor 1

        layout.addLayout(button_layout)

        # Set the background color for the entire widget
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
            }
        """)
