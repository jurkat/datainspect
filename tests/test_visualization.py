"""Tests for visualization functionality."""
import unittest
from datetime import datetime
from typing import override
import pandas as pd
from src.data.models import Dataset, Visualization
from src.visualization.chart_types import BarChart, LineChart, ScatterChart, PieChart


class TestVisualization(unittest.TestCase):
    """Test cases for visualization functionality."""

    @override
    def setUp(self) -> None:
        """Set up test fixtures."""
        # Create a test dataset with multiple years
        years = list(range(2000, 2025))
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
            "y_axes": [{"column": "Bevölkerung_Gesamt"}]
        }

        self.visualization = Visualization(
            name="Test-Visualisierung",
            chart_type="bar",
            config=self.config,
            created_at=datetime.now(),
            modified_at=datetime.now()
        )

    def test_bar_chart_get_data(self):
        """Test that BarChart.get_data returns the full dataset."""
        chart = BarChart(self.dataset, self.visualization.config)
        data = chart.get_data()

        # Check that the data has the correct shape
        self.assertEqual(data.shape, self.data.shape)

        # Check that the data contains all years
        self.assertEqual(len(data['Jahr'].unique()), 25)

        # Check that the first and last years are correct
        self.assertEqual(data['Jahr'].min(), 2000)
        self.assertEqual(data['Jahr'].max(), 2024)

    def test_bar_chart_get_x_data(self):
        """Test that BarChart.get_x_data returns the full x-axis data."""
        chart = BarChart(self.dataset, self.visualization.config)
        x_data = chart.get_x_data()

        # Check that the data has the correct length
        self.assertEqual(len(x_data), 25)

        # Check that the first and last years are correct
        self.assertEqual(x_data.iloc[0], 2000)
        self.assertEqual(x_data.iloc[-1], 2024)

    def test_bar_chart_get_y_data(self):
        """Test that BarChart.get_y_data returns the full y-axis data."""
        chart = BarChart(self.dataset, self.visualization.config)
        y_axis_config = self.visualization.config['y_axes'][0]
        y_data = chart.get_y_data(y_axis_config)

        # Check that the data has the correct length
        self.assertEqual(len(y_data), 25)

        # Check that the first and last values are correct
        self.assertEqual(y_data.iloc[0], 80000000)
        self.assertEqual(y_data.iloc[-1], 82400000)

    def test_line_chart_get_data(self):
        """Test that LineChart.get_data returns the full dataset."""
        chart = LineChart(self.dataset, self.visualization.config)
        data = chart.get_data()

        # Check that the data has the correct shape
        self.assertEqual(data.shape, self.data.shape)

        # Check that the data contains all years
        self.assertEqual(len(data['Jahr'].unique()), 25)

        # Check that the first and last years are correct
        self.assertEqual(data['Jahr'].min(), 2000)
        self.assertEqual(data['Jahr'].max(), 2024)

    def test_line_chart_get_x_data(self):
        """Test that LineChart.get_x_data returns the full x-axis data."""
        chart = LineChart(self.dataset, self.visualization.config)
        x_data = chart.get_x_data()

        # Check that the data has the correct length
        self.assertEqual(len(x_data), 25)

        # Check that the first and last years are correct
        self.assertEqual(x_data.iloc[0], 2000)
        self.assertEqual(x_data.iloc[-1], 2024)

    def test_line_chart_get_y_data(self):
        """Test that LineChart.get_y_data returns the full y-axis data."""
        chart = LineChart(self.dataset, self.visualization.config)
        y_axis_config = self.visualization.config['y_axes'][0]
        y_data = chart.get_y_data(y_axis_config)

        # Check that the data has the correct length
        self.assertEqual(len(y_data), 25)

        # Check that the first and last values are correct
        self.assertEqual(y_data.iloc[0], 80000000)
        self.assertEqual(y_data.iloc[-1], 82400000)

    def test_scatter_chart_get_data(self):
        """Test that ScatterChart.get_data returns the full dataset."""
        chart = ScatterChart(self.dataset, self.visualization.config)
        data = chart.get_data()

        # Check that the data has the correct shape
        self.assertEqual(data.shape, self.data.shape)

        # Check that the data contains all years
        self.assertEqual(len(data['Jahr'].unique()), 25)

        # Check that the first and last years are correct
        self.assertEqual(data['Jahr'].min(), 2000)
        self.assertEqual(data['Jahr'].max(), 2024)

    def test_scatter_chart_get_x_data(self):
        """Test that ScatterChart.get_x_data returns the full x-axis data."""
        chart = ScatterChart(self.dataset, self.visualization.config)
        x_data = chart.get_x_data()

        # Check that the data has the correct length
        self.assertEqual(len(x_data), 25)

        # Check that the first and last years are correct
        self.assertEqual(x_data.iloc[0], 2000)
        self.assertEqual(x_data.iloc[-1], 2024)

    def test_scatter_chart_get_y_data(self):
        """Test that ScatterChart.get_y_data returns the full y-axis data."""
        chart = ScatterChart(self.dataset, self.visualization.config)
        y_axis_config = self.visualization.config['y_axes'][0]
        y_data = chart.get_y_data(y_axis_config)

        # Check that the data has the correct length
        self.assertEqual(len(y_data), 25)

        # Check that the first and last values are correct
        self.assertEqual(y_data.iloc[0], 80000000)
        self.assertEqual(y_data.iloc[-1], 82400000)

    def test_pie_chart_get_data(self):
        """Test that PieChart.get_data returns the full dataset."""
        # Pie chart needs a specific configuration
        pie_config = {
            "name": "Test-Pie-Chart",
            "x_axis": "Jahr",
            "y_axes": [{"column": "Bevölkerung_Gesamt"}]
        }

        chart = PieChart(self.dataset, pie_config)
        data = chart.get_data()

        # Check that the data has the correct shape
        self.assertEqual(data.shape, self.data.shape)

        # Check that the data contains all years
        self.assertEqual(len(data['Jahr'].unique()), 25)

        # Check that the first and last years are correct
        self.assertEqual(data['Jahr'].min(), 2000)
        self.assertEqual(data['Jahr'].max(), 2024)


if __name__ == '__main__':
    _ = unittest.main()
