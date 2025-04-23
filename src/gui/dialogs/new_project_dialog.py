"""Dialog for creating a new project."""
from typing import Final
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QDialogButtonBox,
    QWidget
)

class NewProjectDialog(QDialog):
    """Dialog for creating a new project."""
    
    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the dialog.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setWindowTitle("Neues Projekt")
        self.setModal(True)
        
        # Create layout
        layout: Final[QVBoxLayout] = QVBoxLayout(self)
        
        # Create form layout
        form_layout: Final[QFormLayout] = QFormLayout()
        
        # Add project name field
        self.name_edit: Final[QLineEdit] = QLineEdit()
        form_layout.addRow("Projektname:", self.name_edit)
        
        layout.addLayout(form_layout)
        
        # Add buttons
        button_box: Final[QDialogButtonBox] = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def get_project_name(self) -> str:
        """Return the entered project name.
        
        Returns:
            The project name as string
        """
        return self.name_edit.text().strip()
