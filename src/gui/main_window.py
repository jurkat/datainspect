"""Main window for the DataInspect application.

This module implements the main window of the DataInspect application, which hosts
all the UI components and manages the application state.
"""
from typing import Optional, override
import os
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QSplitter,
    QFileDialog,
    QMessageBox,
    QStackedWidget,
    QDialog,
    QToolBar,
    QStatusBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QKeySequence

from src.data.models import Project, DataSource
from src.data.project_store import ProjectStore
from src.data.importers.csv_importer import CSVImporter
from src.gui.widgets import (
    StartScreen, ProjectInfoWidget, DataSourceView,
    MainContentWidget
)
from src.gui.dialogs.new_project_dialog import NewProjectDialog
from src.gui.dialogs.csv_import_with_transform_dialog import CSVImportDialogWithTransformation
from src.config import (
    PROJECT_FILE_EXTENSION, WINDOW_TITLE,
    WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT,
    WINDOW_PROJECT_WIDTH, LEFT_PANEL_WIDTH,
    UI_COLORS
)
from src.gui.dialogs import RenameProjectDialog  # This class already exists
from src.gui.styles import BASE_STYLE


class MainWindow(QMainWindow):
    """Main window of the DataInspect application."""

    def __init__(self) -> None:
        """Initialize the main window."""
        super().__init__()

        # Window properties
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT)
        self.setMinimumSize(800, 600)  # Minimum window size

        # Apply application-wide style
        self.setStyleSheet(BASE_STYLE)

        # Project management
        self.project_store = ProjectStore()
        self.current_project: Optional[Project] = None
        self.project_actions: list[QAction] = []  # Actions that require an open project

        # Setup UI components
        self._setup_menu()  # Important: Initialize menu before UI setup
        self._setup_toolbar()
        self._setup_statusbar()
        self.setup_ui()
        self.update_actions_state()

    def setup_ui(self) -> None:
        """Set up the user interface."""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create stacked widget
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Create start screen
        self.start_screen = StartScreen(
            on_new_project=self.on_new_project,
            on_open_project=self.on_open_project,
            on_file_dropped=self.on_project_file_dropped
        )

        # Create project view
        self.project_view = QWidget()
        self.project_layout = QVBoxLayout(self.project_view)
        self.project_layout.setContentsMargins(0, 0, 0, 0)
        self.project_layout.setSpacing(0)

        # Create main splitter
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel with project info and data sources
        self.left_panel = QWidget()
        self.left_panel.setFixedWidth(LEFT_PANEL_WIDTH)
        self.left_layout = QVBoxLayout(self.left_panel)
        self.left_layout.setContentsMargins(10, 10, 10, 10)
        self.left_layout.setSpacing(10)

        # Project info widget
        self.project_info = ProjectInfoWidget()
        self.left_layout.addWidget(self.project_info)

        # Data sources view
        self.data_source_view = DataSourceView(
            on_refresh_source=self.on_refresh_data_source,
            on_delete_source=self.on_delete_data_source,
            on_select_source=self.on_select_data_source,
            on_add_source=self.on_add_data_source
        )
        self.left_layout.addWidget(self.data_source_view)

        # Center panel: Main content area
        self.center_panel = QWidget()
        self.center_layout = QVBoxLayout(self.center_panel)
        self.center_layout.setContentsMargins(10, 10, 10, 10)
        self.center_layout.setSpacing(10)

        # Main content widget with tabs
        self.main_content = MainContentWidget()
        self.center_layout.addWidget(self.main_content)

        # Add panels to main splitter
        self.main_splitter.addWidget(self.left_panel)
        self.main_splitter.addWidget(self.center_panel)

        # Set initial sizes for the splitter
        self.main_splitter.setSizes([LEFT_PANEL_WIDTH, 1000])
        self.main_splitter.setCollapsible(0, False)  # Left panel cannot be collapsed

        # Add splitter to project layout
        self.project_layout.addWidget(self.main_splitter)

        # Add widgets to stacked widget
        _ = self.stacked_widget.addWidget(self.start_screen)
        _ = self.stacked_widget.addWidget(self.project_view)

        # Show start screen initially
        self.stacked_widget.setCurrentWidget(self.start_screen)

    def on_new_project(self) -> None:
        """Handle new project button click."""
        # Show dialog to get project name
        dialog = NewProjectDialog(self)
        if dialog.exec() != 1:  # 1 = Accepted, 0 = Rejected
            return

        project_name = dialog.get_project_name()
        if not project_name:
            return

        # Get save location for project file
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Projekt speichern",
            os.path.join(os.path.expanduser("~/Dokumente"), f"{project_name}{PROJECT_FILE_EXTENSION}"),
            f"DataInspect Projekte (*{PROJECT_FILE_EXTENSION})"
        )

        if not file_path:
            return

        try:
            # Create new project
            project = self.project_store.create_new(project_name)
            project.file_path = Path(file_path)
            self.current_project = project

            # Save the new project
            self.project_store.save(project, file_path)

            # Update UI for project view
            self.update_project_view()

            # Switch to project view
            self.stacked_widget.setCurrentWidget(self.project_view)

            # Update menu actions
            self.update_actions_state()

            # Resize window to project size
            self.resize_to_project_size()
        except Exception as e:
            _ = QMessageBox.critical(
                self,
                "Fehler beim Erstellen des Projekts",
                f"Projekt konnte nicht erstellt werden: {str(e)}"
            )

    def on_open_project(self) -> None:
        """Handle open project button click."""
        # Get project file from user
        project_file, _ = QFileDialog.getOpenFileName(
            self,
            "Projekt öffnen",
            os.path.expanduser("~/Dokumente"),
            f"DataInspect Projekte (*{PROJECT_FILE_EXTENSION})"
        )

        if not project_file:
            return

        self.open_project_file(project_file)

    def on_project_file_dropped(self, file_path: str) -> None:
        """Handle project file dropped on start screen.

        Args:
            file_path: Path to the dropped project file
        """
        self.open_project_file(file_path)

    def open_project_file(self, file_path: str) -> None:
        """Open a project file."""
        try:
            # Open project using the ProjectStore
            self.current_project = self.project_store.load(file_path)

            # Update UI for project view
            self.update_project_view()

            # Switch to project view
            self.stacked_widget.setCurrentWidget(self.project_view)

            # Update menu actions
            self.update_actions_state()

            # Resize window to project size
            self.resize_to_project_size()

        except Exception as e:
            _ = QMessageBox.critical(
                self,
                "Fehler beim Öffnen des Projekts",
                f"Projekt konnte nicht geöffnet werden: {str(e)}"
            )

    def resize_to_project_size(self) -> None:
        """Resize the window to the project size."""
        # Resize window to project width with the same aspect ratio
        current_size = self.size()
        aspect_ratio = current_size.width() / current_size.height()
        new_width = WINDOW_PROJECT_WIDTH
        new_height = int(new_width / aspect_ratio)
        self.resize(new_width, new_height)

    def update_project_view(self) -> None:
        """Update the project view with current project data."""
        if not self.current_project:
            return

        # Set the project on widgets that implement the Observer pattern
        self.project_info.update_project(self.current_project)
        self.data_source_view.set_project(self.current_project)

        # The widgets will now observe changes in the project automatically

    def on_add_data_source(self, file_path: str | None = None) -> None:
        """Handle adding a data source.

        Args:
            file_path: Optional path to the data source file.
                       If None or empty string, open a file dialog to select a file.
        """
        if not self.current_project:
            return

        # If no file path provided or empty string, open a file dialog
        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Datenquelle hinzufügen",
                os.path.expanduser("~/Dokumente"),
                "CSV-Dateien (*.csv);;Alle Dateien (*.*)"
            )

            if not file_path:
                return

        try:
            # Get file information
            file_name = os.path.basename(file_path)
            file_ext = os.path.splitext(file_name)[1].lower()

            # Map file extension to data source type
            type_map = {
                '.csv': 'CSV',
                '.xlsx': 'Excel',
                '.xls': 'Excel',
                '.json': 'JSON',
                '.db': 'Database',
                '.sqlite': 'Database'
            }

            source_type = type_map.get(file_ext, 'Unknown')
            file_path_obj = Path(file_path)

            # Handle different file types
            if source_type == 'CSV':
                # Open CSV import dialog with transformation capabilities
                dialog = CSVImportDialogWithTransformation(file_path_obj, self)
                if dialog.exec() != QDialog.DialogCode.Accepted:
                    return

                # Get import options from dialog
                import_options = dialog.get_import_options()

                # Get transformed data if available
                transformed_data = dialog.get_transformed_data()

                # Import CSV file with transformed data if available
                data_source, error = CSVImporter.import_file(
                    file_path_obj,
                    name=import_options['name'],
                    delimiter=import_options['delimiter'],
                    encoding=import_options['encoding'],
                    has_header=import_options['has_header'],
                    skip_rows=import_options['skip_rows'],
                    decimal=import_options['decimal'],
                    thousands=import_options['thousands'],
                    transformed_data=transformed_data
                )

                if error:
                    _ = QMessageBox.critical(self, "Fehler beim Importieren", error)
                    return

                if data_source and data_source.dataset:
                    # Add data source to project
                    self.current_project.add_data_source(data_source)

                    # Show success message
                    _ = QMessageBox.information(
                        self,
                        "CSV-Import erfolgreich",
                        f"Die Datei '{file_name}' wurde erfolgreich importiert.\n"
                        f"Zeilen: {data_source.dataset.metadata.get('rows', 'unbekannt')}\n"
                        f"Spalten: {data_source.dataset.metadata.get('columns', 'unbekannt')}"
                    )
            else:
                # For other file types, just create a basic DataSource object
                data_source = DataSource(
                    name=file_name,
                    source_type=source_type,
                    file_path=file_path_obj,
                    created_at=datetime.now()
                )

                # Add to project
                self.current_project.add_data_source(data_source)

                # Show message that actual import is not yet implemented
                _ = QMessageBox.information(
                    self,
                    "Datenquelle hinzugefügt",
                    f"Die Datenquelle '{file_name}' wurde hinzugefügt.\n"
                    f"Hinweis: Der Import von {source_type}-Dateien ist noch nicht vollständig implementiert."
                )

            # Save project
            if self.current_project.file_path is not None:
                self.project_store.save(self.current_project, self.current_project.file_path)
        except Exception as e:
            _ = QMessageBox.critical(
                self,
                "Fehler beim Hinzufügen der Datenquelle",
                f"Datenquelle konnte nicht hinzugefügt werden: {str(e)}"
            )

    def on_data_source_selected(self, data_source: DataSource) -> None:
        """Handle data source selection.

        Args:
            data_source: The selected data source
        """
        # This would be implemented in Phase 2
        # For now, just show a message box
        _ = QMessageBox.information(
            self,
            "Datenquelle ausgewählt",
            f"Ausgewählte Datenquelle: {data_source.name}\n"
            f"Typ: {data_source.source_type}\n"
            f"Speicherort: {data_source.file_path}"
        )

    def on_refresh_data_source(self, data_source: DataSource) -> None:
        """Handle refreshing a data source.

        Args:
            data_source: The data source to refresh
        """
        if not self.current_project:
            return

        try:
            # In a real implementation, you would reload the data from the source
            _ = QMessageBox.information(
                self,
                "Datenquelle aktualisieren",
                f"Aktualisiere Datenquelle: {data_source.name}"
            )

            # Save project
            if self.current_project.file_path is not None:
                self.project_store.save(self.current_project, self.current_project.file_path)
        except Exception as e:
            _ = QMessageBox.critical(
                self,
                "Fehler beim Aktualisieren der Datenquelle",
                f"Datenquelle konnte nicht aktualisiert werden: {str(e)}"
            )

    def on_delete_data_source(self, data_source: DataSource) -> None:
        """Handle deleting a data source.

        Args:
            data_source: The data source to delete
        """
        if not self.current_project:
            return

        # Confirm with the user
        reply = QMessageBox.question(
            self,
            "Datenquelle löschen",
            f"Sind Sie sicher, dass Sie die Datenquelle '{data_source.name}' löschen möchten?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            # Remove from project
            self.current_project.remove_data_source(data_source)

            # Update project view
            self.update_project_view()

            # Save project
            if self.current_project.file_path is not None:
                self.project_store.save(self.current_project, self.current_project.file_path)
        except Exception as e:
            _ = QMessageBox.critical(
                self,
                "Fehler beim Löschen der Datenquelle",
                f"Datenquelle konnte nicht gelöscht werden: {str(e)}"
            )

    def on_select_data_source(self, data_source: DataSource) -> None:
        """Handle selecting a data source.

        Args:
            data_source: The selected data source
        """
        if not self.current_project:
            return

        # Update the main content widget with the selected data source
        self.main_content.set_data_source(data_source, self.current_project)

        # Update status bar
        status_bar = self.statusBar()
        if status_bar:
            status_bar.showMessage(f"Datenquelle '{data_source.name}' ausgewählt")

    def _setup_menu(self):
        """Setup the menu bar."""
        menubar = self.menuBar()
        if menubar is None:
            return  # No menu bar available

        # File menu
        file_menu = menubar.addMenu("&Datei")
        if file_menu is None:
            return  # Could not create menu

        new_action = QAction("&Neues Projekt...", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        _ = new_action.triggered.connect(self.on_new_project)
        _ = file_menu.addAction(new_action)

        open_action = QAction("Projekt &öffnen...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        _ = open_action.triggered.connect(self.on_open_project)
        _ = file_menu.addAction(open_action)

        _ = file_menu.addSeparator()

        close_action = QAction("Projekt &schließen", self)
        close_action.setShortcut(QKeySequence.StandardKey.Close)
        _ = close_action.triggered.connect(self.close_project)
        _ = file_menu.addAction(close_action)
        self.project_actions.append(close_action)

        _ = file_menu.addSeparator()

        rename_action = QAction("Projekt &umbenennen...", self)
        _ = rename_action.triggered.connect(self.rename_project)
        _ = file_menu.addAction(rename_action)
        self.project_actions.append(rename_action)

        _ = file_menu.addSeparator()

        save_action = QAction("Projekt &speichern", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        _ = save_action.triggered.connect(self.save_project)
        _ = file_menu.addAction(save_action)
        self.project_actions.append(save_action)

        save_as_action = QAction("Projekt speichern &unter...", self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        _ = save_as_action.triggered.connect(self.save_project_as)
        _ = file_menu.addAction(save_as_action)
        self.project_actions.append(save_as_action)

        _ = file_menu.addSeparator()

        exit_action = QAction("&Beenden", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        _ = exit_action.triggered.connect(self.close)
        _ = file_menu.addAction(exit_action)

    def _setup_toolbar(self) -> None:
        """Set up the toolbar."""
        toolbar = QToolBar("Hauptwerkzeugleiste")
        toolbar.setMovable(False)
        # Verwende direkt QSize statt Qt.SizeHint.size
        from PyQt6.QtCore import QSize
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        # Add actions to toolbar
        new_action = QAction("Neues Projekt", self)
        new_action.setStatusTip("Erstellt ein neues Projekt")
        _ = new_action.triggered.connect(self.on_new_project)
        _ = toolbar.addAction(new_action)

        open_action = QAction("Projekt öffnen", self)
        open_action.setStatusTip("Öffnet ein bestehendes Projekt")
        _ = open_action.triggered.connect(self.on_open_project)
        _ = toolbar.addAction(open_action)

        _ = toolbar.addSeparator()

        add_source_action = QAction("Datenquelle hinzufügen", self)
        add_source_action.setStatusTip("Fügt eine neue Datenquelle zum Projekt hinzu")
        # Use empty string instead of None
        _ = add_source_action.triggered.connect(lambda: self.on_add_data_source(""))
        _ = toolbar.addAction(add_source_action)
        self.project_actions.append(add_source_action)

        self.addToolBar(toolbar)

    def _setup_statusbar(self) -> None:
        """Set up the status bar."""
        status_bar = QStatusBar()
        status_bar.setStyleSheet(f"""
            QStatusBar {{
                background-color: {UI_COLORS['background_lighter']};
                color: {UI_COLORS['foreground']};
                border-top: 1px solid {UI_COLORS['border']};
            }}
        """)
        self.setStatusBar(status_bar)

        # Add permanent widgets to status bar
        status_bar.showMessage("Bereit")

    def update_actions_state(self):
        """Update the enabled state of actions based on whether a project is open."""
        has_project = self.current_project is not None
        for action in self.project_actions:
            action.setEnabled(has_project)

        # Update window title to show project name
        if has_project and self.current_project is not None:
            self.setWindowTitle(f"DataInspect - {self.current_project.name}")
            status_bar = self.statusBar()
            if status_bar:
                status_bar.showMessage(f"Projekt '{self.current_project.name}' geöffnet")
        else:
            self.setWindowTitle("DataInspect")
            status_bar = self.statusBar()
            if status_bar:
                status_bar.showMessage("Bereit")

    def close_project(self):
        """Close the current project."""
        if not self.current_project:
            return

        # Ask for confirmation if project has unsaved changes
        if self.current_project.has_unsaved_changes():
            reply = QMessageBox.question(
                self,
                "Projekt schließen",
                "Möchten Sie die Änderungen vor dem Schließen speichern?",
                QMessageBox.StandardButton.Save |
                QMessageBox.StandardButton.Discard |
                QMessageBox.StandardButton.Cancel
            )

            if reply == QMessageBox.StandardButton.Save:
                if not self.save_project():  # If save was cancelled or failed
                    return
            elif reply == QMessageBox.StandardButton.Cancel:
                return

        self.current_project = None
        self.update_actions_state()
        self.stacked_widget.setCurrentWidget(self.start_screen)

        # Reset window size to default when project is closed
        self.resize(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT)

    def save_project(self) -> bool:
        """Save the current project.

        Returns:
            bool: True if project was saved successfully, False otherwise
        """
        if not self.current_project:
            _ = QMessageBox.warning(self, "Warnung", "Kein Projekt ist derzeit geöffnet")
            return False

        if self.current_project.file_path is None:
            return self.save_project_as()

        try:
            self.project_store.save(self.current_project, self.current_project.file_path)
            return True
        except Exception as e:
            _ = QMessageBox.critical(self, "Fehler", f"Fehler beim Speichern des Projekts: {str(e)}")
            return False

    def save_project_as(self) -> bool:
        """Save the current project to a new location.

        Returns:
            bool: True if project was saved successfully, False otherwise
        """
        if not self.current_project:
            _ = QMessageBox.warning(self, "Warnung", "Kein Projekt ist derzeit geöffnet")
            return False

        # Use project name as suggested file name
        suggested_name = self.current_project.name + PROJECT_FILE_EXTENSION

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Projekt speichern unter",
            os.path.join(os.path.expanduser("~/Dokumente"), suggested_name),
            f"DataInspect Projekte (*{PROJECT_FILE_EXTENSION})"
        )

        if file_path:
            try:
                self.project_store.save(self.current_project, file_path)
                self.current_project.file_path = Path(file_path)
                self.update_actions_state()
                return True
            except Exception as e:
                _ = QMessageBox.critical(self, "Fehler", f"Fehler beim Speichern des Projekts: {str(e)}")

        return False

    def rename_project(self) -> None:
        """Rename the current project."""
        if not self.current_project:
            _ = QMessageBox.warning(self, "Warnung", "Kein Projekt ist derzeit geöffnet")
            return

        dialog = RenameProjectDialog(self.current_project.name, self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        new_name = dialog.get_new_name()
        if not new_name or new_name == self.current_project.name:
            return

        # Store old name before any changes
        old_name = self.current_project.name

        try:
            # Update project name
            self.current_project.name = new_name

            # If project was already saved, we need to save it again
            if self.current_project.file_path:
                _ = self.save_project()

            # Update UI
            self.update_project_view()
            self.update_actions_state()

            _ = QMessageBox.information(
                self,
                "Projekt umbenannt",
                f'Projekt wurde von "{old_name}" zu "{new_name}" umbenannt.'
            )
        except Exception as e:
            _ = QMessageBox.critical(
                self,
                "Fehler beim Umbenennen",
                f"Projekt konnte nicht umbenannt werden: {str(e)}"
            )
            # Restore old name on error
            self.current_project.name = old_name

    @override
    def closeEvent(self, a0) -> None:
        """Handle window close event.

        Args:
            a0: Close event
        """
        # Ensure a0 is not None before using it
        if a0 is None:
            return

        # Rename parameter for internal use
        event = a0
        # Check for unsaved changes
        if self.current_project and self.current_project.has_unsaved_changes():
            reply = QMessageBox.question(
                self,
                "Ungespeicherte Änderungen",
                "Das aktuelle Projekt hat ungespeicherte Änderungen. Vor dem Schließen speichern?",
                QMessageBox.StandardButton.Save |
                QMessageBox.StandardButton.Discard |
                QMessageBox.StandardButton.Cancel
            )

            if reply == QMessageBox.StandardButton.Save:
                try:
                    if self.current_project.file_path is not None:
                        self.project_store.save(self.current_project, self.current_project.file_path)
                    else:
                        # Wenn kein Dateipfad vorhanden ist, verwenden wir save_project_as
                        success = self.save_project_as()
                        if not success:
                            event.ignore()
                            return
                    event.accept()
                except Exception as e:
                    _ = QMessageBox.critical(
                        self,
                        "Fehler beim Speichern des Projekts",
                        f"Fehler beim Speichern des Projekts: {str(e)}"
                    )
                    event.ignore()
            elif reply == QMessageBox.StandardButton.Cancel:
                event.ignore()
            else:
                event.accept()
        else:
            event.accept()
