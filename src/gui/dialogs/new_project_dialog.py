"""Dialog for creating a new project."""
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QDialogButtonBox,
    QMessageBox
)

class NewProjectDialog(QDialog):
    """Dialog for getting the name of a new project."""
    
    def __init__(self, parent=None):
        """Initialize the dialog."""
        super().__init__(parent)
        self.setWindowTitle("Neues Projekt")
        self.setModal(True)
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        
        # Project name input
        layout.addWidget(QLabel("Projektname:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Geben Sie einen Projektnamen ein")
        layout.addWidget(self.name_input)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        _ = button_box.accepted.connect(self.validate_and_accept)
        _ = button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        # Set minimum size
        self.setMinimumWidth(300)
        
    def validate_and_accept(self):
        """Validate the input before accepting."""
        name = self.name_input.text().strip()
        if not name:
            _ = QMessageBox.warning(
                self,
                "Ungültige Eingabe",
                "Bitte geben Sie einen Projektnamen ein."
            )
            return
        self.accept()
        
    def get_project_name(self) -> str:
        """Get the entered project name."""
        return self.name_input.text().strip()
