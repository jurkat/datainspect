"""Main content widget for DataInspect application.

This widget contains the main content area with tabs for data preview and visualizations.
"""
from typing import Optional, Callable
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QLabel, QFrame,
    QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt

from src.data.models import DataSource, Project
from src.gui.widgets.data_preview import DataPreviewWidget
from src.config import UI_COLORS, VISUALIZATION_TYPES


class VisualizationPlaceholder(QWidget):
    """Placeholder widget for visualizations."""

    def __init__(self, on_create_visualization: Callable[[], None], parent=None) -> None:
        """Initialize the visualization placeholder.

        Args:
            on_create_visualization: Callback for creating a new visualization
            parent: Parent widget
        """
        super().__init__(parent)
        self.on_create_visualization = on_create_visualization
        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Info label
        info_label = QLabel("Keine Visualisierung ausgewählt")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet(f"font-size: 16px; color: {UI_COLORS['foreground_dim']};")
        layout.addWidget(info_label)

        # Create visualization button
        create_button = QPushButton("Neue Visualisierung erstellen")
        _ = create_button.setProperty("accent", "primary")
        create_button.setFixedWidth(250)
        create_button.setFixedHeight(40)
        _ = create_button.clicked.connect(self.on_create_visualization)
        layout.addWidget(create_button)

        # Available visualization types
        types_frame = QFrame()
        types_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {UI_COLORS['background_lighter']};
                border: none;
                border-radius: 2px;
                padding: 2px;
                margin-top: 10px;
            }}
        """)
        types_layout = QVBoxLayout(types_frame)
        types_layout.setContentsMargins(2, 2, 2, 2)
        types_layout.setSpacing(2)

        types_label = QLabel("Verfügbare Visualisierungstypen:")
        types_label.setStyleSheet("font-weight: bold; margin-bottom: 2px;")
        types_layout.addWidget(types_label)

        # Add each visualization type
        for vis_type, vis_info in VISUALIZATION_TYPES.items():
            type_layout = QHBoxLayout()
            type_layout.setContentsMargins(0, 0, 0, 0)
            type_layout.setSpacing(4)

            icon_label = QLabel(vis_info['icon'])
            icon_label.setStyleSheet("font-size: 18px; min-width: 30px; border: none; padding: 0px;")
            type_layout.addWidget(icon_label)

            name_label = QLabel(f"<b>{vis_info['name']}</b>")
            name_label.setStyleSheet("border: none; padding: 0px;")
            type_layout.addWidget(name_label)

            desc_label = QLabel(vis_info['description'])
            desc_label.setStyleSheet(f"color: {UI_COLORS['foreground_dim']}; border: none; padding: 0px;")
            type_layout.addWidget(desc_label, 1)  # Stretch factor 1

            types_layout.addLayout(type_layout)

        layout.addWidget(types_frame)


class MainContentWidget(QWidget):
    """Widget containing the main content area with tabs."""

    def __init__(self, parent=None) -> None:
        """Initialize the main content widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.current_data_source: Optional[DataSource] = None
        self.current_project: Optional[Project] = None

        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.tab_widget.setDocumentMode(True)

        # Data preview tab
        self.data_preview = DataPreviewWidget()
        _ = self.tab_widget.addTab(self.data_preview, "Datenvorschau")

        # Visualization tab
        self.visualization_placeholder = VisualizationPlaceholder(
            on_create_visualization=self.on_create_visualization
        )
        _ = self.tab_widget.addTab(self.visualization_placeholder, "Visualisierung")

        layout.addWidget(self.tab_widget)

    def set_data_source(self, data_source: Optional[DataSource], project: Project) -> None:
        """Set the data source to display.

        Args:
            data_source: The data source to display
            project: The project containing the data source
        """
        self.current_data_source = data_source
        self.current_project = project

        # Update data preview
        self.data_preview.set_data_source(data_source, project)

        # Switch to data preview tab
        self.tab_widget.setCurrentIndex(0)

    def on_create_visualization(self) -> None:
        """Handle creating a new visualization."""
        # This will be implemented in the future
        # For now, just switch to the visualization tab
        self.tab_widget.setCurrentIndex(1)
