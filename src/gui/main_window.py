"""Main window implementation."""
import logging
from typing import Final, Optional
from PyQt6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QWidget,
    QVBoxLayout,
    QStatusBar,
    QMenu,
    QFileDialog
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from ..config import WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT, WINDOW_TITLE, PROJECT_FILE_EXTENSION
from ..data.project_store import ProjectStore
from ..data.models import Project
from ..exceptions import ProjectError, ProjectNotFoundError
from .dialogs import NewProjectDialog

class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.current_project: Optional[Project] = None
        self.project_actions: list[QAction] = []  # Actions that require an open project
        self.setup_ui()
        self.update_actions_state()
        
    def setup_ui(self):
        """Setup the user interface."""
        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        
        # Setup menu bar
        self._setup_menu()
        
        # Setup status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
    def _setup_menu(self):
        """Setup the menu bar."""
        menubar = self.menuBar()
        if menubar is None:
            self.logger.error("Failed to create menu bar")
            return
            
        # File menu
        file_menu = menubar.addMenu("&File")
        if file_menu is None:
            self.logger.error("Failed to create file menu")
            return
        
        new_action = QAction("&New Project...", self)
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        open_action = QAction("&Open Project...", self)
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        close_action = QAction("&Close Project", self)
        close_action.triggered.connect(self.close_project)
        file_menu.addAction(close_action)
        self.project_actions.append(close_action)
        
        file_menu.addSeparator()
        
        save_action = QAction("&Save Project", self)
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)
        self.project_actions.append(save_action)
        
        save_as_action = QAction("Save Project &As...", self)
        save_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_as_action)
        self.project_actions.append(save_as_action)
        
    def update_actions_state(self):
        """Update the enabled state of actions based on whether a project is open."""
        has_project = self.current_project is not None
        for action in self.project_actions:
            action.setEnabled(has_project)
        
        # Update window title to show project name
        project_name = None
        if self.current_project is not None:
            project_name = getattr(self.current_project, 'name', None)
            
        if project_name is not None:
            self.setWindowTitle(f"{project_name} - {WINDOW_TITLE}")
        else:
            self.setWindowTitle(WINDOW_TITLE)
            
    def new_project(self):
        """Create a new project."""
        dialog = NewProjectDialog(self)
        if dialog.exec():
            name = dialog.get_project_name()
            self.current_project = ProjectStore.create_new(name)
            self.status_bar.showMessage(f"Created new project: {name}")
            self.update_actions_state()
            
    def open_project(self):
        """Open an existing project."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Project",
            "",
            f"DataInspect Projects (*{PROJECT_FILE_EXTENSION})"
        )
        
        if file_path:
            try:
                self.current_project = ProjectStore.load(file_path)
                if self.current_project and self.current_project.name:
                    self.status_bar.showMessage(f"Opened project: {self.current_project.name}")
                else:
                    self.status_bar.showMessage("Opened project")
                self.update_actions_state()
            except (ProjectError, ProjectNotFoundError) as e:
                QMessageBox.critical(self, "Error", str(e))
                
    def close_project(self):
        """Close the current project."""
        if not self.current_project:
            return
            
        # Ask for confirmation if project has unsaved changes
        if self.current_project.has_unsaved_changes():  # You'll need to implement this method
            reply = QMessageBox.question(
                self,
                "Close Project",
                "Do you want to save the changes before closing?",
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
        self.status_bar.showMessage("Project closed")
                
    def save_project(self) -> bool:
        """Save the current project.
        
        Returns:
            bool: True if project was saved successfully, False otherwise
        """
        if not self.current_project:
            QMessageBox.warning(self, "Warning", "No project is currently open")
            return False
            
        if not self.current_project.file_path:
            return self.save_project_as()
            
        try:
            ProjectStore.save(self.current_project, self.current_project.file_path)
            self.status_bar.showMessage("Project saved successfully")
            return True
        except ProjectError as e:
            QMessageBox.critical(self, "Error", str(e))
            return False
                
    def save_project_as(self) -> bool:
        """Save the current project to a new location.
        
        Returns:
            bool: True if project was saved successfully, False otherwise
        """
        if not self.current_project:
            QMessageBox.warning(self, "Warning", "No project is currently open")
            return False
            
        # Use project name as suggested file name
        suggested_name = self.current_project.name + PROJECT_FILE_EXTENSION
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Project As",
            suggested_name,
            f"DataInspect Projects (*{PROJECT_FILE_EXTENSION})"
        )
        
        if file_path:
            try:
                ProjectStore.save(self.current_project, file_path)
                self.status_bar.showMessage("Project saved successfully")
                return True
            except ProjectError as e:
                QMessageBox.critical(self, "Error", str(e))
                
        return False
