"""DataSourceView widget for DataInspect application."""
from typing import Callable, List, Any, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QFrame,
    QLabel, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt
from ...config import SUPPORTED_FORMATS
from ...data.models import DataSource, Project
from .drop_zone import DropZone

class DataSourceDropZone(DropZone):
    """Drop zone for data source files."""
    
    def __init__(self, on_file_dropped: Callable[[str], None]) -> None:
        super().__init__(
            accepted_extensions=SUPPORTED_FORMATS,
            drop_hint="Datenquellen (.csv)\nhier ablegen.",
            on_file_dropped=on_file_dropped
        )

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
        
        self.setup_ui()
        
    def setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Source info
        info_layout = QVBoxLayout()
        name_label = QLabel(self.data_source.name)
        name_label.setStyleSheet("font-weight: bold;")
        type_label = QLabel(f"Typ: {self.data_source.source_type}")
        type_label.setStyleSheet("color: #666;")
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(type_label)
        layout.addLayout(info_layout)
        
        # Buttons
        refresh_btn = QPushButton("↻")
        refresh_btn.setToolTip("Aktualisieren")
        _ = refresh_btn.clicked.connect(lambda: self.on_refresh(self.data_source))
        
        delete_btn = QPushButton("🗑")
        delete_btn.setToolTip("Löschen")
        _ = delete_btn.clicked.connect(lambda: self.on_delete(self.data_source))
        
        layout.addWidget(refresh_btn)
        layout.addWidget(delete_btn)
        
        # Styling
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QPushButton {
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        
        # Make the whole item clickable
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mousePressEvent = lambda a0: self.on_select(self.data_source)

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
        self.on_select_source = on_select_source
        self.on_add_source = on_add_source
        self.current_project: Optional[Project] = None
        
        self.setup_ui()
    
    def setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Drop zone at the top
        self.drop_zone = DataSourceDropZone(self.on_add_source)
        layout.addWidget(self.drop_zone)
        
        # Scrollable area for data sources
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        # Container for data source items
        self.sources_container = QWidget()
        self.sources_layout = QVBoxLayout(self.sources_container)
        self.sources_layout.setContentsMargins(0, 0, 0, 0)
        self.sources_layout.setSpacing(5)
        self.sources_layout.addStretch()
        
        scroll_area.setWidget(self.sources_container)
        layout.addWidget(scroll_area)

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
        
        # Add new items
        for source in data_sources:
            item = DataSourceItem(
                data_source=source,
                on_refresh=self.on_refresh_source,
                on_delete=self.on_delete_source,
                on_select=self.on_select_source
            )
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
