"""Dialog windows for the application."""
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QDialogButtonBox
)

class NewProjectDialog(QDialog):
    """Dialog for creating a new project."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Neues Projekt")
        self.setup_ui()

    def setup_ui(self):
        """Setup the dialog UI."""
        layout = QVBoxLayout()

        # Project name input
        layout.addWidget(QLabel("Projektname:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        _ = button_box.accepted.connect(self.accept)
        _ = button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_project_name(self) -> str:
        """Get the entered project name."""
        return self.name_input.text().strip()

class RenameProjectDialog(QDialog):
    """Dialog for renaming a project."""
    def __init__(self, old_name: str, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Projekt umbenennen")
        self.setModal(True)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Neuer Name für das Projekt '{old_name}':"))
        self.name_input = QLineEdit()
        self.name_input.setText(old_name)
        layout.addWidget(self.name_input)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        _ = button_box.accepted.connect(self.accept)
        _ = button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        self.setLayout(layout)
    def get_new_name(self) -> str:
        return self.name_input.text().strip()

class ConfirmDeleteDialog(QDialog):
    """Dialog to confirm project deletion."""
    def __init__(self, project_name: str, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Projekt löschen")
        self.setModal(True)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Möchten Sie das Projekt '{project_name}' wirklich löschen? Diese Aktion kann nicht rückgängig gemacht werden."))
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        _ = button_box.accepted.connect(self.accept)
        _ = button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        self.setLayout(layout)
