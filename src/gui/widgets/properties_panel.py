"""Properties panel widget for DataInspect application.

This widget displays properties and configuration options for the currently selected item.
"""
from typing import Optional, Any
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QScrollArea,
    QFormLayout, QStackedWidget
)
from PyQt6.QtCore import Qt

from src.data.models import DataSource, Dataset, Column, Visualization
from src.config import UI_COLORS
from src.gui.styles import get_card_style


class PropertiesPanel(QWidget):
    """Panel for displaying and editing properties of the selected item."""

    def __init__(self, parent=None) -> None:
        """Initialize the properties panel.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.current_item: Optional[Any] = None
        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Title
        self.title_label = QLabel("Eigenschaften")
        _ = self.title_label.setProperty("title", True)
        layout.addWidget(self.title_label)

        # Scroll area for properties
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        # Stacked widget to show different property panels
        self.stacked_widget = QStackedWidget()

        # Empty panel
        self.empty_panel = QWidget()
        empty_layout = QVBoxLayout(self.empty_panel)
        empty_label = QLabel("Kein Element ausgewählt")
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        _ = empty_label.setProperty("dimmed", True)
        empty_layout.addWidget(empty_label)

        # Data source panel
        self.data_source_panel = QWidget()
        self.setup_data_source_panel()

        # Dataset panel
        self.dataset_panel = QWidget()
        self.setup_dataset_panel()

        # Column panel
        self.column_panel = QWidget()
        self.setup_column_panel()

        # Visualization panel
        self.visualization_panel = QWidget()
        self.setup_visualization_panel()

        # Add panels to stacked widget
        _ = self.stacked_widget.addWidget(self.empty_panel)
        _ = self.stacked_widget.addWidget(self.data_source_panel)
        _ = self.stacked_widget.addWidget(self.dataset_panel)
        _ = self.stacked_widget.addWidget(self.column_panel)
        _ = self.stacked_widget.addWidget(self.visualization_panel)

        # Show empty panel initially
        self.stacked_widget.setCurrentWidget(self.empty_panel)

        scroll_area.setWidget(self.stacked_widget)
        layout.addWidget(scroll_area)

    def setup_data_source_panel(self) -> None:
        """Set up the data source properties panel."""
        layout = QVBoxLayout(self.data_source_panel)
        layout.setContentsMargins(0, 0, 0, 0)

        # Basic info card
        info_card = QFrame()
        info_card.setStyleSheet(get_card_style())
        info_layout = QFormLayout(info_card)

        self.ds_name_label = QLabel()
        info_layout.addRow("Name:", self.ds_name_label)

        self.ds_type_label = QLabel()
        info_layout.addRow("Typ:", self.ds_type_label)

        self.ds_created_label = QLabel()
        info_layout.addRow("Erstellt:", self.ds_created_label)

        self.ds_path_label = QLabel()
        self.ds_path_label.setWordWrap(True)
        info_layout.addRow("Pfad:", self.ds_path_label)

        layout.addWidget(info_card)

        # Dataset info card
        dataset_card = QFrame()
        dataset_card.setStyleSheet(get_card_style())
        dataset_layout = QVBoxLayout(dataset_card)

        dataset_title = QLabel("Dataset")
        _ = dataset_title.setProperty("title", True)
        dataset_layout.addWidget(dataset_title)

        dataset_form = QFormLayout()

        self.ds_rows_label = QLabel()
        dataset_form.addRow("Zeilen:", self.ds_rows_label)

        self.ds_columns_label = QLabel()
        dataset_form.addRow("Spalten:", self.ds_columns_label)

        dataset_layout.addLayout(dataset_form)
        layout.addWidget(dataset_card)

        # Placeholder for future visualization list
        vis_card = QFrame()
        vis_card.setStyleSheet(get_card_style())
        vis_layout = QVBoxLayout(vis_card)

        vis_title = QLabel("Visualisierungen")
        _ = vis_title.setProperty("title", True)
        vis_layout.addWidget(vis_title)

        vis_placeholder = QLabel("Keine Visualisierungen vorhanden")
        _ = vis_placeholder.setProperty("dimmed", True)
        vis_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vis_layout.addWidget(vis_placeholder)

        layout.addWidget(vis_card)
        layout.addStretch()

    def setup_dataset_panel(self) -> None:
        """Set up the dataset properties panel."""
        layout = QVBoxLayout(self.dataset_panel)
        layout.setContentsMargins(0, 0, 0, 0)

        # Basic info card
        info_card = QFrame()
        info_card.setStyleSheet(get_card_style())
        info_layout = QFormLayout(info_card)

        self.dataset_rows_label = QLabel()
        info_layout.addRow("Zeilen:", self.dataset_rows_label)

        self.dataset_columns_label = QLabel()
        info_layout.addRow("Spalten:", self.dataset_columns_label)

        self.dataset_created_label = QLabel()
        info_layout.addRow("Erstellt:", self.dataset_created_label)

        self.dataset_modified_label = QLabel()
        info_layout.addRow("Geändert:", self.dataset_modified_label)

        layout.addWidget(info_card)

        # Placeholder for future filtering options
        filter_card = QFrame()
        filter_card.setStyleSheet(get_card_style(UI_COLORS['accent_secondary']))
        filter_layout = QVBoxLayout(filter_card)

        filter_title = QLabel("Filteroptionen")
        _ = filter_title.setProperty("title", True)
        filter_layout.addWidget(filter_title)

        filter_placeholder = QLabel("Hier werden zukünftig Filteroptionen angezeigt")
        _ = filter_placeholder.setProperty("dimmed", True)
        filter_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        filter_layout.addWidget(filter_placeholder)

        layout.addWidget(filter_card)
        layout.addStretch()

    def setup_column_panel(self) -> None:
        """Set up the column properties panel."""
        layout = QVBoxLayout(self.column_panel)
        layout.setContentsMargins(0, 0, 0, 0)

        # Basic info card
        info_card = QFrame()
        info_card.setStyleSheet(get_card_style())
        info_layout = QFormLayout(info_card)

        self.column_name_label = QLabel()
        info_layout.addRow("Name:", self.column_name_label)

        self.column_type_label = QLabel()
        info_layout.addRow("Datentyp:", self.column_type_label)

        self.column_original_type_label = QLabel()
        info_layout.addRow("Originaltyp:", self.column_original_type_label)

        layout.addWidget(info_card)

        # Statistics card
        stats_card = QFrame()
        stats_card.setStyleSheet(get_card_style())
        stats_layout = QVBoxLayout(stats_card)

        stats_title = QLabel("Statistiken")
        _ = stats_title.setProperty("title", True)
        stats_layout.addWidget(stats_title)

        self.stats_layout = QFormLayout()
        stats_layout.addLayout(self.stats_layout)

        layout.addWidget(stats_card)
        layout.addStretch()

    def setup_visualization_panel(self) -> None:
        """Set up the visualization properties panel."""
        layout = QVBoxLayout(self.visualization_panel)
        layout.setContentsMargins(0, 0, 0, 0)

        # Basic info card
        info_card = QFrame()
        info_card.setStyleSheet(get_card_style())
        info_layout = QFormLayout(info_card)

        self.vis_name_label = QLabel()
        info_layout.addRow("Name:", self.vis_name_label)

        self.vis_type_label = QLabel()
        info_layout.addRow("Typ:", self.vis_type_label)

        self.vis_created_label = QLabel()
        info_layout.addRow("Erstellt:", self.vis_created_label)

        self.vis_modified_label = QLabel()
        info_layout.addRow("Geändert:", self.vis_modified_label)

        layout.addWidget(info_card)

        # Configuration card
        config_card = QFrame()
        config_card.setStyleSheet(get_card_style(UI_COLORS['accent_primary']))
        config_layout = QVBoxLayout(config_card)

        config_title = QLabel("Konfiguration")
        _ = config_title.setProperty("title", True)
        config_layout.addWidget(config_title)

        self.config_layout = QFormLayout()
        config_layout.addLayout(self.config_layout)

        layout.addWidget(config_card)

        # Export options card
        export_card = QFrame()
        export_card.setStyleSheet(get_card_style(UI_COLORS['accent_tertiary']))
        export_layout = QVBoxLayout(export_card)

        export_title = QLabel("Exportoptionen")
        _ = export_title.setProperty("title", True)
        export_layout.addWidget(export_title)

        export_placeholder = QLabel("Hier werden zukünftig Exportoptionen angezeigt")
        _ = export_placeholder.setProperty("dimmed", True)
        export_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        export_layout.addWidget(export_placeholder)

        layout.addWidget(export_card)
        layout.addStretch()

    def set_data_source(self, data_source: DataSource) -> None:
        """Set the data source to display properties for.

        Args:
            data_source: The data source to display properties for
        """
        self.current_item = data_source
        self.title_label.setText(f"Eigenschaften: {data_source.name}")

        # Update data source info
        self.ds_name_label.setText(data_source.name)
        self.ds_type_label.setText(data_source.source_type)
        self.ds_created_label.setText(data_source.created_at.strftime("%d.%m.%Y %H:%M"))
        self.ds_path_label.setText(str(data_source.file_path))

        # Update dataset info if available
        if data_source.dataset:
            self.ds_rows_label.setText(str(data_source.dataset.metadata.get("rows", "-")))
            self.ds_columns_label.setText(str(data_source.dataset.metadata.get("columns", "-")))
        else:
            self.ds_rows_label.setText("-")
            self.ds_columns_label.setText("-")

        # Show data source panel
        self.stacked_widget.setCurrentWidget(self.data_source_panel)

    def set_dataset(self, dataset: Dataset) -> None:
        """Set the dataset to display properties for.

        Args:
            dataset: The dataset to display properties for
        """
        self.current_item = dataset
        self.title_label.setText("Eigenschaften: Dataset")

        # Update dataset info
        self.dataset_rows_label.setText(str(dataset.metadata.get("rows", "-")))
        self.dataset_columns_label.setText(str(dataset.metadata.get("columns", "-")))
        self.dataset_created_label.setText(dataset.created_at.strftime("%d.%m.%Y %H:%M"))
        self.dataset_modified_label.setText(dataset.modified_at.strftime("%d.%m.%Y %H:%M"))

        # Show dataset panel
        self.stacked_widget.setCurrentWidget(self.dataset_panel)

    def set_column(self, column: Column) -> None:
        """Set the column to display properties for.

        Args:
            column: The column to display properties for
        """
        self.current_item = column
        self.title_label.setText(f"Eigenschaften: {column.name}")

        # Update column info
        self.column_name_label.setText(column.name)
        self.column_type_label.setText(column.data_type)
        self.column_original_type_label.setText(column.original_type)

        # Clear existing stats
        while self.stats_layout.rowCount() > 0:
            self.stats_layout.removeRow(0)

        # Add stats
        for key, value in column.stats.items():
            self.stats_layout.addRow(f"{key}:", QLabel(str(value)))

        # Show column panel
        self.stacked_widget.setCurrentWidget(self.column_panel)

    def set_visualization(self, visualization: Visualization) -> None:
        """Set the visualization to display properties for.

        Args:
            visualization: The visualization to display properties for
        """
        self.current_item = visualization
        self.title_label.setText(f"Eigenschaften: {visualization.name}")

        # Update visualization info
        self.vis_name_label.setText(visualization.name)
        self.vis_type_label.setText(visualization.chart_type)
        self.vis_created_label.setText(visualization.created_at.strftime("%d.%m.%Y %H:%M"))
        self.vis_modified_label.setText(visualization.modified_at.strftime("%d.%m.%Y %H:%M"))

        # Clear existing config
        while self.config_layout.rowCount() > 0:
            self.config_layout.removeRow(0)

        # Add config
        for key, value in visualization.config.items():
            self.config_layout.addRow(f"{key}:", QLabel(str(value)))

        # Show visualization panel
        self.stacked_widget.setCurrentWidget(self.visualization_panel)

    def clear(self) -> None:
        """Clear the properties panel."""
        self.current_item = None
        self.title_label.setText("Eigenschaften")
        self.stacked_widget.setCurrentWidget(self.empty_panel)
