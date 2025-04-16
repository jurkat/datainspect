"""
Main window module for the DataInspect application.

Provides the main application window with menus and central widget area.
"""

from PyQt6.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QVBoxLayout, 
    QLabel, 
    QStatusBar
)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    """Main window of the application."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DataInspect")
        self.setGeometry(100, 100, 800, 600)
        
        # Setup UI components
        self._setup_menu_bar()
        self._setup_status_bar()
        self._setup_central_widget()
    
    def _setup_menu_bar(self):
        """Setup the application menu bar."""
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("&Datei")
        file_menu.addAction("Öffnen...", self._on_open_file)
        file_menu.addSeparator()
        file_menu.addAction("Beenden", self.close)
        
        # View menu
        view_menu = menu_bar.addMenu("&Ansicht")
        view_menu.addAction("Datenansicht", self._on_toggle_data_view)
        view_menu.addAction("Visualisierungsansicht", self._on_toggle_visualization_view)
    
    def _setup_status_bar(self):
        """Setup the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Bereit")
    
    def _setup_central_widget(self):
        """Setup the central widget of the main window."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        welcome_label = QLabel("Willkommen bei DataInspect - Daten Visualisierung")
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        info_label = QLabel("Bitte öffnen Sie eine Datei, um mit der Analyse zu beginnen.")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addStretch()
        layout.addWidget(welcome_label)
        layout.addWidget(info_label)
        layout.addStretch()
    
    # Event handlers
    def _on_open_file(self):
        """Handle open file action."""
        self.status_bar.showMessage("Datei öffnen...")
        # TODO: Implement file opening functionality
    
    def _on_toggle_data_view(self):
        """Toggle data view."""
        self.status_bar.showMessage("Datenansicht wird angezeigt...")
        # TODO: Implement view toggling
    
    def _on_toggle_visualization_view(self):
        """Toggle visualization view."""
        self.status_bar.showMessage("Visualisierungsansicht wird angezeigt...")
        # TODO: Implement view toggling
