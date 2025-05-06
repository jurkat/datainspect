"""Chart renderer for DataInspect application."""
from typing import Dict, Any, Optional, Type
from matplotlib.figure import Figure

from src.data.models import Dataset, Visualization
from src.visualization.chart_base import ChartBase
from src.visualization.chart_types import (
    BarChart, LineChart, PieChart, ScatterChart, HeatmapChart
)


class ChartRenderer:
    """Handles rendering of charts based on visualization configuration."""

    # Map of chart types to chart classes
    CHART_CLASSES: Dict[str, Type[ChartBase]] = {
        'bar': BarChart,
        'line': LineChart,
        'pie': PieChart,
        'scatter': ScatterChart,
        'heatmap': HeatmapChart
    }

    @classmethod
    def render_chart(cls, dataset: Dataset, visualization: Visualization) -> Optional[Figure]:
        """Render a chart based on visualization configuration.

        Args:
            dataset: The dataset to visualize
            visualization: The visualization configuration

        Returns:
            The rendered matplotlib figure, or None if rendering failed
        """
        try:
            # Get the chart class for the visualization type
            chart_class = cls.CHART_CLASSES.get(visualization.chart_type)
            if not chart_class:
                raise ValueError(f"Unbekannter Diagrammtyp: {visualization.chart_type}")

            # Create and render the chart
            chart = chart_class(dataset, visualization.config)
            figure = chart.render()
            return figure
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Fehler beim Rendern des Diagramms: {str(e)}")
            return None

    @classmethod
    def render_preview(cls, dataset: Dataset, config: Dict[str, Any], chart_type: str) -> Optional[Figure]:
        """Render a preview chart based on configuration.

        Args:
            dataset: The dataset to visualize
            config: The chart configuration
            chart_type: The type of chart to render

        Returns:
            The rendered matplotlib figure, or None if rendering failed
        """
        try:
            # Get the chart class for the visualization type
            chart_class = cls.CHART_CLASSES.get(chart_type)
            if not chart_class:
                raise ValueError(f"Unbekannter Diagrammtyp: {chart_type}")

            # Create and render the chart
            chart = chart_class(dataset, config)
            figure = chart.render()
            return figure
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Fehler beim Rendern der Vorschau: {str(e)}")
            return None
