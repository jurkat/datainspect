"""Main content widget for DataInspect application.

This widget contains the main content area with tabs for data preview and visualizations.
"""
from typing import Optional, Callable
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QLabel, QFrame,
    QPushButton, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt

from src.data.models import DataSource, Project, Visualization
from src.gui.widgets.data_preview import DataPreviewWidget
from src.gui.widgets.visualization_view import VisualizationView
from src.gui.widgets.visualization_display import VisualizationDisplay
from src.gui.dialogs.visualization_creation_dialog import VisualizationCreationDialog
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

        # Visualization tab - split into list and display
        visualization_tab = QWidget()
        visualization_layout = QHBoxLayout(visualization_tab)
        visualization_layout.setContentsMargins(0, 0, 0, 0)
        visualization_layout.setSpacing(0)

        # Left side: Visualization list
        self.visualization_view = VisualizationView(
            on_select_visualization=self.on_select_visualization,
            on_delete_visualization=self.on_delete_visualization,
            on_create_visualization=self.on_create_visualization,
            on_edit_visualization=self.edit_visualization
        )
        visualization_layout.addWidget(self.visualization_view, 1)  # 30% width

        # Right side: Visualization display
        self.visualization_display = VisualizationDisplay()
        visualization_layout.addWidget(self.visualization_display, 2)  # 70% width

        # Set stretch factors
        visualization_layout.setStretch(0, 1)  # Left panel: 30%
        visualization_layout.setStretch(1, 2)  # Right panel: 70%

        _ = self.tab_widget.addTab(visualization_tab, "Visualisierung")

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

        # Update visualization view
        self.visualization_view.set_data_source(data_source, project)

        # Clear visualization display
        if hasattr(self, 'visualization_display'):
            self.visualization_display.clear()

        # Switch to data preview tab
        self.tab_widget.setCurrentIndex(0)

    def on_select_visualization(self, visualization: Visualization) -> None:
        """Handle selection of a visualization.

        Args:
            visualization: The selected visualization
        """
        import logging
        logger = logging.getLogger(__name__)

        # Check if we have a data source selected
        if not self.current_data_source or not self.current_project:
            logger.warning("Keine Datenquelle ausgewählt")
            return

        # Check if the data source has a dataset
        if not self.current_data_source.dataset:
            logger.warning("Kein Datensatz vorhanden")
            return

        # Display the visualization
        try:
            logger.info("Zeige Visualisierung an: %s", visualization.name)
            self.visualization_display.display_visualization(visualization, self.current_data_source)

            # Switch to visualization tab if not already there
            if self.tab_widget.currentIndex() != 1:  # 1 is the visualization tab
                self.tab_widget.setCurrentIndex(1)

        except Exception as e:
            logger.error("Fehler beim Anzeigen der Visualisierung: %s", str(e))
            import traceback
            logger.error("Traceback: %s", traceback.format_exc())

            # Show error message
            _ = QMessageBox.critical(
                self,
                "Fehler beim Anzeigen der Visualisierung",
                f"Bei der Anzeige der Visualisierung ist ein Fehler aufgetreten: {str(e)}"
            )

        # Double-click or context menu action to edit
        if hasattr(self, '_edit_mode') and self._edit_mode:
            self._edit_mode = False  # Reset edit mode flag
            self.edit_visualization(visualization)

    def edit_visualization(self, visualization: Visualization) -> None:
        """Edit a visualization.

        Args:
            visualization: The visualization to edit
        """
        import logging
        logger = logging.getLogger(__name__)

        # Check if we have a data source selected
        if not self.current_data_source or not self.current_project:
            logger.warning("Keine Datenquelle ausgewählt")
            return

        # Check if the data source has a dataset
        if not self.current_data_source.dataset:
            logger.warning("Kein Datensatz vorhanden")
            return

        try:
            # Open the visualization dialog in edit mode
            logger.info("Öffne Visualisierungsdialog zum Bearbeiten von: %s", visualization.name)
            dialog = VisualizationCreationDialog(
                self.current_data_source,
                self,
                existing_visualization=visualization
            )
            result = dialog.exec()

            if result == VisualizationCreationDialog.DialogCode.Accepted:
                # Get the updated visualization from the dialog
                updated_visualization = dialog.get_visualization()
                logger.info("Visualisierung aktualisiert: %s", updated_visualization.name)

                # Notify that the project has changed
                if self.current_project:
                    self.current_project.modified = updated_visualization.modified_at
                    self.current_project.notify_observers()

                # Update the visualization list
                self.visualization_view.update_visualizations_list()

                # Update the visualization display
                self.visualization_display.display_visualization(updated_visualization, self.current_data_source)

                # Show success message
                _ = QMessageBox.information(
                    self,
                    "Visualisierung aktualisiert",
                    f"Die Visualisierung '{updated_visualization.name}' wurde erfolgreich aktualisiert."
                )
        except Exception as e:
            import traceback
            logger.error("Fehler beim Bearbeiten der Visualisierung: %s", str(e))
            logger.error("Traceback: %s", traceback.format_exc())

            # Show error message
            _ = QMessageBox.critical(
                self,
                "Fehler beim Bearbeiten der Visualisierung",
                f"Bei der Bearbeitung der Visualisierung ist ein Fehler aufgetreten: {str(e)}"
            )

    def on_delete_visualization(self, visualization: Visualization) -> None:
        """Handle deletion of a visualization.

        Args:
            visualization: The visualization to delete
        """
        # Confirm deletion
        result = QMessageBox.question(
            self,
            "Visualisierung löschen",
            f"Möchten Sie die Visualisierung '{visualization.name}' wirklich löschen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if result == QMessageBox.StandardButton.Yes and self.current_data_source:
            # Remove the visualization from the data source
            self.current_data_source.remove_visualization(visualization.id)

            # Notify that the project has changed
            if self.current_project:
                from datetime import datetime
                self.current_project.modified = datetime.now()
                self.current_project.notify_observers()

            # Update the visualization view
            self.visualization_view.update_visualizations_list()

            # Clear the visualization display if the deleted visualization was being displayed
            if (hasattr(self, 'visualization_display') and
                hasattr(self.visualization_display, 'current_visualization') and
                self.visualization_display.current_visualization and
                self.visualization_display.current_visualization.id == visualization.id):
                self.visualization_display.clear()

    def on_create_visualization(self) -> None:
        """Handle creating a new visualization."""
        # Check if we have a data source selected
        if not self.current_data_source or not self.current_project:
            _ = QMessageBox.warning(
                self,
                "Keine Datenquelle ausgewählt",
                "Bitte wählen Sie zuerst eine Datenquelle aus, um eine Visualisierung zu erstellen."
            )
            return

        # Check if the data source has a dataset
        if not self.current_data_source.dataset:
            _ = QMessageBox.warning(
                self,
                "Kein Datensatz vorhanden",
                "Die ausgewählte Datenquelle enthält keinen Datensatz. "
                "Bitte importieren Sie zuerst Daten."
            )
            return

        # Create and show the visualization dialog
        try:
            import logging
            logger = logging.getLogger(__name__)

            logger.info("Erstelle Visualisierungsdialog für Datenquelle: %s", self.current_data_source.name)
            dialog = VisualizationCreationDialog(self.current_data_source, self)
            result = dialog.exec()

            if result == VisualizationCreationDialog.DialogCode.Accepted:
                # Get the visualization from the dialog
                visualization = dialog.get_visualization()
                logger.info("Visualisierung erstellt: %s", visualization.name)

                # Add the visualization to the data source
                self.current_data_source.add_visualization(visualization)

                # Notify that the project has changed
                if self.current_project:
                    self.current_project.modified = visualization.modified_at
                    self.current_project.notify_observers()

                # Switch to the visualization tab
                self.tab_widget.setCurrentIndex(1)

                # Update the visualization list
                self.visualization_view.update_visualizations_list()

                # Display the new visualization
                self.visualization_display.display_visualization(visualization, self.current_data_source)

                # Show success message
                _ = QMessageBox.information(
                    self,
                    "Visualisierung erstellt",
                    f"Die Visualisierung '{visualization.name}' wurde erfolgreich erstellt."
                )
        except Exception as e:
            import logging
            import traceback
            logger = logging.getLogger(__name__)

            # Log detailed error information
            logger.error("Fehler beim Erstellen der Visualisierung: %s", str(e))
            logger.error("Traceback: %s", traceback.format_exc())

            # Show error message
            _ = QMessageBox.critical(
                self,
                "Fehler beim Erstellen der Visualisierung",
                f"Bei der Erstellung der Visualisierung ist ein Fehler aufgetreten: {str(e)}"
            )
