"""Implementation of different chart types for DataInspect application."""
from typing import Dict, Any, cast
from typing_extensions import override
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from src.visualization.chart_base import ChartBase


class BarChart(ChartBase):
    """Bar chart implementation."""

    @override
    def render_chart(self, ax: Axes) -> None:
        """Render the bar chart.

        Args:
            ax: The axes to render the chart on
        """
        x_data = self.get_x_data()
        y_axes = self.config.get('y_axes', [])
        colors = self.get_colors()

        # Set up bar positions
        x_pos = np.arange(len(x_data))
        width = 0.8 / len(y_axes) if y_axes else 0.8

        # Plot each y-axis as a set of bars
        for i, y_axis_config in enumerate(y_axes):
            y_axis_dict = cast(Dict[str, Any], y_axis_config)
            y_data = self.get_y_data(y_axis_dict)
            label = y_axis_dict.get('column', f'Reihe {i+1}')
            color = colors[i] if i < len(colors) else '#3D78D6'

            # Calculate bar positions
            bar_pos = x_pos - 0.4 + (i + 0.5) * width

            # Create bars
            _ = ax.bar(bar_pos, y_data, width=width, label=label, color=color, alpha=0.8)

        # Set x-axis ticks
        _ = ax.set_xticks(x_pos)
        _ = ax.set_xticklabels(x_data, rotation=45, ha='right')

        # Add legend if there are multiple y-axes
        if len(y_axes) > 1:
            _ = ax.legend()


class LineChart(ChartBase):
    """Line chart implementation."""

    @override
    def render_chart(self, ax: Axes) -> None:
        """Render the line chart.

        Args:
            ax: The axes to render the chart on
        """
        x_data = self.get_x_data()
        y_axes = self.config.get('y_axes', [])
        colors = self.get_colors()

        # Plot each y-axis as a line
        for i, y_axis_config in enumerate(y_axes):
            y_axis_dict = cast(Dict[str, Any], y_axis_config)
            y_data = self.get_y_data(y_axis_dict)
            label = y_axis_dict.get('column', f'Reihe {i+1}')
            color = colors[i] if i < len(colors) else '#3D78D6'

            # Create line
            _ = ax.plot(x_data, y_data, label=label, color=color, marker='o', markersize=4)

        # Add grid
        _ = ax.grid(True, linestyle='--', alpha=0.7)

        # Add legend if there are multiple y-axes
        if len(y_axes) > 1:
            _ = ax.legend()


class PieChart(ChartBase):
    """Pie chart implementation."""

    @override
    def create_figure(self):
        """Create a figure and axes for the pie chart.

        Returns:
            A tuple containing the figure and axes
        """
        return plt.subplots(figsize=(8, 8))

    @override
    def render_chart(self, ax: Axes) -> None:
        """Render the pie chart.

        Args:
            ax: The axes to render the chart on
        """
        x_data = self.get_x_data()
        y_axes = self.config.get('y_axes', [])

        # For pie chart, we only use the first y-axis
        if not y_axes:
            raise ValueError("Keine Y-Achse für das Kreisdiagramm angegeben")

        y_axis_dict = cast(Dict[str, Any], y_axes[0])
        y_data = self.get_y_data(y_axis_dict)

        # Create pie chart
        # Convert Series to list of strings for labels
        labels = [str(x) for x in x_data.tolist()] if hasattr(x_data, 'tolist') else [str(x) for x in x_data]

        result = ax.pie(
            y_data,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        )

        # Unpack the result
        wedges, texts = result[:2]
        autotexts = result[2] if len(result) > 2 else []

        # Make text more readable
        for text in texts:
            _ = text.set_fontsize(9)
        for autotext in autotexts:
            _ = autotext.set_fontsize(9)
            _ = autotext.set_color('white')

        # Equal aspect ratio ensures that pie is drawn as a circle
        _ = ax.set_aspect('equal')


class ScatterChart(ChartBase):
    """Scatter chart implementation."""

    @override
    def render_chart(self, ax: Axes) -> None:
        """Render the scatter chart.

        Args:
            ax: The axes to render the chart on
        """
        x_data = self.get_x_data()
        y_axes = self.config.get('y_axes', [])
        colors = self.get_colors()

        # For scatter plot, we only use the first y-axis
        if not y_axes:
            raise ValueError("Keine Y-Achse für das Streudiagramm angegeben")

        y_axis_dict = cast(Dict[str, Any], y_axes[0])
        y_data = self.get_y_data(y_axis_dict)
        color = colors[0] if colors else '#3D78D6'

        # Create scatter plot
        _ = ax.scatter(x_data, y_data, color=color, alpha=0.7, s=50)

        # Add grid
        _ = ax.grid(True, linestyle='--', alpha=0.3)


class HeatmapChart(ChartBase):
    """Heatmap chart implementation."""

    @override
    def create_figure(self):
        """Create a figure and axes for the heatmap.

        Returns:
            A tuple containing the figure and axes
        """
        return plt.subplots(figsize=(10, 8))

    @override
    def render_chart(self, ax: Axes) -> None:
        """Render the heatmap.

        Args:
            ax: The axes to render the chart on
        """
        data = self.get_data()
        y_axes = self.config.get('y_axes', [])

        # For heatmap, we need both x-axis and y-axis to be categorical
        if not y_axes:
            raise ValueError("Keine Y-Achse für die Heatmap angegeben")

        y_axis_dict = cast(Dict[str, Any], y_axes[0])
        y_column = y_axis_dict.get('column', '')
        if not y_column or y_column not in data.columns:
            raise ValueError(f"Y-Achse '{y_column}' nicht im Datensatz gefunden")

        # Create pivot table for heatmap
        pivot_data = pd.pivot_table(
            data,
            values=data.select_dtypes(include=[np.number]).columns[0],  # Use first numeric column as values
            index=y_column,
            columns=self.config.get('x_axis', ''),
            aggfunc='mean'
        )

        # Create heatmap
        im = ax.imshow(pivot_data, cmap='viridis')

        # Add colorbar if figure is available
        if ax.figure is not None:
            cbar = ax.figure.colorbar(im, ax=ax)
            _ = cbar.ax.set_ylabel("Werte", rotation=-90, va="bottom")

        # Set ticks and labels
        _ = ax.set_xticks(np.arange(len(pivot_data.columns)))
        _ = ax.set_yticks(np.arange(len(pivot_data.index)))
        _ = ax.set_xticklabels(pivot_data.columns, rotation=45, ha="right")
        _ = ax.set_yticklabels(pivot_data.index)

        # Loop over data dimensions and create text annotations
        for i in range(len(pivot_data.index)):
            for j in range(len(pivot_data.columns)):
                value = pivot_data.iloc[i, j]
                if not pd.isna(value):
                    _ = ax.text(j, i, f"{value:.1f}",
                              ha="center", va="center", color="w")
