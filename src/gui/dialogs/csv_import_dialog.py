"""CSV import dialog for DataInspect application."""
from typing import Optional, Dict, Any
from pathlib import Path
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QCheckBox, QSpinBox, QTableWidget, QTableWidgetItem, QGroupBox,
    QFormLayout, QDialogButtonBox, QLineEdit, QGridLayout, QTabWidget,
    QWidget
)
from PyQt6.QtCore import Qt

import pandas as pd

from ...data.importers.csv_importer import CSVImporter

class CSVImportDialog(QDialog):
    """Dialog for configuring CSV import options."""

    def __init__(self, file_path: Path, parent=None) -> None:
        """Initialize the dialog.

        Args:
            file_path: Path to the CSV file to import
            parent: Parent widget
        """
        super().__init__(parent)
        self.file_path = file_path
        self.preview_df: Optional[pd.DataFrame] = None

        # Default import options
        self.import_options = {
            'name': file_path.stem,  # Default name is the file name without extension
            'delimiter': ',',
            'encoding': 'utf-8',
            'has_header': True,
            'skip_rows': 0,
            'decimal': '.',
            'thousands': ','
        }

        # Try to detect delimiter
        try:
            self.import_options['delimiter'] = CSVImporter.detect_delimiter(file_path)
        except Exception:
            # Use default if detection fails
            pass

        self.setup_ui()
        self.update_preview()

    def setup_ui(self) -> None:
        """Set up the user interface."""
        self.setWindowTitle("CSV-Datei importieren")
        self.setMinimumWidth(900)
        self.setMinimumHeight(650)

        layout = QVBoxLayout(self)

        # File info and name section
        info_layout = QHBoxLayout()

        # File info
        file_info = QLabel(f"Datei: {self.file_path.name}")
        file_info.setStyleSheet("font-weight: bold;")
        info_layout.addWidget(file_info)

        # Spacer
        info_layout.addStretch()

        # Data source name
        name_label = QLabel("Name der Datenquelle:")
        name_label.setStyleSheet("font-weight: bold;")
        info_layout.addWidget(name_label)

        self.name_edit = QLineEdit(str(self.import_options['name']))
        self.name_edit.setMinimumWidth(200)
        _ = self.name_edit.textChanged.connect(self.on_name_changed)
        info_layout.addWidget(self.name_edit)

        layout.addLayout(info_layout)

        # Tab Widget for the different import steps
        self.tab_widget = QTabWidget()

        # Tab 1: Importoptionen
        self.options_tab = QWidget()
        self.setup_options_tab()
        _ = self.tab_widget.addTab(self.options_tab, "Importoptionen")

        # Tab 2: Datenvorschau
        self.preview_tab = QWidget()
        self.setup_preview_tab()
        _ = self.tab_widget.addTab(self.preview_tab, "Datenvorschau")

        layout.addWidget(self.tab_widget)

        # Apply button (right-aligned, blue)
        apply_layout = QHBoxLayout()
        apply_layout.setContentsMargins(0, 5, 0, 5)
        apply_layout.addStretch()

        apply_button = QPushButton("Anwenden")
        apply_button.setStyleSheet("background-color: #0078D7; color: white;")
        apply_button.setFixedWidth(120)
        _ = apply_button.clicked.connect(self.update_preview)
        apply_layout.addWidget(apply_button)

        layout.addLayout(apply_layout)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        _ = button_box.accepted.connect(self.accept)
        _ = button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        # Signals for tab changes
        _ = self.tab_widget.currentChanged.connect(self.on_tab_changed)

    def setup_options_tab(self) -> None:
        """Set up the tab for import options."""
        options_layout = QVBoxLayout(self.options_tab)

        # Options group with 3 columns
        options_group = QGroupBox("Importoptionen")
        options_grid = QGridLayout(options_group)

        # Column 1: Basic options
        col1_group = QGroupBox("Grundlegende Optionen")
        col1_layout = QFormLayout(col1_group)
        # Set labels to be left-aligned
        col1_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        # Delimiter
        self.delimiter_combo = QComboBox()
        self.delimiter_combo.addItems([',', ';', '\\t', '|', ' '])
        self.delimiter_combo.setEditable(True)
        self.delimiter_combo.setCurrentText(str(self.import_options['delimiter']))
        _ = self.delimiter_combo.currentTextChanged.connect(self.on_option_changed)
        col1_layout.addRow("Trennzeichen:", self.delimiter_combo)

        # Encoding
        self.encoding_combo = QComboBox()
        self.encoding_combo.addItems(['utf-8', 'latin1', 'iso-8859-1', 'cp1252'])
        self.encoding_combo.setEditable(True)
        self.encoding_combo.setCurrentText(str(self.import_options['encoding']))
        _ = self.encoding_combo.currentTextChanged.connect(self.on_option_changed)
        col1_layout.addRow("Zeichenkodierung:", self.encoding_combo)

        # Header
        self.header_check = QCheckBox()
        self.header_check.setChecked(bool(self.import_options['has_header']))
        _ = self.header_check.stateChanged.connect(self.on_option_changed)
        col1_layout.addRow("Kopfzeile vorhanden:", self.header_check)

        # Skip rows (moved from Advanced options)
        self.skip_rows_spin = QSpinBox()
        self.skip_rows_spin.setRange(0, 100)
        self.skip_rows_spin.setValue(int(self.import_options['skip_rows']))
        _ = self.skip_rows_spin.valueChanged.connect(self.on_option_changed)
        col1_layout.addRow("Zeilen überspringen:", self.skip_rows_spin)

        # Add explanation for header handling
        header_info = QLabel("Hinweis: Wenn keine Kopfzeile vorhanden ist, werden automatisch Spaltennamen im Format 'Spalte_X' generiert.")
        header_info.setWordWrap(True)
        col1_layout.addRow(header_info)

        options_grid.addWidget(col1_group, 0, 0)

        # Column 2: Number formatting
        col2_group = QGroupBox("Zahlenformatierung")
        col2_layout = QFormLayout(col2_group)
        # Set labels to be left-aligned
        col2_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        # Decimal separator
        self.decimal_combo = QComboBox()
        self.decimal_combo.addItems(['.', ','])
        self.decimal_combo.setCurrentText(str(self.import_options['decimal']))
        _ = self.decimal_combo.currentTextChanged.connect(self.on_option_changed)
        col2_layout.addRow("Dezimaltrennzeichen:", self.decimal_combo)

        # Thousands separator
        self.thousands_combo = QComboBox()
        self.thousands_combo.addItems([',', '.', ' ', ''])
        self.thousands_combo.setCurrentText(str(self.import_options['thousands']))
        _ = self.thousands_combo.currentTextChanged.connect(self.on_option_changed)
        col2_layout.addRow("Tausendertrennzeichen:", self.thousands_combo)

        # Add explanation for number formatting
        number_info = QLabel("Hinweis: Diese Einstellungen bestimmen, wie Zahlen in der CSV-Datei formatiert sind.")
        number_info.setWordWrap(True)
        col2_layout.addRow(number_info)

        options_grid.addWidget(col2_group, 0, 1)

        # Set column stretch factors
        options_grid.setColumnStretch(0, 1)
        options_grid.setColumnStretch(1, 1)

        options_layout.addWidget(options_group)

        # No button here anymore, moved to main layout

    def setup_preview_tab(self) -> None:
        """Set up the tab for data preview."""
        preview_layout = QVBoxLayout(self.preview_tab)

        # Preview group
        preview_group = QGroupBox("Datenvorschau")
        preview_inner_layout = QVBoxLayout(preview_group)

        # Table widget for preview
        self.preview_table = QTableWidget()
        self.preview_table.setAlternatingRowColors(True)
        preview_inner_layout.addWidget(self.preview_table)

        preview_layout.addWidget(preview_group)

    def on_tab_changed(self, index: int) -> None:
        """Responds to changes of the active tab.

        Args:
            index: Index of the newly selected tab
        """
        # Update the preview when switching tabs
        if index == 1:  # Preview tab
            self.update_preview()

    def on_name_changed(self) -> None:
        """Handle changes to the data source name."""
        self.import_options['name'] = self.name_edit.text()

    def on_option_changed(self) -> None:
        """Handle changes to import options."""
        # Update import options
        self.import_options['delimiter'] = self.delimiter_combo.currentText()
        self.import_options['encoding'] = self.encoding_combo.currentText()
        self.import_options['has_header'] = self.header_check.isChecked()
        self.import_options['skip_rows'] = self.skip_rows_spin.value()
        self.import_options['decimal'] = self.decimal_combo.currentText()
        self.import_options['thousands'] = self.thousands_combo.currentText()

        # Special handling for tab character
        if self.import_options['delimiter'] == '\\t':
            self.import_options['delimiter'] = '\t'

    def update_preview(self) -> None:
        """Update the preview table with current options."""
        self.on_option_changed()  # Ensure options are up to date

        # Get preview data
        preview_df, error = CSVImporter.get_preview(
            self.file_path,
            delimiter=str(self.import_options['delimiter']),
            encoding=str(self.import_options['encoding']),
            has_header=bool(self.import_options['has_header']),
            skip_rows=int(self.import_options['skip_rows'])
        )

        if error:
            # Show error in preview table
            self.preview_table.setRowCount(1)
            self.preview_table.setColumnCount(1)
            self.preview_table.setItem(0, 0, QTableWidgetItem(error))
            return

        self.preview_df = preview_df

        if preview_df is None:
            return

        # Update preview table
        self.preview_table.setRowCount(len(preview_df))
        self.preview_table.setColumnCount(len(preview_df.columns))

        # Set headers
        self.preview_table.setHorizontalHeaderLabels(preview_df.columns)

        # Fill data
        for row in range(len(preview_df)):
            for col in range(len(preview_df.columns)):
                value = preview_df.iloc[row, col]
                self.preview_table.setItem(row, col, QTableWidgetItem(str(value)))

        # Resize columns to content
        self.preview_table.resizeColumnsToContents()

    def get_import_options(self) -> Dict[str, Any]:
        """Get the current import options.

        Returns:
            Dictionary of import options
        """
        # Make sure the options are up to date
        self.on_option_changed()
        return self.import_options