"""Widget collection for the DataInspect application."""
from .project_info_widget import ProjectInfoWidget
from .start_screen import StartScreen
from .data_source_view import DataSourceView
from .data_preview import DataPreviewWidget
from .properties_panel import PropertiesPanel
from .main_content import MainContentWidget
from .chart_view import ChartView
from .visualization_view import VisualizationView
from .visualization_display import VisualizationDisplay

__all__ = [
    'ProjectInfoWidget',
    'StartScreen',
    'DataSourceView',
    'DataPreviewWidget',
    'PropertiesPanel',
    'MainContentWidget',
    'ChartView',
    'VisualizationView',
    'VisualizationDisplay'
]
