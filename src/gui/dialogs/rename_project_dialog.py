"""Dialog for renaming a project."""
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)


class RenameProjectDialog(QDialog):
    """Dialog for renaming a project."""

    def __init__(self, current_name: str, parent=None) -> None:
        """Initialize the dialog.

        Args:
            current_name: Current name of the project
            parent: Parent widget
        """
        super().__init__(parent)
        self.setWindowTitle("Projekt umbenennen")
        self.setModal(True)
        self.current_name = current_name
        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)

        # Add description label
        description = QLabel("Geben Sie einen neuen Namen für das Projekt ein:")
        layout.addWidget(description)

        # Add name input
        self.name_input = QLineEdit(self.current_name)
        self.name_input.selectAll()
        layout.addWidget(self.name_input)

        # Add buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        _ = ok_button.clicked.connect(self.validate_and_accept)
        cancel_button = QPushButton("Abbrechen")
        _ = cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        # Set minimum size
        self.setMinimumWidth(300)

    def validate_and_accept(self) -> None:
        """Validate the input and accept the dialog."""
        new_name = self.name_input.text().strip()
        
        if not new_name:
            _ = QMessageBox.warning(
                self,
                "Ungültiger Name",
                "Der Projektname darf nicht leer sein."
            )
            return
            
        if new_name == self.current_name:
            _ = QMessageBox.information(
                self,
                "Keine Änderung",
                "Der neue Name entspricht dem aktuellen Namen."
            )
            self.reject()
            return
            
        self.accept()

    def get_new_name(self) -> str:
        """Get the new project name.

        Returns:
            str: The new project name
        """
        return self.name_input.text().strip()