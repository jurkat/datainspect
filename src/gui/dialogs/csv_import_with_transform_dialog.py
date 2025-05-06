"""CSV import dialog with data transformation capabilities for DataInspect application."""
from typing import Optional, Dict, Any
from pathlib import Path
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QCheckBox, QSpinBox, QTableWidget, QTableWidgetItem, QGroupBox,
    QFormLayout, QDialogButtonBox, QLineEdit, QGridLayout, QWidget,
    QListWidget, QDoubleSpinBox, QMenu, QSplitter, QFrame, QHeaderView,
    QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QColor, QBrush

import pandas as pd

from ...data.importers.csv_importer import CSVImporter
from ...data.transformations.data_transformation import (
    TransformationOperation, DataTransformation,
    DataFrameTransformer
)

class CSVImportDialogWithTransformation(QDialog):
    """Dialog for configuring CSV import options with data transformation capabilities."""

    def __init__(self, file_path: Path, parent=None) -> None:
        """Initialize the dialog.

        Args:
            file_path: Path to the CSV file to import
            parent: Parent widget
        """
        super().__init__(parent)
        self.file_path = file_path
        self.preview_df: Optional[pd.DataFrame] = None
        self.transformed_df: Optional[pd.DataFrame] = None
        self.full_df: Optional[pd.DataFrame] = None  # Complete dataset for statistics
        self.missing_values_info: Dict[str, Dict[str, Any]] = {}  # Information about missing values per column

        # Transformer for data cleaning and conversion
        self.data_transformer = DataFrameTransformer()

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
        self.setMinimumWidth(1000)
        self.setMinimumHeight(700)

        main_layout = QVBoxLayout(self)

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

        main_layout.addLayout(info_layout)

        # Main content splitter (vertical)
        main_splitter = QSplitter(Qt.Orientation.Vertical)
        main_splitter.setChildrenCollapsible(False)

        # Top section: Import options and transformation list
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)

        # Create a horizontal splitter for options and transformation list
        options_transform_splitter = QSplitter(Qt.Orientation.Horizontal)
        options_transform_splitter.setChildrenCollapsible(False)

        # Import options (left side)
        options_widget = QWidget()
        self.setup_options_section(options_widget)
        options_transform_splitter.addWidget(options_widget)

        # Transformation list (right side)
        transform_widget = QWidget()
        self.setup_transformation_section(transform_widget)
        options_transform_splitter.addWidget(transform_widget)

        # Set the size proportions (2/3 for options, 1/3 for transformations)
        options_transform_splitter.setSizes([650, 350])

        top_layout.addWidget(options_transform_splitter)

        # Add the top widget to the main splitter
        main_splitter.addWidget(top_widget)

        # Add the Apply button between top and bottom widgets
        apply_widget = QWidget()
        apply_layout = QHBoxLayout(apply_widget)
        apply_layout.setContentsMargins(0, 5, 0, 5)
        apply_layout.addStretch()

        apply_button = QPushButton("Anwenden")
        apply_button.setStyleSheet("background-color: #0078D7; color: white;")
        apply_button.setFixedWidth(120)
        _ = apply_button.clicked.connect(self.apply_and_update)
        apply_layout.addWidget(apply_button)

        main_splitter.addWidget(apply_widget)

        # Bottom section: Transformed data preview
        bottom_widget = QWidget()
        self.setup_preview_section(bottom_widget)

        # Add the bottom widget to the main splitter
        main_splitter.addWidget(bottom_widget)

        # Set the size proportions (35% for config, 5% for button, 60% for preview)
        main_splitter.setSizes([300, 30, 400])

        main_layout.addWidget(main_splitter)

        # Button is now placed between top and bottom widgets in the main_splitter

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        _ = button_box.accepted.connect(self.accept)
        _ = button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

    def setup_options_section(self, parent_widget: QWidget) -> None:
        """Set up the import options section.

        Args:
            parent_widget: The parent widget to attach the options to
        """
        options_layout = QVBoxLayout(parent_widget)

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

    def setup_transformation_section(self, parent_widget: QWidget) -> None:
        """Set up the transformation section.

        Args:
            parent_widget: The parent widget to attach the transformation controls to
        """
        transform_layout = QVBoxLayout(parent_widget)

        # Group box for transformation list
        transform_group = QGroupBox("Transformationsliste")
        group_layout = QVBoxLayout(transform_group)

        # List of transformations
        self.transformations_list = QListWidget()
        group_layout.addWidget(self.transformations_list)

        # Setup context menu for list
        self.transformations_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        _ = self.transformations_list.customContextMenuRequested.connect(self.show_transformation_context_menu)

        # Setup double-click to edit
        _ = self.transformations_list.itemDoubleClicked.connect(self.edit_selected_transformation)

        # Explanation text
        info_label = QLabel("Wählen Sie eine Transformation aus der Liste aus, um sie zu bearbeiten (Doppelklick), oder fügen Sie eine neue Transformation hinzu.")
        info_label.setWordWrap(True)
        group_layout.addWidget(info_label)

        # Button to add transformation
        add_button = QPushButton("Neue Transformation hinzufügen")
        _ = add_button.clicked.connect(self.add_transformation_dialog)
        group_layout.addWidget(add_button)

        # Button to remove transformation
        remove_button = QPushButton("Ausgewählte Transformation entfernen")
        _ = remove_button.clicked.connect(self.remove_selected_transformation)
        group_layout.addWidget(remove_button)

        transform_layout.addWidget(transform_group)

    def setup_preview_section(self, parent_widget: QWidget) -> None:
        """Set up the data preview section.

        Args:
            parent_widget: The parent widget to attach the preview to
        """
        preview_layout = QVBoxLayout(parent_widget)

        # Missing values info group box
        missing_values_group = QGroupBox("Fehlende Werte nach Transformation")
        missing_values_layout = QVBoxLayout(missing_values_group)

        # Create a frame to contain the table and ensure it fills the available space
        table_frame = QFrame()
        table_frame.setFrameShape(QFrame.Shape.NoFrame)
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)

        # Table for missing values info
        self.missing_values_table = QTableWidget()
        self.missing_values_table.setColumnCount(3)
        self.missing_values_table.setHorizontalHeaderLabels(["Spalte", "Fehlende Werte", "Prozent"])

        # Set the table to fill the available space
        self.missing_values_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Configure the horizontal header
        header = self.missing_values_table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
            header.setStretchLastSection(True)

        self.missing_values_table.setAlternatingRowColors(True)

        # Add the table to the frame layout
        table_layout.addWidget(self.missing_values_table)

        # Add the frame to the group layout
        missing_values_layout.addWidget(table_frame)

        # Add explanation
        missing_values_info = QLabel("Diese Tabelle zeigt die Anzahl der fehlenden Werte pro Spalte nach Anwendung aller Transformationen.")
        missing_values_info.setWordWrap(True)
        missing_values_layout.addWidget(missing_values_info)

        preview_layout.addWidget(missing_values_group)

        # Preview group box
        preview_group = QGroupBox("Vorschau der transformierten Daten")
        preview_inner_layout = QVBoxLayout(preview_group)

        # Preview table
        self.preview_table = QTableWidget()
        self.preview_table.setAlternatingRowColors(True)
        preview_inner_layout.addWidget(self.preview_table)

        # Data type legend
        legend_layout = QHBoxLayout()

        legend_label = QLabel("Legende - Datentypen:")
        legend_label.setStyleSheet("font-weight: bold;")
        legend_layout.addWidget(legend_label)

        legend_types = [
            ("i", "Integer (Ganzzahl)"),
            ("f", "Float (Dezimalzahl)"),
            ("s", "String (Text)"),
            ("d", "Date (Datum)"),
            ("b", "Boolean (Ja/Nein)"),
            ("c", "Category (Kategorie)"),
            ("?", "Unbekannt/Gemischt")
        ]

        for code, description in legend_types:
            legend_item = QLabel(f"{code}: {description}")
            legend_layout.addWidget(legend_item)

        legend_layout.addStretch()
        preview_inner_layout.addLayout(legend_layout)

        preview_layout.addWidget(preview_group)

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

        # Lade den vollständigen Datensatz für die Statistiken und für den späteren Import
        self.load_full_dataset()

        # Since we've removed tabs, always show the transformed preview
        self.update_transformation_preview()

    def load_full_dataset(self) -> None:
        """Loads the complete dataset for calculating statistics and for later import."""
        try:
            # Determine header row setting
            header = 0 if self.import_options['has_header'] else None

            # Read the entire CSV file
            self.full_df = pd.read_csv(
                self.file_path,
                delimiter=str(self.import_options['delimiter']),
                encoding=str(self.import_options['encoding']),
                header=header,
                skiprows=int(self.import_options['skip_rows']),
                decimal=str(self.import_options['decimal']),
                thousands=str(self.import_options['thousands'])
            )

            # If no header is present, rename the columns
            if not self.import_options['has_header']:
                self.full_df.columns = [f"Spalte_{i+1}" for i in range(len(self.full_df.columns))]

        except Exception as e:
            print(f"Error loading the complete dataset: {e}")
            self.full_df = None

    def get_data_type_code(self, column_data) -> str:
        """Get a single character code representing the data type of a column.

        Args:
            column_data: Series data from a pandas DataFrame column

        Returns:
            A single character representing the data type
        """
        if pd.api.types.is_integer_dtype(column_data):
            return "i"  # Integer
        elif pd.api.types.is_float_dtype(column_data):
            return "f"  # Float
        elif pd.api.types.is_datetime64_any_dtype(column_data):
            return "d"  # Date
        elif pd.api.types.is_bool_dtype(column_data):
            return "b"  # Boolean
        elif hasattr(column_data, 'cat') or str(column_data.dtype) == 'category':
            return "c"  # Category
        elif pd.api.types.is_string_dtype(column_data) or pd.api.types.is_object_dtype(column_data):
            # Check if it's truly a string or mixed
            if column_data.apply(lambda x: isinstance(x, str)).all():
                return "s"  # String
            else:
                return "?"  # Mixed/Unknown
        else:
            return "?"  # Unknown

    def calculate_missing_values(self) -> Dict[str, Dict[str, Any]]:
        """Calculates the missing values for each column in the complete dataset.

        Returns:
            Dictionary with column name as key and information about missing values
        """
        missing_values_info = {}

        # If no complete dataset is available, use the preview
        df_to_use = self.full_df if self.full_df is not None else self.transformed_df

        if df_to_use is None:
            return missing_values_info

        # Apply transformations to the complete dataset
        if self.full_df is not None:
            transformed_full_df = self.data_transformer.apply_all(self.full_df)
        else:
            transformed_full_df = self.transformed_df

        # Ensure that transformed_full_df is not None
        if transformed_full_df is None:
            return missing_values_info

        # Calculate missing values for each column
        for col in transformed_full_df.columns:
            # Number of missing values
            null_count = transformed_full_df[col].isna().sum()
            # Total number of values
            total_count = len(transformed_full_df)
            # Percentage of missing values
            null_percent = (null_count / total_count) * 100 if total_count > 0 else 0

            missing_values_info[col] = {
                'count': null_count,
                'total': total_count,
                'percent': null_percent
            }

        return missing_values_info

    def update_missing_values_info(self) -> None:
        """Updates the table with information about missing values."""
        # Calculate missing values
        self.missing_values_info = self.calculate_missing_values()

        if not self.missing_values_info:
            # Clear the table if no information is available
            self.missing_values_table.setRowCount(0)
            return

        # Update the table
        self.missing_values_table.setRowCount(len(self.missing_values_info))

        # Fill the table with data
        for row, (col_name, info) in enumerate(self.missing_values_info.items()):
            # Column name
            self.missing_values_table.setItem(row, 0, QTableWidgetItem(col_name))

            # Number of missing values
            count_item = QTableWidgetItem(f"{info['count']} / {info['total']}")
            self.missing_values_table.setItem(row, 1, count_item)

            # Percentage of missing values
            percent_item = QTableWidgetItem(f"{info['percent']:.2f}%")
            self.missing_values_table.setItem(row, 2, percent_item)

            # Color only the "Missing Values" and "Percent" cells dark red if missing values are present
            if info['count'] > 0:
                # Only color columns 1 (Missing Values) and 2 (Percent)
                for col in range(1, 3):
                    item = self.missing_values_table.item(row, col)
                    if item:
                        item.setBackground(QBrush(QColor(180, 0, 0)))  # Dark red
                        item.setForeground(QBrush(QColor(255, 255, 255)))  # White text for better contrast

        # Adjust column width to content
        self.missing_values_table.resizeColumnsToContents()

        # Force the table to update its layout and use the full width
        self.missing_values_table.updateGeometry()

        # Ensure the header is properly configured
        header = self.missing_values_table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
            header.setStretchLastSection(True)

    def update_transformation_preview(self) -> None:
        """Updates the preview of the transformed data."""
        if self.preview_df is None:
            return

        # If no transformations have been applied yet, show the original data
        if self.transformed_df is None:
            self.transformed_df = self.data_transformer.apply_all(self.preview_df)

        # Update the table
        self.preview_table.setRowCount(len(self.transformed_df))
        self.preview_table.setColumnCount(len(self.transformed_df.columns))

        # Set headers with data type
        column_headers = []
        for col in self.transformed_df.columns:
            data_type = self.get_data_type_code(self.transformed_df[col])
            column_headers.append(f"{col} [{data_type}]")

        self.preview_table.setHorizontalHeaderLabels(column_headers)

        # Fill data
        for row in range(len(self.transformed_df)):
            for col in range(len(self.transformed_df.columns)):
                value = self.transformed_df.iloc[row, col]
                item = QTableWidgetItem(str(value))

                # Mark missing values in dark red
                if pd.isna(value):
                    item.setBackground(QBrush(QColor(180, 0, 0)))  # Dark red
                    item.setForeground(QBrush(QColor(255, 255, 255)))  # White text for better contrast

                self.preview_table.setItem(row, col, item)

        # Adjust column width to content
        self.preview_table.resizeColumnsToContents()

        # Update the missing values information
        self.update_missing_values_info()

    def edit_selected_transformation(self) -> None:
        """Opens the dialog to edit the selected transformation."""
        selected_items = self.transformations_list.selectedItems()
        if selected_items:
            # Get the index of the selected transformation
            index = self.transformations_list.row(selected_items[0])
            if 0 <= index < len(self.data_transformer.transformations):
                self.edit_transformation_dialog(index)

    def _update_transformation_list(self) -> None:
        """Updates the list of transformations in the UI."""
        self.transformations_list.clear()

        for desc in self.data_transformer.get_transformation_descriptions():
            self.transformations_list.addItem(desc)

    def show_transformation_context_menu(self, position) -> None:
        """Shows a context menu for the transformation list.

        Args:
            position: Position of the mouse click
        """
        selected_items = self.transformations_list.selectedItems()
        if not selected_items:
            return

        menu = QMenu()

        # Edit option
        edit_action = QAction("Bearbeiten", self)
        _ = edit_action.triggered.connect(self.edit_selected_transformation)
        menu.addAction(edit_action)

        # Remove option
        remove_action = QAction("Entfernen", self)
        _ = remove_action.triggered.connect(self.remove_selected_transformation)
        menu.addAction(remove_action)

        # Show the menu at the position of the mouse click
        _ = menu.exec(self.transformations_list.mapToGlobal(position))

    def remove_selected_transformation(self) -> None:
        """Removes the selected transformation from the list."""
        selected_items = self.transformations_list.selectedItems()
        if selected_items:
            # Get the index of the selected transformation
            index = self.transformations_list.row(selected_items[0])

            # Remove the transformation
            self.data_transformer.remove_transformation(index)

            # Update the UI
            self._update_transformation_list()

            # Update the preview and missing values info
            self.update_transformation_preview()

    def add_transformation_dialog(self) -> None:
        """Opens a dialog to add a new transformation."""
        # Create a dialog window for selecting the transformation
        dialog = QDialog(self)
        dialog.setWindowTitle("Transformation hinzufügen")
        dialog.setMinimumWidth(500)
        dialog.setMinimumHeight(400)

        layout = QVBoxLayout(dialog)

        # Column selection
        form_layout = QFormLayout()
        # Set labels to be left-aligned
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        column_combo = QComboBox()

        # Add all available columns
        if self.preview_df is not None:
            for column in self.preview_df.columns:
                column_combo.addItem(column)

        form_layout.addRow("Spalte:", column_combo)

        # Transformation type
        type_combo = QComboBox()
        type_combo.addItems([
            "Fehlende Werte",
            "Typkonvertierung",
            "Textoperation",
            "Numerische Operation",
            "Ausreißerbehandlung"
        ])
        form_layout.addRow("Transformationstyp:", type_combo)

        # Operation (depends on type)
        operation_combo = QComboBox()
        form_layout.addRow("Operation:", operation_combo)

        # Container for configuration options
        config_container = QWidget()
        config_layout = QFormLayout(config_container)
        config_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        # Placeholder for configuration options
        config_placeholder = QLabel("Wählen Sie eine Operation aus, um die Konfigurationsoptionen anzuzeigen.")
        config_placeholder.setWordWrap(True)
        config_layout.addRow(config_placeholder)

        # Update the operation list when the type changes
        def update_operation_list():
            operation_combo.clear()
            selected_type = type_combo.currentText()

            if selected_type == "Fehlende Werte":
                operation_combo.addItems([
                    "Entfernen",
                    "Durch Mittelwert ersetzen",
                    "Durch Median ersetzen",
                    "Durch Modus ersetzen",
                    "Durch benutzerdefinierten Wert ersetzen"
                ])
            elif selected_type == "Typkonvertierung":
                operation_combo.addItems([
                    "In Zahl konvertieren",
                    "In Text konvertieren",
                    "In Datum konvertieren",
                    "In Kategorie konvertieren"
                ])
            elif selected_type == "Textoperation":
                operation_combo.addItems([
                    "In Kleinbuchstaben",
                    "In Großbuchstaben",
                    "Leerzeichen entfernen",
                    "Text ersetzen"
                ])
            elif selected_type == "Numerische Operation":
                operation_combo.addItems([
                    "Runden",
                    "Normalisieren",
                    "Standardisieren",
                    "Wertebereich begrenzen"
                ])
            elif selected_type == "Ausreißerbehandlung":
                operation_combo.addItems([
                    "Ausreißer entfernen",
                    "Ausreißer begrenzen"
                ])

            # Update the configuration options
            update_config_options()

        # Configuration options based on the selected operation
        def update_config_options():
            # Delete all existing widgets
            while config_layout.rowCount() > 0:
                config_layout.removeRow(0)

            # We don't need the type, just the operation
            _ = type_combo.currentText()
            selected_operation = operation_combo.currentText()

            # Show corresponding configuration options
            if selected_operation == "Durch benutzerdefinierten Wert ersetzen":
                replace_value = QLineEdit()
                replace_value.setObjectName("value")
                config_layout.addRow("Ersatzwert:", replace_value)

            elif selected_operation == "In Datum konvertieren":
                format_input = QLineEdit()
                format_input.setObjectName("format")
                format_input.setText("%Y-%m-%d")
                format_input.setPlaceholderText("%Y-%m-%d")
                config_layout.addRow("Datumsformat:", format_input)

            elif selected_operation == "Text ersetzen":
                pattern_input = QLineEdit()
                pattern_input.setObjectName("pattern")
                config_layout.addRow("Suchmuster:", pattern_input)

                replacement_input = QLineEdit()
                replacement_input.setObjectName("replacement")
                config_layout.addRow("Ersetzung:", replacement_input)

            elif selected_operation == "Runden":
                decimals_input = QSpinBox()
                decimals_input.setObjectName("decimals")
                decimals_input.setRange(0, 10)
                decimals_input.setValue(0)
                config_layout.addRow("Dezimalstellen:", decimals_input)

            elif selected_operation == "Wertebereich begrenzen":
                min_input = QDoubleSpinBox()
                min_input.setObjectName("min")
                min_input.setRange(-1000000, 1000000)
                min_input.setValue(0)
                config_layout.addRow("Minimalwert:", min_input)

                max_input = QDoubleSpinBox()
                max_input.setObjectName("max")
                max_input.setRange(-1000000, 1000000)
                max_input.setValue(100)
                config_layout.addRow("Maximalwert:", max_input)

            elif selected_operation == "Ausreißer entfernen":
                threshold_input = QDoubleSpinBox()
                threshold_input.setObjectName("threshold")
                threshold_input.setRange(0.1, 10.0)
                threshold_input.setSingleStep(0.1)
                threshold_input.setValue(3.0)
                config_layout.addRow("Schwellenwert (Standardabweichungen):", threshold_input)

            elif selected_operation == "Ausreißer begrenzen":
                lower_input = QDoubleSpinBox()
                lower_input.setObjectName("lower")
                lower_input.setRange(0.0, 0.5)
                lower_input.setSingleStep(0.01)
                lower_input.setValue(0.05)
                config_layout.addRow("Unteres Perzentil:", lower_input)

                upper_input = QDoubleSpinBox()
                upper_input.setObjectName("upper")
                upper_input.setRange(0.5, 1.0)
                upper_input.setSingleStep(0.01)
                upper_input.setValue(0.95)
                config_layout.addRow("Oberes Perzentil:", upper_input)

            # If no configuration options are available, show placeholder
            if config_layout.rowCount() == 0:
                placeholder = QLabel("Diese Operation benötigt keine zusätzlichen Konfigurationsoptionen.")
                placeholder.setWordWrap(True)
                config_layout.addRow(placeholder)

        # Initialize the lists
        update_operation_list()

        # Connect signals
        _ = type_combo.currentTextChanged.connect(update_operation_list)
        _ = operation_combo.currentTextChanged.connect(update_config_options)

        # Add layouts to the main layout
        layout.addLayout(form_layout)

        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # Heading for configuration options
        config_label = QLabel("Konfigurationsoptionen:")
        config_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(config_label)

        # Add configuration container
        layout.addWidget(config_container)

        # Add space
        layout.addStretch()

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        _ = button_box.accepted.connect(dialog.accept)
        _ = button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        # Show dialog
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            # Convert UI selection to TransformationOperation
            selected_column = column_combo.currentText()
            selected_type_text = type_combo.currentText()
            selected_operation_text = operation_combo.currentText()

            # Convert text to corresponding enum value
            operation = self._get_operation_from_text(selected_type_text, selected_operation_text)

            if operation:
                # Collect parameters from configuration options
                parameters = {}

                # Find all input fields in the configuration container
                for i in range(config_layout.rowCount()):
                    widget_item = config_layout.itemAt(i, QFormLayout.ItemRole.FieldRole)
                    if widget_item is None or widget_item.widget() is None:
                        continue

                    widget = widget_item.widget()
                    if not hasattr(widget, 'objectName'):
                        continue

                    # Type check for objectName
                    if widget is None:
                        continue

                    try:
                        param_name = widget.objectName()
                        if not param_name:
                            continue
                    except (AttributeError, TypeError):
                        continue

                    # Extract value based on widget type
                    if isinstance(widget, QLineEdit):
                        parameters[param_name] = widget.text()
                    elif isinstance(widget, QSpinBox):
                        parameters[param_name] = widget.value()
                    elif isinstance(widget, QDoubleSpinBox):
                        parameters[param_name] = widget.value()

                # Create a new transformation
                transformation = DataTransformation(
                    column=selected_column,
                    operation=operation,
                    parameters=parameters
                )

                # Add the transformation
                self.data_transformer.add_transformation(transformation)

                # Update the transformation list in the UI
                self._update_transformation_list()

                # Update the preview and missing values info
                self.update_transformation_preview()

    def edit_transformation_dialog(self, index: int) -> None:
        """Opens a dialog to edit an existing transformation.

        Args:
            index: Index of the transformation to edit
        """
        if not (0 <= index < len(self.data_transformer.transformations)):
            return

        # Get the transformation to edit
        transformation = self.data_transformer.transformations[index]

        # Create a dialog window for editing the transformation
        dialog = QDialog(self)
        dialog.setWindowTitle("Transformation bearbeiten")
        dialog.setMinimumWidth(500)
        dialog.setMinimumHeight(400)

        layout = QVBoxLayout(dialog)

        # Column selection (disabled as the column should not be changed)
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        column_label = QLabel(transformation.column)
        column_label.setStyleSheet("font-weight: bold;")
        form_layout.addRow("Spalte:", column_label)

        # Transformation type and operation (for information only)
        operation_name = transformation.operation.name.replace('_', ' ').title()
        operation_label = QLabel(operation_name)
        operation_label.setStyleSheet("font-weight: bold;")
        form_layout.addRow("Operation:", operation_label)

        # Container for configuration options
        config_container = QWidget()
        config_layout = QFormLayout(config_container)
        config_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        # Add configuration options based on the operation
        if transformation.operation == TransformationOperation.REPLACE_CUSTOM:
            replace_value = QLineEdit()
            replace_value.setObjectName("value")
            replace_value.setText(str(transformation.parameters.get('value', '')))
            config_layout.addRow("Ersatzwert:", replace_value)

        elif transformation.operation == TransformationOperation.CONVERT_TO_DATE:
            format_input = QLineEdit()
            format_input.setObjectName("format")
            format_input.setText(str(transformation.parameters.get('format', '%Y-%m-%d')))
            format_input.setPlaceholderText("%Y-%m-%d")
            config_layout.addRow("Datumsformat:", format_input)

        elif transformation.operation == TransformationOperation.TEXT_REPLACE:
            pattern_input = QLineEdit()
            pattern_input.setObjectName("pattern")
            pattern_input.setText(str(transformation.parameters.get('pattern', '')))
            config_layout.addRow("Suchmuster:", pattern_input)

            replacement_input = QLineEdit()
            replacement_input.setObjectName("replacement")
            replacement_input.setText(str(transformation.parameters.get('replacement', '')))
            config_layout.addRow("Ersetzung:", replacement_input)

        elif transformation.operation == TransformationOperation.NUMERIC_ROUND:
            decimals_input = QSpinBox()
            decimals_input.setObjectName("decimals")
            decimals_input.setRange(0, 10)
            decimals_input.setValue(int(transformation.parameters.get('decimals', 0)))
            config_layout.addRow("Dezimalstellen:", decimals_input)

        elif transformation.operation == TransformationOperation.NUMERIC_LIMIT_RANGE:
            min_input = QDoubleSpinBox()
            min_input.setObjectName("min")
            min_input.setRange(-1000000, 1000000)
            min_input.setValue(float(transformation.parameters.get('min', 0)))
            config_layout.addRow("Minimalwert:", min_input)

            max_input = QDoubleSpinBox()
            max_input.setObjectName("max")
            max_input.setRange(-1000000, 1000000)
            max_input.setValue(float(transformation.parameters.get('max', 100)))
            config_layout.addRow("Maximalwert:", max_input)

        elif transformation.operation == TransformationOperation.OUTLIER_REMOVE:
            threshold_input = QDoubleSpinBox()
            threshold_input.setObjectName("threshold")
            threshold_input.setRange(0.1, 10.0)
            threshold_input.setSingleStep(0.1)
            threshold_input.setValue(float(transformation.parameters.get('threshold', 3.0)))
            config_layout.addRow("Schwellenwert (Standardabweichungen):", threshold_input)

        elif transformation.operation == TransformationOperation.OUTLIER_WINSORIZE:
            lower_input = QDoubleSpinBox()
            lower_input.setObjectName("lower")
            lower_input.setRange(0.0, 0.5)
            lower_input.setSingleStep(0.01)
            lower_input.setValue(float(transformation.parameters.get('lower', 0.05)))
            config_layout.addRow("Unteres Perzentil:", lower_input)

            upper_input = QDoubleSpinBox()
            upper_input.setObjectName("upper")
            upper_input.setRange(0.5, 1.0)
            upper_input.setSingleStep(0.01)
            upper_input.setValue(float(transformation.parameters.get('upper', 0.95)))
            config_layout.addRow("Oberes Perzentil:", upper_input)

        # If no configuration options are available, show placeholder
        if config_layout.rowCount() == 0:
            placeholder = QLabel("Diese Operation benötigt keine zusätzlichen Konfigurationsoptionen.")
            placeholder.setWordWrap(True)
            config_layout.addRow(placeholder)

        # Add layouts to the main layout
        layout.addLayout(form_layout)

        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # Heading for configuration options
        config_label = QLabel("Konfigurationsoptionen:")
        config_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(config_label)

        # Add configuration container
        layout.addWidget(config_container)

        # Add space
        layout.addStretch()

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        _ = button_box.accepted.connect(dialog.accept)
        _ = button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        # Show dialog
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            # Collect parameters from configuration options
            parameters = {}

            # Find all input fields in the configuration container
            for i in range(config_layout.rowCount()):
                widget_item = config_layout.itemAt(i, QFormLayout.ItemRole.FieldRole)
                if widget_item is None or widget_item.widget() is None:
                    continue

                widget = widget_item.widget()
                if not hasattr(widget, 'objectName'):
                    continue

                # Type check for objectName
                if widget is None:
                    continue

                try:
                    param_name = widget.objectName()
                    if not param_name:
                        continue
                except (AttributeError, TypeError):
                    continue

                # Extract value based on widget type
                if isinstance(widget, QLineEdit):
                    parameters[param_name] = widget.text()
                elif isinstance(widget, QSpinBox):
                    parameters[param_name] = widget.value()
                elif isinstance(widget, QDoubleSpinBox):
                    parameters[param_name] = widget.value()

            # Update the parameters of the transformation
            transformation.parameters = parameters

            # Update the transformation list in the UI
            self._update_transformation_list()

            # Update the preview and missing values info
            self.update_transformation_preview()

    def _get_operation_from_text(self, type_text: str, operation_text: str) -> Optional[TransformationOperation]:
        """Converts text to a TransformationOperation enum value.

        Args:
            type_text: Transformation type as text
            operation_text: Operation type as text

        Returns:
            Corresponding enum value or None if no mapping was found
        """
        # Mapping from text to TransformationOperation
        type_operation_map = {
            "Fehlende Werte": {
                "Entfernen": TransformationOperation.REMOVE_MISSING,
                "Durch Mittelwert ersetzen": TransformationOperation.REPLACE_MEAN,
                "Durch Median ersetzen": TransformationOperation.REPLACE_MEDIAN,
                "Durch Modus ersetzen": TransformationOperation.REPLACE_MODE,
                "Durch benutzerdefinierten Wert ersetzen": TransformationOperation.REPLACE_CUSTOM
            },
            "Typkonvertierung": {
                "In Zahl konvertieren": TransformationOperation.CONVERT_TO_NUMERIC,
                "In Text konvertieren": TransformationOperation.CONVERT_TO_TEXT,
                "In Datum konvertieren": TransformationOperation.CONVERT_TO_DATE,
                "In Kategorie konvertieren": TransformationOperation.CONVERT_TO_CATEGORICAL
            },
            "Textoperation": {
                "In Kleinbuchstaben": TransformationOperation.TEXT_LOWERCASE,
                "In Großbuchstaben": TransformationOperation.TEXT_UPPERCASE,
                "Leerzeichen entfernen": TransformationOperation.TEXT_TRIM,
                "Text ersetzen": TransformationOperation.TEXT_REPLACE
            },
            "Numerische Operation": {
                "Runden": TransformationOperation.NUMERIC_ROUND,
                "Normalisieren": TransformationOperation.NUMERIC_NORMALIZE,
                "Standardisieren": TransformationOperation.NUMERIC_STANDARDIZE,
                "Wertebereich begrenzen": TransformationOperation.NUMERIC_LIMIT_RANGE
            },
            "Ausreißerbehandlung": {
                "Ausreißer entfernen": TransformationOperation.OUTLIER_REMOVE,
                "Ausreißer begrenzen": TransformationOperation.OUTLIER_WINSORIZE
            }
        }

        return type_operation_map.get(type_text, {}).get(operation_text)

    def apply_transformations(self) -> None:
        """Applies all transformations to the preview data."""
        if self.preview_df is not None:
            # Apply transformations to the preview data
            self.transformed_df = self.data_transformer.apply_all(self.preview_df)

            # Update the preview
            self.update_transformation_preview()

    def apply_and_update(self) -> None:
        """Updates the preview with current options and applies all transformations."""
        # First update the preview with current import options
        self.update_preview()

        # Then apply transformations if we have data
        if self.preview_df is not None:
            # Apply all transformations to the preview data
            self.transformed_df = self.data_transformer.apply_all(self.preview_df)

            # Update the preview
            self.update_transformation_preview()

    def get_import_options(self) -> Dict[str, Any]:
        """Get the current import options.

        Returns:
            Dictionary of import options
        """
        # Stelle sicher, dass die Optionen aktuell sind
        self.on_option_changed()
        return self.import_options

    def get_transformed_data(self) -> Optional[pd.DataFrame]:
        """Gibt die transformierten Daten zurück.

        Returns:
            Die transformierten Daten oder None, wenn keine Transformationen angewendet wurden
        """
        # Wenn der vollständige Datensatz vorhanden ist, wende die Transformationen darauf an
        if self.full_df is not None:
            return self.data_transformer.apply_all(self.full_df)

        # Ansonsten gib die transformierte Vorschau zurück
        return self.transformed_df
