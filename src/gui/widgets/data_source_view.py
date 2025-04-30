"""DataSourceView widget for DataInspect application."""
from typing import Callable, List, Any, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QFrame,
    QLabel, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt
from ...config import SUPPORTED_FORMATS, UI_COLORS
from src.data.models import DataSource, Project
from .drop_zone import DropZone
from src.gui.styles import DATA_SOURCE_ITEM_STYLE, DROP_ZONE_STYLE

class DataSourceDropZone(DropZone):
    """Drop zone for data source files."""

    def __init__(self, on_file_dropped: Callable[[str], None], on_click: Optional[Callable[[], None]] = None) -> None:
        super().__init__(
            accepted_extensions=SUPPORTED_FORMATS,
            drop_hint="Datenquellen (.csv)\nhier ablegen oder klicken",
            on_file_dropped=on_file_dropped,
            on_click=on_click
        )
        self.setStyleSheet(DROP_ZONE_STYLE)

class DataSourceItem(QFrame):
    """Widget representing a single data source."""

    def __init__(
        self,
        data_source: DataSource,
        on_refresh: Callable[[DataSource], None],
        on_delete: Callable[[DataSource], None],
        on_select: Callable[[DataSource], None]
    ) -> None:
        super().__init__()
        self.data_source = data_source
        self.on_refresh = on_refresh
        self.on_delete = on_delete
        self.on_select = on_select
        self._is_selected = False

        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)

        # Source info with icon
        info_layout = QHBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(4)

        # Icon based on source type
        icon_map = {
            'CSV': '📄',
            'Excel': '📊',
            'JSON': '📋',
            'Database': '🗃️'
        }
        icon = icon_map.get(self.data_source.source_type, '📁')
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 16px;")
        info_layout.addWidget(icon_label)

        # Text info - kompaktere Darstellung
        name_label = QLabel(self.data_source.name)
        name_label.setStyleSheet("font-weight: bold;")
        info_layout.addWidget(name_label, 1)  # Stretch factor 1

        # Nur Löschen-Button
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
        _ = delete_btn.clicked.connect(lambda: self.on_delete(self.data_source))

        layout.addLayout(info_layout)
        layout.addWidget(delete_btn)

        # Styling
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setStyleSheet(DATA_SOURCE_ITEM_STYLE)

        # Make the whole item clickable
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mousePressEvent = lambda a0: self.on_select(self.data_source)

    def set_selected(self, selected: bool) -> None:
        """Set the selected state of this item.

        Args:
            selected: Whether this item is selected
        """
        self._is_selected = selected
        _ = self.setProperty("selected", selected)
        style = self.style()
        if style:
            _ = style.unpolish(self)
            _ = style.polish(self)
        self.update()

class DataSourceView(QWidget):
    """View for displaying and managing data sources."""

    def __init__(
        self,
        on_refresh_source: Callable[[DataSource], None],
        on_delete_source: Callable[[DataSource], None],
        on_select_source: Callable[[DataSource], None],
        on_add_source: Callable[[str], None]
    ) -> None:
        super().__init__()
        self.on_refresh_source = on_refresh_source
        self.on_delete_source = on_delete_source
        self.external_on_select_source = on_select_source
        self.on_add_source = on_add_source
        self.current_project: Optional[Project] = None
        self.selected_data_source: Optional[DataSource] = None
        self.item_widgets: List[DataSourceItem] = []

        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Title
        title_label = QLabel("Datenquellen")
        _ = title_label.setProperty("subtitle", True)
        _ = title_label.setStyleSheet(f"color: {UI_COLORS['foreground']}; font-weight: bold; font-size: 14px; margin-bottom: 5px;")
        layout.addWidget(title_label)

        # Drop zone - klickbar gemacht
        self.drop_zone = DataSourceDropZone(
            on_file_dropped=self.on_add_source,
            on_click=lambda: self.on_add_source("")
        )
        layout.addWidget(self.drop_zone)

        # Scrollable area for data sources
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        # Container for data source items
        self.sources_container = QWidget()
        self.sources_layout = QVBoxLayout(self.sources_container)
        self.sources_layout.setContentsMargins(0, 0, 0, 0)
        self.sources_layout.setSpacing(1)  # Minimaler Abstand
        self.sources_layout.addStretch()

        scroll_area.setWidget(self.sources_container)
        layout.addWidget(scroll_area)

    def _handle_selection(self, data_source: DataSource) -> None:
        """Handle selection of a data source.

        Args:
            data_source: The selected data source
        """
        # Update selected state
        self.selected_data_source = data_source

        # Update UI to reflect selection
        for item in self.item_widgets:
            item.set_selected(item.data_source == data_source)

        # Call the original selection handler
        self.external_on_select_source(data_source)

    def update_data_sources(self, data_sources: List[DataSource]) -> None:
        """Update the displayed data sources.

        Args:
            data_sources: List of data sources to display
        """
        # Clear existing items
        while self.sources_layout.count() > 1:  # Keep the stretch at the end
            item = self.sources_layout.takeAt(0)
            widget = item.widget() if item is not None else None
            if widget is not None:
                widget.deleteLater()

        # Clear item widgets list
        self.item_widgets = []

        # Add new items
        for source in data_sources:
            item = DataSourceItem(
                data_source=source,
                on_refresh=self.on_refresh_source,
                on_delete=self.on_delete_source,
                on_select=self._handle_selection
            )
            # Set selected state if this is the currently selected data source
            if self.selected_data_source and source.id == self.selected_data_source.id:
                item.set_selected(True)

            self.item_widgets.append(item)
            self.sources_layout.insertWidget(self.sources_layout.count() - 1, item)

    def set_project(self, project: Project) -> None:
        """Set the current project and register as observer.

        Args:
            project: The project to display and observe
        """
        # Unregister from previous project if exists
        if self.current_project is not None:
            self.current_project.remove_observer(self)

        # Register with new project
        self.current_project = project
        project.add_observer(self)

        # Update UI with current data
        self.update_data_sources(project.data_sources)

    def on_subject_change(self, subject: Any, **kwargs: Any) -> None:
        """Handle updates from observed projects.

        Implements the Observer protocol method that gets called when the observed
        Project changes.

        Args:
            subject: The subject that was changed (Project in this case)
            kwargs: Additional data about the change
        """
        if subject is self.current_project and self.current_project is not None:
            event = kwargs.get('event', '')

            # Handle different types of events
            if event in ('data_source_added', 'data_source_removed'):
                # Update the list of data sources when they change
                self.update_data_sources(self.current_project.data_sources)

    def remove_item(self, item_widget: DataSourceItem) -> None:
        """Remove an item from the list.

        Args:
            item_widget: The widget to remove
        """
        # Diese Implementierung verwendet sources_layout statt data_source_list
        for i in range(self.sources_layout.count() - 1):  # Minus 1 wegen dem Stretch am Ende
            layout_item = self.sources_layout.itemAt(i)
            if layout_item is not None and layout_item.widget() == item_widget:
                # Widget vom Layout entfernen
                self.sources_layout.removeItem(layout_item)
                widget = layout_item.widget()
                if widget is not None:
                    widget.deleteLater()
                break
