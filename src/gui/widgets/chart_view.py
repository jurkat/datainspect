"""Chart view widget for DataInspect application."""
from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QByteArray
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from src.data.models import Dataset, Visualization
from src.visualization.chart_renderer import ChartRenderer


class MatplotlibCanvas(FigureCanvas):
    """Matplotlib canvas for displaying charts in Qt."""

    def __init__(self, figure: Figure) -> None:
        """Initialize the canvas with a figure.

        Args:
            figure: The matplotlib figure to display
        """
        super().__init__(figure)
        self.setMinimumSize(400, 300)


class ChartView(QWidget):
    """Widget for displaying charts."""

    def __init__(self, parent=None) -> None:
        """Initialize the chart view.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.figure: Optional[Figure] = None
        self.canvas: Optional[MatplotlibCanvas] = None
        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Placeholder for when no chart is displayed
        self.placeholder = QLabel("Keine Visualisierung ausgewählt")
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder.setStyleSheet("color: #999; font-size: 14px;")
        layout.addWidget(self.placeholder)

    def display_chart(self, dataset: Dataset, visualization: Visualization) -> None:
        """Display a chart based on visualization configuration.

        Args:
            dataset: The dataset to visualize
            visualization: The visualization configuration
        """
        # Clear any existing chart
        self.clear_chart()

        # Log dataset shape for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"Chart dataset shape: {dataset.data.shape}")

        # Render the chart
        self.figure = ChartRenderer.render_chart(dataset, visualization)
        if not self.figure:
            # Show error message if rendering failed
            self.placeholder.setText("Fehler beim Rendern der Visualisierung")
            self.placeholder.setVisible(True)
            return

        # Create canvas for the figure
        self.canvas = MatplotlibCanvas(self.figure)

        # Hide placeholder and add canvas
        self.placeholder.setVisible(False)
        layout = self.layout()
        if layout:
            layout.addWidget(self.canvas)

    def display_preview(self, dataset: Dataset, config: dict, chart_type: str) -> None:
        """Display a preview chart based on configuration.

        Args:
            dataset: The dataset to visualize
            config: The chart configuration
            chart_type: The type of chart to render
        """
        # Clear any existing chart
        self.clear_chart()

        # Log dataset shape for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"Preview dataset shape: {dataset.data.shape}")

        # Render the preview
        self.figure = ChartRenderer.render_preview(dataset, config, chart_type)
        if not self.figure:
            # Show error message if rendering failed
            self.placeholder.setText("Fehler beim Rendern der Vorschau")
            self.placeholder.setVisible(True)
            return

        # Create canvas for the figure
        self.canvas = MatplotlibCanvas(self.figure)

        # Hide placeholder and add canvas
        self.placeholder.setVisible(False)
        layout = self.layout()
        if layout:
            layout.addWidget(self.canvas)

    def clear_chart(self) -> None:
        """Clear the current chart."""
        if self.canvas:
            layout = self.layout()
            if layout:
                layout.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None

        self.figure = None
        self.placeholder.setVisible(True)

    def export_to_image(self) -> Optional[QByteArray]:
        """Export the current chart to a PNG image.

        Returns:
            QByteArray containing the PNG image data, or None if no chart is displayed
        """
        if not self.figure:
            return None

        from io import BytesIO
        from PyQt6.QtCore import QByteArray

        buffer = BytesIO()
        self.figure.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        _ = buffer.seek(0)

        return QByteArray(buffer.getvalue())
