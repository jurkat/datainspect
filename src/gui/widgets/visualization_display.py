"""Visualization display widget for DataInspect application."""
from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt

from src.data.models import DataSource, Visualization
from src.gui.widgets.chart_view import ChartView
from src.config import UI_COLORS


class VisualizationDisplay(QWidget):
    """Widget for displaying a visualization."""

    def __init__(self, parent=None) -> None:
        """Initialize the visualization display.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.current_visualization: Optional[Visualization] = None
        self.current_data_source: Optional[DataSource] = None
        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Header with visualization info
        self.header_widget = QWidget()
        header_layout = QHBoxLayout(self.header_widget)
        header_layout.setContentsMargins(0, 0, 0, 10)

        # Visualization title
        self.title_label = QLabel("Keine Visualisierung ausgewählt")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        header_layout.addWidget(self.title_label, 1)  # Stretch factor 1

        # Export button (placeholder for now)
        self.export_button = QPushButton("Exportieren")
        self.export_button.setToolTip("Visualisierung als Bild exportieren")
        self.export_button.setEnabled(False)
        header_layout.addWidget(self.export_button)

        layout.addWidget(self.header_widget)

        # Chart view
        self.chart_view = ChartView()
        layout.addWidget(self.chart_view, 1)  # Stretch factor 1

        # Placeholder message
        self.placeholder = QLabel("Wählen Sie eine Visualisierung aus der Liste aus")
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder.setStyleSheet(f"color: {UI_COLORS['foreground_dim']}; font-size: 14px;")
        layout.addWidget(self.placeholder)

        # Initially show placeholder
        self.chart_view.setVisible(False)
        self.placeholder.setVisible(True)

    def display_visualization(self, visualization: Visualization, data_source: DataSource) -> None:
        """Display a visualization.

        Args:
            visualization: The visualization to display
            data_source: The data source containing the visualization
        """
        import logging
        logger = logging.getLogger(__name__)

        # Store current visualization and data source
        self.current_visualization = visualization
        self.current_data_source = data_source

        # Update title
        self.title_label.setText(visualization.name)

        # Enable export button
        self.export_button.setEnabled(True)

        # Check if data source has a dataset
        if not data_source.dataset:
            logger.warning("Datenquelle hat keinen Datensatz")
            self.chart_view.setVisible(False)
            self.placeholder.setText("Die Datenquelle enthält keinen Datensatz")
            self.placeholder.setVisible(True)
            return

        try:
            # Display the chart
            logger.info("Zeige Visualisierung an: %s", visualization.name)
            self.chart_view.display_chart(data_source.dataset, visualization)
            
            # Show chart view, hide placeholder
            self.chart_view.setVisible(True)
            self.placeholder.setVisible(False)
        except Exception as e:
            logger.error("Fehler beim Anzeigen der Visualisierung: %s", str(e))
            import traceback
            logger.error("Traceback: %s", traceback.format_exc())
            
            # Show error message
            self.chart_view.setVisible(False)
            self.placeholder.setText(f"Fehler beim Anzeigen der Visualisierung: {str(e)}")
            self.placeholder.setVisible(True)

    def clear(self) -> None:
        """Clear the current visualization."""
        # Reset title
        self.title_label.setText("Keine Visualisierung ausgewählt")
        
        # Disable export button
        self.export_button.setEnabled(False)
        
        # Clear chart view
        self.chart_view.clear_chart()
        
        # Show placeholder
        self.chart_view.setVisible(False)
        self.placeholder.setText("Wählen Sie eine Visualisierung aus der Liste aus")
        self.placeholder.setVisible(True)
        
        # Reset current visualization and data source
        self.current_visualization = None
        self.current_data_source = None
