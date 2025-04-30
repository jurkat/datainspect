"""Data preview widget for DataInspect application."""
from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QHBoxLayout, QGroupBox, QFormLayout
)

from src.data.models import DataSource, Dataset, Project


class DataPreviewWidget(QWidget):
    """Widget for displaying a preview of a dataset."""

    def __init__(self, parent=None) -> None:
        """Initialize the widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.current_data_source: Optional[DataSource] = None
        self.current_dataset: Optional[Dataset] = None
        self.current_project: Optional[Project] = None

        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)

        # Title
        self.title_label = QLabel("Keine Datenquelle ausgewählt")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(self.title_label)

        # Info section
        info_layout = QHBoxLayout()

        # Source info
        self.source_info_group = QGroupBox("Quellinformationen")
        source_info_layout = QFormLayout(self.source_info_group)

        self.source_type_label = QLabel("-")
        source_info_layout.addRow("Typ:", self.source_type_label)

        self.source_created_label = QLabel("-")
        source_info_layout.addRow("Erstellt:", self.source_created_label)

        info_layout.addWidget(self.source_info_group)

        # Dataset info
        self.dataset_info_group = QGroupBox("Datensatzinformationen")
        dataset_info_layout = QFormLayout(self.dataset_info_group)

        self.rows_label = QLabel("-")
        dataset_info_layout.addRow("Zeilen:", self.rows_label)

        self.columns_label = QLabel("-")
        dataset_info_layout.addRow("Spalten:", self.columns_label)

        self.format_info_label = QLabel("-")
        dataset_info_layout.addRow("Format:", self.format_info_label)

        info_layout.addWidget(self.dataset_info_group)

        layout.addLayout(info_layout)

        # Data preview
        preview_label = QLabel("Datenvorschau:")
        preview_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(preview_label)

        self.preview_table = QTableWidget()
        self.preview_table.setAlternatingRowColors(True)
        header = self.preview_table.horizontalHeader()
        if header:
            header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.preview_table)

        # Set dark mode styling
        self.setStyleSheet("""
            QGroupBox {
                background-color: #2d2d2d;
                border: 1px solid #444;
                border-radius: 4px;
                padding-top: 15px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                color: #e0e0e0;
            }
            QLabel {
                color: #e0e0e0;
            }
            QTableWidget {
                background-color: #2d2d2d;
                alternate-background-color: #3a3a3a;
                color: #e0e0e0;
                gridline-color: #444;
                border: 1px solid #444;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #3d3d3d;
                color: #e0e0e0;
                padding: 4px;
                border: 1px solid #555;
            }
        """)

    def set_data_source(self, data_source: Optional[DataSource], project: Project) -> None:
        """Set the data source to display.

        Args:
            data_source: The data source to display
            project: The project containing the data source
        """
        self.current_data_source = data_source
        self.current_project = project

        if data_source is None:
            self.clear_preview()
            return

        # Update title
        self.title_label.setText(f"Datenquelle: {data_source.name}")

        # Update source info
        self.source_type_label.setText(data_source.source_type)
        self.source_created_label.setText(data_source.created_at.strftime("%d.%m.%Y %H:%M"))

        # Get dataset from data source
        self.current_dataset = data_source.dataset

        if self.current_dataset is None:
            self.clear_dataset_info()
            return

        # Update dataset info
        self.rows_label.setText(str(self.current_dataset.metadata.get("rows", "-")))
        self.columns_label.setText(str(self.current_dataset.metadata.get("columns", "-")))

        # Format info
        format_info = []
        if "delimiter" in self.current_dataset.metadata:
            delimiter = self.current_dataset.metadata["delimiter"]
            delimiter_name = {",": "Komma", ";": "Semikolon", "\t": "Tabulator", "|": "Pipe"}.get(delimiter, delimiter)
            format_info.append(f"Trennzeichen: {delimiter_name}")

        if "has_header" in self.current_dataset.metadata:
            has_header = "Ja" if self.current_dataset.metadata["has_header"] else "Nein"
            format_info.append(f"Kopfzeile: {has_header}")

        self.format_info_label.setText(", ".join(format_info))

        # Update preview table
        self.update_preview_table()

    def update_preview_table(self) -> None:
        """Update the preview table with data from the current dataset."""
        if self.current_dataset is None or not hasattr(self.current_dataset, 'data'):
            self.preview_table.setRowCount(0)
            self.preview_table.setColumnCount(0)
            return

        # Verwende die neue get_preview-Methode
        preview_df = self.current_dataset.get_preview(10)

        # Update table dimensions
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

    def clear_preview(self) -> None:
        """Clear all preview information."""
        self.title_label.setText("Keine Datenquelle ausgewählt")
        self.source_type_label.setText("-")
        self.source_created_label.setText("-")
        self.clear_dataset_info()

    def clear_dataset_info(self) -> None:
        """Clear dataset-specific information."""
        self.rows_label.setText("-")
        self.columns_label.setText("-")
        self.format_info_label.setText("-")
        self.preview_table.setRowCount(0)
        self.preview_table.setColumnCount(0)
