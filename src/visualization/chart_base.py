"""Base classes for chart visualization in DataInspect application."""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, cast, Tuple
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from PyQt6.QtCore import QByteArray

from src.data.models import Dataset


class ChartBase(ABC):
    """Base class for all chart types."""

    def __init__(self, dataset: Dataset, config: Dict[str, Any]) -> None:
        """Initialize the chart.

        Args:
            dataset: The dataset to visualize
            config: Configuration for the chart
        """
        self.dataset = dataset
        self.config = config
        self.figure: Optional[Figure] = None

    def render(self) -> Figure:
        """Render the chart and return the figure.

        This is a template method that defines the skeleton of the rendering algorithm.
        Subclasses should override the specific steps.

        Returns:
            The rendered matplotlib figure
        """
        # Get data
        _ = self.get_data()

        # Create figure
        fig, ax = self.create_figure()

        try:
            # Render the specific chart type
            self.render_chart(ax)

            # Set common properties
            self.set_common_properties(ax)
        except Exception as e:
            # Handle error
            self.handle_error(ax, str(e))

        # Adjust layout
        plt.tight_layout()

        self.figure = fig
        return fig

    def create_figure(self) -> Tuple[Figure, Axes]:
        """Create a figure and axes for the chart.

        Returns:
            A tuple containing the figure and axes
        """
        return plt.subplots(figsize=(10, 6))

    def set_common_properties(self, ax: Axes) -> None:
        """Set common properties for the chart.

        Args:
            ax: The axes to set properties on
        """
        # Set labels and title
        _ = ax.set_xlabel(self.get_x_label())
        _ = ax.set_ylabel(self.get_y_label())
        _ = ax.set_title(self.get_title())

        # Set y-axis to start at 0 for most chart types
        if self.__class__.__name__ not in ['PieChart', 'HeatmapChart']:
            _ = ax.set_ylim(bottom=0)

    def handle_error(self, ax: Axes, error_message: str) -> None:
        """Handle an error during chart rendering.

        Args:
            ax: The axes to show the error on
            error_message: The error message to display
        """
        _ = ax.text(0.5, 0.5, f"Fehler: {error_message}",
               horizontalalignment='center',
               verticalalignment='center',
               transform=ax.transAxes)

    @abstractmethod
    def render_chart(self, ax: Axes) -> None:
        """Render the specific chart type.

        Args:
            ax: The axes to render the chart on
        """

    def get_data(self) -> pd.DataFrame:
        """Get the data for the chart based on configuration.

        Returns:
            DataFrame with the data for the chart
        """
        # Start with the full dataset
        data = self.dataset.data

        # Apply filters if specified
        if 'filter' in self.config and self.config['filter']:
            data = self.apply_filters(data)

        # Apply aggregation if specified
        if 'aggregation' in self.config and self.config['aggregation']:
            # TODO: Implement aggregation
            pass

        # Log the data shape for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"Chart data shape: {data.shape}")

        return data

    def apply_filters(self, data: pd.DataFrame) -> pd.DataFrame:
        """Apply filters to the data.

        Args:
            data: The DataFrame to filter

        Returns:
            Filtered DataFrame
        """
        import logging
        import numpy as np
        logger = logging.getLogger(__name__)
        filtered_data = data.copy()

        try:
            # Apply column filters
            if 'columns' in self.config['filter'] and self.config['filter']['columns']:
                column_filters = self.config['filter']['columns']

                if not column_filters:
                    return filtered_data

                # Erstelle eine Maske für jeden Filter
                filter_masks = []

                for i, filter_config in enumerate(column_filters):
                    column = filter_config.get('column', '')
                    if not column or column not in filtered_data.columns:
                        continue

                    filter_type = filter_config.get('type', '')
                    operator = filter_config.get('operator', '')
                    value = filter_config.get('value')
                    value2 = filter_config.get('value2')
                    logic = filter_config.get('logic', 'and')  # Standard ist UND

                    # Erstelle eine temporäre Kopie für diesen Filter
                    temp_data = filtered_data.copy()

                    # Wende den Filter an
                    if filter_type == 'text':
                        temp_filtered = self._apply_text_filter(temp_data, column, operator, value)
                    elif filter_type == 'numeric':
                        temp_filtered = self._apply_numeric_filter(temp_data, column, operator, value, value2)
                    elif filter_type == 'date':
                        temp_filtered = self._apply_date_filter(temp_data, column, operator, value, value2)
                    elif filter_type == 'year':
                        temp_filtered = self._apply_year_filter(temp_data, column, operator, value, value2)
                    else:
                        # Unbekannter Filtertyp, überspringe
                        continue

                    # Erstelle eine Maske für diesen Filter
                    # Wir identifizieren die Zeilen, die nach dem Filter übrig bleiben
                    if len(temp_filtered) > 0:
                        # Erstelle einen eindeutigen Index für die Identifizierung der Zeilen
                        if not filtered_data.index.is_unique:
                            # Wenn der Index nicht eindeutig ist, erstelle einen temporären
                            temp_index = np.arange(len(filtered_data))
                            filtered_data = filtered_data.reset_index(drop=True)
                            filtered_data.index = temp_index
                            temp_filtered = temp_filtered.reset_index(drop=True)
                            temp_filtered.index = temp_filtered.index.values

                        # Erstelle die Maske basierend auf dem Index
                        mask = pd.Series(filtered_data.index.isin(temp_filtered.index), index=filtered_data.index)
                    else:
                        # Wenn keine Zeilen übrig bleiben, erstelle eine leere Maske
                        mask = pd.Series(False, index=filtered_data.index)

                    # Füge die Maske zur Liste hinzu
                    filter_masks.append((mask, logic))

                # Kombiniere alle Masken basierend auf ihrer Logik
                if filter_masks:
                    # Starte mit der ersten Maske
                    final_mask = filter_masks[0][0]

                    # Kombiniere mit den restlichen Masken
                    for i in range(1, len(filter_masks)):
                        mask, logic = filter_masks[i]
                        if logic == 'and':
                            final_mask = final_mask & mask
                        else:  # 'or'
                            final_mask = final_mask | mask

                    # Wende die kombinierte Maske an und stelle sicher, dass wir ein DataFrame zurückgeben
                    result = filtered_data[final_mask]
                    if isinstance(result, pd.DataFrame):
                        filtered_data = result
                    else:
                        # Wenn wir eine Series oder etwas anderes bekommen, konvertiere es zu einem DataFrame
                        filtered_data = pd.DataFrame(result)

            logger.debug(f"Filtered data shape: {filtered_data.shape}")
        except Exception as e:
            logger.error(f"Error applying filters: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")

        return filtered_data

    def _filter_dataframe(self, data: pd.DataFrame, mask: Any) -> pd.DataFrame:
        """Filter a DataFrame using a boolean mask.

        Args:
            data: The DataFrame to filter
            mask: Boolean mask to use as filter (can be Series, DataFrame, or array-like)

        Returns:
            Filtered DataFrame
        """
        import pandas as pd

        # Ensure we have a valid mask
        if mask is None:
            return data

        # Apply the mask and ensure we return a DataFrame
        try:
            filtered = data[mask]
            # Ensure we return a DataFrame
            if isinstance(filtered, pd.DataFrame):
                return filtered
            elif isinstance(filtered, pd.Series):
                # If we got a Series, convert it back to DataFrame
                return pd.DataFrame(filtered).reset_index(drop=True)
            else:
                # For any other type, try to convert to DataFrame
                return pd.DataFrame(filtered)
        except Exception:
            # If filtering fails, return the original data
            import logging
            logger = logging.getLogger(__name__)
            logger.warning("Failed to apply filter mask, returning original data")
            return data

    def _apply_text_filter(self, data: pd.DataFrame, column: str, operator: str, value: str) -> pd.DataFrame:
        """Apply text filter to the data.

        Args:
            data: The DataFrame to filter
            column: The column to filter on
            operator: The filter operator
            value: The filter value

        Returns:
            Filtered DataFrame
        """
        if not value:
            return data

        try:
            if operator == 'contains':
                mask = data[column].astype(str).str.contains(value, na=False, case=False)
                return self._filter_dataframe(data, mask)
            elif operator == 'equals':
                mask = data[column].astype(str).str.lower() == value.lower()
                return self._filter_dataframe(data, mask)
            elif operator == 'starts_with':
                mask = data[column].astype(str).str.startswith(value, na=False)
                return self._filter_dataframe(data, mask)
            elif operator == 'ends_with':
                mask = data[column].astype(str).str.endswith(value, na=False)
                return self._filter_dataframe(data, mask)
            elif operator == 'specific_values':
                # Für "Bestimmte Werte anzeigen"
                values = [v.strip() for v in value.split(',')]
                mask = data[column].astype(str).isin(values)
                return self._filter_dataframe(data, mask)


        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Error applying text filter: {str(e)}")

        return data

    def _apply_numeric_filter(self, data: pd.DataFrame, column: str, operator: str,
                             value: Any, value2: Optional[Any] = None) -> pd.DataFrame:
        """Apply numeric filter to the data.

        Args:
            data: The DataFrame to filter
            column: The column to filter on
            operator: The filter operator
            value: The filter value
            value2: The second filter value (for between operator)

        Returns:
            Filtered DataFrame
        """
        try:
            # Convert values to float
            num_value = float(value) if value is not None else None
            num_value2 = float(value2) if value2 is not None else None

            if operator == 'equals' and num_value is not None:
                mask = data[column] == num_value
                return self._filter_dataframe(data, mask)
            elif operator == 'greater_than' and num_value is not None:
                mask = data[column] > num_value
                return self._filter_dataframe(data, mask)
            elif operator == 'less_than' and num_value is not None:
                mask = data[column] < num_value
                return self._filter_dataframe(data, mask)
            elif operator == 'between' and num_value is not None and num_value2 is not None:
                mask = (data[column] >= num_value) & (data[column] <= num_value2)
                return self._filter_dataframe(data, mask)
            elif operator == 'divisible_by' and num_value is not None and num_value != 0:
                mask = data[column] % num_value == 0
                return self._filter_dataframe(data, mask)
            elif operator == 'every_nth' and num_value is not None and num_value > 0:
                # Für "Jeden n-ten Wert"
                n = int(num_value)
                # Erstelle einen Index für jede n-te Zeile
                indices = list(range(0, len(data), n))
                return data.iloc[indices].copy()
            elif operator == 'first_n' and num_value is not None and num_value > 0:
                # Für "Erste n Werte"
                n = int(num_value)
                return data.head(n).copy()
            elif operator == 'last_n' and num_value is not None and num_value > 0:
                # Für "Letzte n Werte"
                n = int(num_value)
                return data.tail(n).copy()
        except (ValueError, TypeError):
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Invalid numeric filter values: {value}, {value2}")
        return data

    def _apply_date_filter(self, data: pd.DataFrame, column: str, operator: str,
                          value: Any, value2: Optional[Any] = None) -> pd.DataFrame:
        """Apply date filter to the data.

        Args:
            data: The DataFrame to filter
            column: The column to filter on
            operator: The filter operator
            value: The filter value
            value2: The second filter value (for between operator)

        Returns:
            Filtered DataFrame
        """
        import pandas as pd
        import logging
        logger = logging.getLogger(__name__)

        try:
            # Convert values to datetime
            date_value = pd.to_datetime(value) if value else None
            date_value2 = pd.to_datetime(value2) if value2 else None

            if operator == 'equals' and date_value is not None:
                mask = data[column] == date_value
                return self._filter_dataframe(data, mask)
            elif operator == 'after' and date_value is not None:
                mask = data[column] > date_value
                return self._filter_dataframe(data, mask)
            elif operator == 'before' and date_value is not None:
                mask = data[column] < date_value
                return self._filter_dataframe(data, mask)
            elif operator == 'between' and date_value is not None and date_value2 is not None:
                mask = (data[column] >= date_value) & (data[column] <= date_value2)
                return self._filter_dataframe(data, mask)
        except Exception as e:
            logger.warning(f"Error applying date filter: {str(e)}")
        return data

    def _apply_year_filter(self, data: pd.DataFrame, column: str, operator: str,
                          value: Any, value2: Optional[Any] = None) -> pd.DataFrame:
        """Apply year filter to the data.

        Args:
            data: The DataFrame to filter
            column: The column to filter on
            operator: The filter operator
            value: The filter value
            value2: The second filter value (for between operator)

        Returns:
            Filtered DataFrame
        """
        import logging
        logger = logging.getLogger(__name__)

        try:
            # Convert values to int
            year_value = int(value) if value is not None else None
            year_value2 = int(value2) if value2 is not None else None

            if operator == 'equals' and year_value is not None:
                mask = data[column] == year_value
                return self._filter_dataframe(data, mask)
            elif operator == 'greater_than' and year_value is not None:
                mask = data[column] > year_value
                return self._filter_dataframe(data, mask)
            elif operator == 'less_than' and year_value is not None:
                mask = data[column] < year_value
                return self._filter_dataframe(data, mask)
            elif operator == 'between' and year_value is not None and year_value2 is not None:
                mask = (data[column] >= year_value) & (data[column] <= year_value2)
                return self._filter_dataframe(data, mask)
            elif operator == 'first_n' and year_value is not None:
                sorted_years = sorted(data[column].unique())
                if len(sorted_years) > 0:
                    first_n_years = sorted_years[:year_value]
                    mask = data[column].isin(first_n_years)
                    return self._filter_dataframe(data, mask)
            elif operator == 'last_n' and year_value is not None:
                sorted_years = sorted(data[column].unique())
                if len(sorted_years) > 0:
                    last_n_years = sorted_years[-year_value:]
                    mask = data[column].isin(last_n_years)
                    return self._filter_dataframe(data, mask)
        except (ValueError, TypeError):
            logger.warning(f"Invalid year filter values: {value}, {value2}")
        return data

    def _apply_x_axis_filter(self, data: pd.DataFrame, x_axis: str, x_filter: Dict[str, Any]) -> pd.DataFrame:
        """Apply X-axis filter to the data.

        Args:
            data: The DataFrame to filter
            x_axis: The X-axis column
            x_filter: The X-axis filter configuration

        Returns:
            Filtered DataFrame
        """
        import logging
        logger = logging.getLogger(__name__)

        filter_type = x_filter.get('type', '')
        value = x_filter.get('value')

        try:
            if filter_type == 'every_nth' and value:
                # Convert value to int
                n = int(value)
                if n <= 0:
                    return data

                # Get unique values of x_axis
                unique_values = sorted(data[x_axis].unique())
                # Select every nth value
                selected_values = unique_values[::n]
                # Filter data to only include rows with these x values
                mask = data[x_axis].isin(selected_values)
                return self._filter_dataframe(data, mask)
            elif filter_type == 'specific_values' and value:
                # Convert comma-separated string to list
                if isinstance(value, str):
                    values = [v.strip() for v in value.split(',')]
                    # Try to convert to appropriate type
                    try:
                        # Check if values are numeric
                        numeric_values = [float(v) for v in values]
                        mask = data[x_axis].isin(numeric_values)
                        return self._filter_dataframe(data, mask)
                    except ValueError:
                        # If not numeric, use as strings
                        mask = data[x_axis].astype(str).isin(values)
                        return self._filter_dataframe(data, mask)
                elif isinstance(value, list):
                    mask = data[x_axis].isin(value)
                    return self._filter_dataframe(data, mask)
            elif filter_type == 'first_n' and value:
                # Convert value to int
                n = int(value)
                if n <= 0:
                    return data

                # Get unique values of x_axis
                unique_values = sorted(data[x_axis].unique())
                # Select first n values
                selected_values = unique_values[:n]
                # Filter data to only include rows with these x values
                mask = data[x_axis].isin(selected_values)
                return self._filter_dataframe(data, mask)
            elif filter_type == 'last_n' and value:
                # Convert value to int
                n = int(value)
                if n <= 0:
                    return data

                # Get unique values of x_axis
                unique_values = sorted(data[x_axis].unique())
                # Select last n values
                selected_values = unique_values[-n:]
                # Filter data to only include rows with these x values
                mask = data[x_axis].isin(selected_values)
                return self._filter_dataframe(data, mask)
        except Exception as e:
            logger.error(f"Error applying X-axis filter: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")

        return data

    def get_x_data(self) -> pd.Series:
        """Get the x-axis data.

        Returns:
            Series with the x-axis data
        """
        data = self.get_data()
        x_axis = self.config.get('x_axis', '')
        if not x_axis or x_axis not in data.columns:
            raise ValueError(f"X-Achse '{x_axis}' nicht im Datensatz gefunden")
        result = data[x_axis]
        if isinstance(result, pd.Series):
            return result
        raise ValueError(f"X-Achse '{x_axis}' liefert keine Series zurück")

    def get_y_data(self, y_axis_config: Dict[str, Any]) -> pd.Series:
        """Get the y-axis data for a specific y-axis configuration.

        Args:
            y_axis_config: Configuration for the y-axis

        Returns:
            Series with the y-axis data
        """
        data = self.get_data()
        y_column = y_axis_config.get('column', '')
        if not y_column or y_column not in data.columns:
            raise ValueError(f"Y-Achse '{y_column}' nicht im Datensatz gefunden")
        result = data[y_column]
        if isinstance(result, pd.Series):
            return result
        raise ValueError(f"Y-Achse '{y_column}' liefert keine Series zurück")

    def get_title(self) -> str:
        """Get the chart title.

        Returns:
            The chart title
        """
        return self.config.get('name', 'Visualisierung')

    def get_x_label(self) -> str:
        """Get the x-axis label.

        Returns:
            The x-axis label
        """
        return self.config.get('x_axis', '')

    def get_y_label(self) -> str:
        """Get the y-axis label.

        Returns:
            The y-axis label
        """
        y_axes = self.config.get('y_axes', [])
        if not y_axes:
            return ''

        # If there's only one y-axis, use its column name
        if len(y_axes) == 1:
            return cast(Dict[str, Any], y_axes[0]).get('column', '')

        # If there are multiple y-axes, return a generic label
        return 'Werte'

    def get_colors(self) -> List[str]:
        """Get the colors for the chart.

        Returns:
            List of color hex codes
        """
        y_axes = self.config.get('y_axes', [])
        colors = []

        for y_axis in y_axes:
            y_axis_dict = cast(Dict[str, Any], y_axis)
            color = y_axis_dict.get('color', '#3D78D6')  # Default to blue
            colors.append(color)

        # If no colors are specified, use default colors
        if not colors:
            colors = ['#3D78D6']  # Default blue

        return colors

    def to_image_data(self) -> QByteArray:
        """Convert the figure to image data.

        Returns:
            QByteArray containing the PNG image data
        """
        from io import BytesIO
        from PyQt6.QtCore import QByteArray

        if not self.figure:
            self.figure = self.render()

        buffer = BytesIO()
        self.figure.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        _ = buffer.seek(0)

        return QByteArray(buffer.getvalue())
