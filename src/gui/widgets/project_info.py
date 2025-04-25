"""ProjectInfo widget for DataInspect application.

This widget displays information about the currently open project.
It shows the project name, creation date, and last modified date.
"""
from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QLabel, 
    QGridLayout
)

from ...data.models import Project


class ProjectInfoWidget(QWidget):
    """Widget displaying information about the current project."""
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Initialize the project info widget."""
        super().__init__(parent)
        self.title_label = QLabel()
        self.created_label = QLabel()
        self.modified_label = QLabel()
        self.setup_ui()
    
    def setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        
        # Title
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.title_label)
        
        # Info grid
        info_layout = QGridLayout()
        info_layout.addWidget(QLabel("Erstellt:"), 0, 0)
        info_layout.addWidget(self.created_label, 0, 1)
        info_layout.addWidget(QLabel("Zuletzt geändert:"), 1, 0)
        info_layout.addWidget(self.modified_label, 1, 1)
        layout.addLayout(info_layout)
        
        layout.addStretch()
    
    def update_project(self, project: Project) -> None:
        """Update the displayed project information."""
        self.title_label.setText(project.name)
        self.created_label.setText(project.created.strftime("%d.%m.%Y %H:%M"))
        self.modified_label.setText(project.modified.strftime("%d.%m.%Y %H:%M"))
