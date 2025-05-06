"""Tests for chart rendering functionality."""
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from typing import override
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.axes import Axes

from src.data.models import Dataset
from src.visualization.chart_types import (
    BarChart, LineChart, PieChart, ScatterChart, HeatmapChart
)


class TestChartRendering(unittest.TestCase):
    """Test cases for chart rendering functionality."""

    @override
    def setUp(self) -> None:
        """Set up test fixtures."""
        # Create a test dataset with multiple years
        years = list(range(2000, 2005))
        population = [80000000 + i * 100000 for i in range(len(years))]
        gdp = [2000 + i * 100 for i in range(len(years))]

        self.data = pd.DataFrame({
            'Jahr': years,
            'Bevölkerung_Gesamt': population,
            'BIP': gdp
        })

        self.dataset = Dataset(
            data=self.data,
            metadata={"columns": 3, "rows": len(years)},
            created_at=datetime.now(),
            modified_at=datetime.now()
        )

        # Create a basic visualization configuration
        self.config = {
            "name": "Test-Visualisierung",
            "x_axis": "Jahr",
            "y_axes": [{"column": "Bevölkerung_Gesamt", "color": "#3D78D6"}]
        }

        # Create a multi-series configuration
        self.multi_config = {
            "name": "Multi-Series-Test",
            "x_axis": "Jahr",
            "y_axes": [
                {"column": "Bevölkerung_Gesamt", "color": "#3D78D6"},
                {"column": "BIP", "color": "#D63D78"}
            ]
        }

    @patch('matplotlib.pyplot.subplots')
    def test_bar_chart_render(self, mock_subplots):
        """Test that BarChart.render calls the correct methods."""
        # Set up mocks
        mock_fig = MagicMock(spec=Figure)
        mock_ax = MagicMock(spec=Axes)
        # Add required attributes for error handling
        mock_ax.transAxes = 'mock_transform'
        mock_ax.figure = mock_fig
        mock_subplots.return_value = (mock_fig, mock_ax)

        # Create chart and call render
        chart = BarChart(self.dataset, self.config)
        result = chart.render()

        # Verify that subplots was called
        mock_subplots.assert_called_once()

        # Verify that the correct methods were called on the axes
        mock_ax.bar.assert_called()
        mock_ax.set_xticks.assert_called()
        mock_ax.set_xticklabels.assert_called()
        mock_ax.set_xlabel.assert_called()
        mock_ax.set_ylabel.assert_called()
        mock_ax.set_title.assert_called()
        mock_ax.set_ylim.assert_called()

        # Verify that the figure was returned
        self.assertEqual(result, mock_fig)

    @patch('matplotlib.pyplot.subplots')
    def test_bar_chart_render_multi_series(self, mock_subplots):
        """Test that BarChart.render handles multiple series correctly."""
        # Set up mocks
        mock_fig = MagicMock(spec=Figure)
        mock_ax = MagicMock(spec=Axes)
        # Add required attributes for error handling
        mock_ax.transAxes = 'mock_transform'
        mock_ax.figure = mock_fig
        mock_subplots.return_value = (mock_fig, mock_ax)

        # Create chart and call render
        chart = BarChart(self.dataset, self.multi_config)
        result = chart.render()

        # Verify that bar was called twice (once for each series)
        self.assertEqual(mock_ax.bar.call_count, 2)

        # Verify that legend was called (for multiple series)
        mock_ax.legend.assert_called_once()

        # Verify that the figure was returned
        self.assertEqual(result, mock_fig)

    @patch('matplotlib.pyplot.subplots')
    def test_line_chart_render(self, mock_subplots):
        """Test that LineChart.render calls the correct methods."""
        # Set up mocks
        mock_fig = MagicMock(spec=Figure)
        mock_ax = MagicMock(spec=Axes)
        # Add required attributes for error handling
        mock_ax.transAxes = 'mock_transform'
        mock_ax.figure = mock_fig
        mock_subplots.return_value = (mock_fig, mock_ax)

        # Create chart and call render
        chart = LineChart(self.dataset, self.config)
        result = chart.render()

        # Verify that subplots was called
        mock_subplots.assert_called_once()

        # Verify that the correct methods were called on the axes
        mock_ax.plot.assert_called()
        mock_ax.grid.assert_called_with(True, linestyle='--', alpha=0.7)
        mock_ax.set_xlabel.assert_called()
        mock_ax.set_ylabel.assert_called()
        mock_ax.set_title.assert_called()
        mock_ax.set_ylim.assert_called()

        # Verify that the figure was returned
        self.assertEqual(result, mock_fig)

    @patch('matplotlib.pyplot.subplots')
    def test_line_chart_render_multi_series(self, mock_subplots):
        """Test that LineChart.render handles multiple series correctly."""
        # Set up mocks
        mock_fig = MagicMock(spec=Figure)
        mock_ax = MagicMock(spec=Axes)
        # Add required attributes for error handling
        mock_ax.transAxes = 'mock_transform'
        mock_ax.figure = mock_fig
        mock_subplots.return_value = (mock_fig, mock_ax)

        # Create chart and call render
        chart = LineChart(self.dataset, self.multi_config)
        result = chart.render()

        # Verify that plot was called twice (once for each series)
        self.assertEqual(mock_ax.plot.call_count, 2)

        # Verify that legend was called (for multiple series)
        mock_ax.legend.assert_called_once()

        # Verify that the figure was returned
        self.assertEqual(result, mock_fig)

    @patch('matplotlib.pyplot.subplots')
    def test_scatter_chart_render(self, mock_subplots):
        """Test that ScatterChart.render calls the correct methods."""
        # Set up mocks
        mock_fig = MagicMock(spec=Figure)
        mock_ax = MagicMock(spec=Axes)
        # Add required attributes for error handling
        mock_ax.transAxes = 'mock_transform'
        mock_ax.figure = mock_fig
        mock_subplots.return_value = (mock_fig, mock_ax)

        # Create chart and call render
        chart = ScatterChart(self.dataset, self.config)
        result = chart.render()

        # Verify that subplots was called
        mock_subplots.assert_called_once()

        # Verify that the correct methods were called on the axes
        mock_ax.scatter.assert_called()
        mock_ax.grid.assert_called_with(True, linestyle='--', alpha=0.3)
        mock_ax.set_xlabel.assert_called()
        mock_ax.set_ylabel.assert_called()
        mock_ax.set_title.assert_called()
        mock_ax.set_ylim.assert_called()

        # Verify that the figure was returned
        self.assertEqual(result, mock_fig)

    @patch('matplotlib.pyplot.subplots')
    def test_pie_chart_render(self, mock_subplots):
        """Test that PieChart.render calls the correct methods."""
        # Set up mocks
        mock_fig = MagicMock(spec=Figure)
        mock_ax = MagicMock(spec=Axes)
        # Add required attributes for error handling
        mock_ax.transAxes = 'mock_transform'
        mock_ax.figure = mock_fig
        mock_subplots.return_value = (mock_fig, mock_ax)

        # Mock the pie method to return a tuple of lists
        mock_wedges = [MagicMock()]
        mock_texts = [MagicMock()]
        mock_autotexts = [MagicMock()]
        mock_ax.pie.return_value = (mock_wedges, mock_texts, mock_autotexts)

        # Create chart and call render
        chart = PieChart(self.dataset, self.config)
        result = chart.render()

        # Verify that subplots was called with the correct figsize
        mock_subplots.assert_called_once()

        # Verify that the correct methods were called on the axes
        mock_ax.pie.assert_called_once()
        mock_ax.set_aspect.assert_called_with('equal')
        mock_ax.set_title.assert_called()

        # Verify that text properties were set
        self.assertTrue(mock_texts[0].set_fontsize.called)
        self.assertTrue(mock_autotexts[0].set_fontsize.called)
        self.assertTrue(mock_autotexts[0].set_color.called)

        # Verify that the figure was returned
        self.assertEqual(result, mock_fig)

    @patch('matplotlib.pyplot.subplots')
    def test_heatmap_chart_render(self, mock_subplots):
        """Test that HeatmapChart.render calls the correct methods."""
        # Set up mocks
        mock_fig = MagicMock(spec=Figure)
        mock_ax = MagicMock(spec=Axes)
        # Add required attributes for error handling
        mock_ax.transAxes = 'mock_transform'
        mock_ax.figure = mock_fig
        mock_subplots.return_value = (mock_fig, mock_ax)

        # Mock the figure's colorbar method
        mock_fig.colorbar = MagicMock()
        mock_colorbar = MagicMock()
        mock_fig.colorbar.return_value = mock_colorbar
        mock_colorbar.ax = MagicMock()

        # Create a special config for heatmap
        heatmap_config = {
            "name": "Heatmap-Test",
            "x_axis": "Jahr",
            "y_axes": [{"column": "BIP"}]
        }

        # Create chart and call render
        chart = HeatmapChart(self.dataset, heatmap_config)
        result = chart.render()

        # Verify that subplots was called with the correct figsize
        mock_subplots.assert_called_once()

        # Verify that the correct methods were called on the axes
        mock_ax.imshow.assert_called_once()
        mock_ax.set_xticks.assert_called()
        mock_ax.set_yticks.assert_called()
        mock_ax.set_xticklabels.assert_called()
        mock_ax.set_yticklabels.assert_called()
        mock_ax.set_title.assert_called()

        # Verify that the figure was returned
        self.assertEqual(result, mock_fig)

    @patch('matplotlib.pyplot.subplots')
    def test_chart_error_handling(self, mock_subplots):
        """Test that charts handle errors gracefully."""
        # Set up mocks
        mock_fig = MagicMock(spec=Figure)
        mock_ax = MagicMock(spec=Axes)
        # Add required attributes for error handling
        mock_ax.transAxes = 'mock_transform'
        mock_ax.figure = mock_fig
        mock_subplots.return_value = (mock_fig, mock_ax)

        # Create a config with an invalid column
        invalid_config = {
            "name": "Invalid-Test",
            "x_axis": "NonExistentColumn",
            "y_axes": [{"column": "Bevölkerung_Gesamt"}]
        }

        # Create chart and call render
        chart = BarChart(self.dataset, invalid_config)
        result = chart.render()

        # Verify that error handling was called
        mock_ax.text.assert_called()  # Error message should be displayed

        # Verify that the figure was still returned
        self.assertEqual(result, mock_fig)


if __name__ == '__main__':
    _ = unittest.main()
