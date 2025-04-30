"""Widget for displaying project information."""
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel
)
from src.data.models import Project
from typing import Any, Optional

class ProjectInfoWidget(QWidget):
    """Widget displaying basic project information."""

    def __init__(self, parent=None):
        """Initialize the widget."""
        super().__init__(parent)
        self.current_project: Optional[Project] = None
        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        # Header
        header = QLabel("Projektinformationen")
        header.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(header)

        # Project details
        self.name_label = QLabel()
        self.created_label = QLabel()
        self.modified_label = QLabel()

        layout.addWidget(self.name_label)
        layout.addWidget(self.created_label)
        layout.addWidget(self.modified_label)

        # Set initial text
        self.clear_info()

    def clear_info(self):
        """Clear all project information."""
        self.name_label.setText("Name: -")
        self.created_label.setText("Erstellt: -")
        self.modified_label.setText("Geändert: -")

    def update_project(self, project: Project | None):
        """Update the displayed project information.

        Args:
            project: Project object containing the information to display
        """
        # Handle None projects
        if project is None:
            self.clear_info()
            return

        # Store reference to the current project
        if self.current_project is not project:
            # Unregister from previous project if exists
            if self.current_project is not None:
                self.current_project.remove_observer(self)

            # Register as observer of the new project
            self.current_project = project
            project.add_observer(self)

        # Update UI with project data
        self.name_label.setText(f"Name: {project.name}")
        self.created_label.setText(
            f"Erstellt: {project.created.strftime('%d.%m.%Y %H:%M')}"
        )
        self.modified_label.setText(
            f"Geändert: {project.modified.strftime('%d.%m.%Y %H:%M')}"
        )

    def on_subject_change(self, subject: Any, **kwargs: Any) -> None:
        """Handle updates from observed projects.

        Implements the Observer protocol method that gets called when the observed
        Project changes.

        Args:
            subject: The subject that was changed (Project in this case)
            kwargs: Additional data about the change
        """
        if subject is self.current_project and self.current_project is not None:
            event = kwargs.get('event', '')

            # Handle different event types differently for efficiency
            if event == 'renamed':
                # Just update the name if only the name changed
                self.name_label.setText(f"Name: {self.current_project.name}")
            else:
                # For other events or if no specific event, update all fields
                self.update_project(self.current_project)