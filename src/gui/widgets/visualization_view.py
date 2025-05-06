"""Visualization view widget for DataInspect application."""
from typing import Optional, Callable
from typing_extensions import override
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt

from src.data.models import DataSource, Visualization, Project
from src.config import UI_COLORS


class VisualizationListItem(QWidget):
    """Widget representing a visualization in the list."""

    def __init__(
        self,
        visualization: Visualization,
        on_select: Callable[[Visualization], None],
        on_delete: Callable[[Visualization], None],
        on_edit: Callable[[Visualization], None],
        parent=None
    ) -> None:
        """Initialize the visualization list item.

        Args:
            visualization: The visualization to represent
            on_select: Callback for when the visualization is selected
            on_delete: Callback for when the visualization is deleted
            on_edit: Callback for when the visualization is edited
            parent: Parent widget
        """
        super().__init__(parent)
        self.visualization = visualization
        self.on_select = on_select
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Icon based on chart type
        icon_map = {
            'bar': '📊',
            'line': '📈',
            'pie': '🥧',
            'scatter': '🔵',
            'heatmap': '🔥'
        }
        icon = icon_map.get(self.visualization.chart_type, '📊')
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(icon_label)

        # Text info - kompaktere Darstellung
        name_label = QLabel(self.visualization.name)
        name_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(name_label, 1)  # Stretch factor 1

        # Edit button (pencil icon)
        edit_btn = QPushButton("✎")
        edit_btn.setToolTip("Bearbeiten")
        edit_btn.setFixedSize(20, 20)
        edit_btn.setStyleSheet("""
            QPushButton {
                border: none;
                color: #aaa;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                color: #fff;
                background-color: #0078D7;
                border-radius: 10px;
            }
        """)
        _ = edit_btn.clicked.connect(lambda: self.on_edit(self.visualization))
        layout.addWidget(edit_btn)

        # Delete button
        delete_btn = QPushButton("×")
        delete_btn.setToolTip("Löschen")
        delete_btn.setFixedSize(20, 20)
        delete_btn.setStyleSheet("""
            QPushButton {
                border: none;
                color: #aaa;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                color: #fff;
                background-color: #d32f2f;
                border-radius: 10px;
            }
        """)
        _ = delete_btn.clicked.connect(lambda: self.on_delete(self.visualization))
        layout.addWidget(delete_btn)

    @override
    def mousePressEvent(self, a0) -> None:
        """Handle mouse press events.

        Args:
            a0: The mouse event
        """
        super().mousePressEvent(a0)
        self.on_select(self.visualization)

    @override
    def mouseDoubleClickEvent(self, a0) -> None:
        """Handle mouse double click events.

        Args:
            a0: The mouse event
        """
        super().mouseDoubleClickEvent(a0)
        # Set a flag to indicate edit mode and then call the select handler
        from src.gui.widgets.main_content import MainContentWidget
        parent = self.parent()
        while parent:
            if isinstance(parent, MainContentWidget):
                # Use setattr to avoid protected access warning
                setattr(parent, "_edit_mode", True)
                break
            parent = parent.parent()
        self.on_select(self.visualization)


class VisualizationView(QWidget):
    """Widget for displaying and managing visualizations."""

    def __init__(
        self,
        on_select_visualization: Callable[[Visualization], None],
        on_delete_visualization: Callable[[Visualization], None],
        on_create_visualization: Callable[[], None],
        on_edit_visualization: Callable[[Visualization], None],
        parent=None
    ) -> None:
        """Initialize the visualization view.

        Args:
            on_select_visualization: Callback for when a visualization is selected
            on_delete_visualization: Callback for when a visualization is deleted
            on_create_visualization: Callback for creating a new visualization
            on_edit_visualization: Callback for editing a visualization
            parent: Parent widget
        """
        super().__init__(parent)
        self.on_select_visualization = on_select_visualization
        self.on_delete_visualization = on_delete_visualization
        self.on_create_visualization = on_create_visualization
        self.on_edit_visualization = on_edit_visualization
        self.current_data_source: Optional[DataSource] = None
        self.current_project: Optional[Project] = None
        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Title
        title_layout = QHBoxLayout()
        title_label = QLabel("Visualisierungen")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        title_layout.addWidget(title_label)

        # Add button
        add_button = QPushButton("+")
        add_button.setToolTip("Neue Visualisierung erstellen")
        add_button.setFixedSize(24, 24)
        add_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: #0078D7;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #0063B1;
            }
        """)
        _ = add_button.clicked.connect(self.on_create_visualization)
        title_layout.addWidget(add_button)

        layout.addLayout(title_layout)

        # List of visualizations
        self.visualizations_list = QListWidget()
        self.visualizations_list.setFrameShape(QFrame.Shape.NoFrame)
        self.visualizations_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {UI_COLORS['background']};
                border: none;
            }}
            QListWidget::item {{
                padding: 0px;
                border: none;
            }}
            QListWidget::item:selected {{
                background-color: {UI_COLORS['selection']};
                border: none;
            }}
        """)
        layout.addWidget(self.visualizations_list)

        # Placeholder for empty list
        self.empty_label = QLabel("Keine Visualisierungen vorhanden")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet(f"color: {UI_COLORS['foreground_dim']};")
        layout.addWidget(self.empty_label)
        self.empty_label.setVisible(False)

    def set_data_source(self, data_source: Optional[DataSource], project: Project) -> None:
        """Set the data source to display visualizations for.

        Args:
            data_source: The data source to display visualizations for
            project: The project containing the data source
        """
        self.current_data_source = data_source
        self.current_project = project
        self.update_visualizations_list()

    def update_visualizations_list(self) -> None:
        """Update the list of visualizations."""
        self.visualizations_list.clear()

        if not self.current_data_source:
            self.empty_label.setVisible(True)
            self.visualizations_list.setVisible(False)
            return

        visualizations = self.current_data_source.visualizations

        if not visualizations:
            self.empty_label.setVisible(True)
            self.visualizations_list.setVisible(False)
            return

        self.empty_label.setVisible(False)
        self.visualizations_list.setVisible(True)

        for visualization in visualizations:
            item = QListWidgetItem()
            widget = VisualizationListItem(
                visualization=visualization,
                on_select=self.on_select_visualization,
                on_delete=self.on_delete_visualization,
                on_edit=self.on_edit_visualization
            )
            item.setSizeHint(widget.sizeHint())
            self.visualizations_list.addItem(item)
            self.visualizations_list.setItemWidget(item, widget)
