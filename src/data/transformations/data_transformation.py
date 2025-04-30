"""
Core functionality for data transformation and cleaning operations.
"""

from enum import Enum, auto
from typing import Any, Callable, TypeVar, cast
import pandas as pd

# Define a type variable for Series
SeriesT = TypeVar('SeriesT', bound=pd.Series)

class TransformationType(Enum):
    """Types of possible data transformations."""
    MISSING_VALUES = auto()
    TYPE_CONVERSION = auto()
    TEXT_OPERATION = auto()
    NUMERIC_OPERATION = auto()
    OUTLIER_HANDLING = auto()


class TransformationOperation(Enum):
    """Available operations for data transformations."""
    # Missing values
    REMOVE_MISSING = auto()
    REPLACE_MEAN = auto()
    REPLACE_MEDIAN = auto()
    REPLACE_MODE = auto()
    REPLACE_CUSTOM = auto()

    # Type conversions
    CONVERT_TO_NUMERIC = auto()
    CONVERT_TO_TEXT = auto()
    CONVERT_TO_DATE = auto()
    CONVERT_TO_CATEGORICAL = auto()

    # Text operations
    TEXT_LOWERCASE = auto()
    TEXT_UPPERCASE = auto()
    TEXT_TRIM = auto()
    TEXT_REPLACE = auto()

    # Numeric operations
    NUMERIC_ROUND = auto()
    NUMERIC_NORMALIZE = auto()
    NUMERIC_STANDARDIZE = auto()
    NUMERIC_LIMIT_RANGE = auto()

    # Outlier handling
    OUTLIER_REMOVE = auto()
    OUTLIER_WINSORIZE = auto()


class DataTransformation:
    """Represents a single data transformation for a column."""

    def __init__(
        self,
        column: str,
        operation: TransformationOperation,
        parameters: dict[str, Any] | None = None
    ) -> None:
        """
        Initializes a new data transformation.

        Parameters
        ----------
        column : str
            Name of the column to transform
        operation : TransformationOperation
            Operation to perform
        parameters : dict[str, Any] | None, optional
            Parameters for the operation, by default None
        """
        self.column = column
        self.operation = operation
        self.parameters = parameters or {}
        self._transformation_function = self._get_transformation_function()

    def _get_transformation_function(self) -> Callable[[pd.Series], pd.Series]:
        """
        Returns the transformation function based on the operation.

        Returns
        -------
        Callable[[pd.Series], pd.Series]
            Function for transforming the data
        """
        # Implementation of a factory for the different transformations

        # Handling missing values
        if self.operation == TransformationOperation.REMOVE_MISSING:
            # Cast is used to specify the return type as pd.Series
            return lambda series: cast(pd.Series, series.dropna())
        elif self.operation == TransformationOperation.REPLACE_MEAN:
            # Lambda with explicit type checking
            def replace_mean(series: pd.Series) -> pd.Series:
                if pd.api.types.is_numeric_dtype(series):
                    return cast(pd.Series, series.fillna(series.mean()))
                return cast(pd.Series, series.fillna(series.iloc[0] if len(series) > 0 else ""))
            return replace_mean
        elif self.operation == TransformationOperation.REPLACE_MEDIAN:
            # Lambda with explicit type checking
            def replace_median(series: pd.Series) -> pd.Series:
                if pd.api.types.is_numeric_dtype(series):
                    return cast(pd.Series, series.fillna(series.median()))
                return cast(pd.Series, series.fillna(series.iloc[0] if len(series) > 0 else ""))
            return replace_median
        elif self.operation == TransformationOperation.REPLACE_MODE:
            # Lambda with explicit type checking
            def replace_mode(series: pd.Series) -> pd.Series:
                if not series.mode().empty:
                    return cast(pd.Series, series.fillna(series.mode().iloc[0]))
                return cast(pd.Series, series.fillna(series.iloc[0] if len(series) > 0 else ""))
            return replace_mode
        elif self.operation == TransformationOperation.REPLACE_CUSTOM:
            value = self.parameters.get('value', '')
            return lambda series: cast(pd.Series, series.fillna(value))

        # Type conversions
        elif self.operation == TransformationOperation.CONVERT_TO_NUMERIC:
            errors = self.parameters.get('errors', 'coerce')  # 'coerce' sets invalid values to NaN
            return lambda series: cast(pd.Series, pd.to_numeric(series, errors=errors))
        elif self.operation == TransformationOperation.CONVERT_TO_TEXT:
            return lambda series: cast(pd.Series, series.astype(str))
        elif self.operation == TransformationOperation.CONVERT_TO_DATE:
            date_format = self.parameters.get('format', None)
            errors = self.parameters.get('errors', 'coerce')
            return lambda series: cast(pd.Series, pd.to_datetime(series, format=date_format, errors=errors))
        elif self.operation == TransformationOperation.CONVERT_TO_CATEGORICAL:
            return lambda series: cast(pd.Series, series.astype('category'))

        # Text operations
        elif self.operation == TransformationOperation.TEXT_LOWERCASE:
            return lambda series: cast(pd.Series, series.str.lower() if hasattr(series, 'str') else series)
        elif self.operation == TransformationOperation.TEXT_UPPERCASE:
            return lambda series: cast(pd.Series, series.str.upper() if hasattr(series, 'str') else series)
        elif self.operation == TransformationOperation.TEXT_TRIM:
            return lambda series: cast(pd.Series, series.str.strip() if hasattr(series, 'str') else series)
        elif self.operation == TransformationOperation.TEXT_REPLACE:
            pattern = self.parameters.get('pattern', '')
            replacement = self.parameters.get('replacement', '')
            return lambda series: cast(pd.Series, series.str.replace(pattern, replacement, regex=True) if hasattr(series, 'str') else series)

        # Numeric operations
        elif self.operation == TransformationOperation.NUMERIC_ROUND:
            decimals = self.parameters.get('decimals', 0)
            return lambda series: cast(pd.Series, series.round(decimals) if pd.api.types.is_numeric_dtype(series) else series)
        elif self.operation == TransformationOperation.NUMERIC_NORMALIZE:
            # Min-Max Normalization: (x - min) / (max - min)
            return lambda series: cast(pd.Series, (series - series.min()) / (series.max() - series.min()) if pd.api.types.is_numeric_dtype(series) else series)
        elif self.operation == TransformationOperation.NUMERIC_STANDARDIZE:
            # Z-Score Standardization: (x - mean) / std
            return lambda series: cast(pd.Series, (series - series.mean()) / series.std() if pd.api.types.is_numeric_dtype(series) else series)
        elif self.operation == TransformationOperation.NUMERIC_LIMIT_RANGE:
            min_val = self.parameters.get('min', None)
            max_val = self.parameters.get('max', None)

            def limit_range(series: pd.Series) -> pd.Series:
                if pd.api.types.is_numeric_dtype(series):
                    result = series.clip(lower=min_val, upper=max_val)
                    # Explicit type handling to avoid downcasting
                    return cast(pd.Series, result)
                return series

            return limit_range

        # Outlier handling
        elif self.operation == TransformationOperation.OUTLIER_REMOVE:
            threshold = self.parameters.get('threshold', 3.0)  # Standard deviations
            return lambda series: cast(pd.Series, series.mask(
                abs(series - series.mean()) > threshold * series.std(),
                None
            ) if pd.api.types.is_numeric_dtype(series) else series)
        elif self.operation == TransformationOperation.OUTLIER_WINSORIZE:
            lower = self.parameters.get('lower', 0.05)  # Lower percentile
            upper = self.parameters.get('upper', 0.95)  # Upper percentile

            def winsorize(series: pd.Series) -> pd.Series:
                if pd.api.types.is_numeric_dtype(series):
                    lower_val = series.quantile(lower)
                    upper_val = series.quantile(upper)

                    # Set the option to change the downcasting behavior
                    pd.set_option('future.no_silent_downcasting', True)
                    try:
                        result = series.clip(lower=lower_val, upper=upper_val)
                        # Ensure that the data type is preserved
                        if result.dtype != series.dtype:
                            result = result.astype(series.dtype)
                        return cast(pd.Series, result)
                    finally:
                        # Reset the option
                        pd.set_option('future.no_silent_downcasting', False)
                return series

            return winsorize

        # Default behavior: Identity function
        return lambda series: cast(pd.Series, series)

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies the transformation to the DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            Input DataFrame

        Returns
        -------
        pd.DataFrame
            Transformed DataFrame
        """
        result_df = df.copy()
        if self.column in result_df.columns:
            # Explicitly treat the column as a Series
            try:
                # Explicitly handle the type and only process pd.Series
                series = result_df[self.column].copy()
                # Only if it's actually a Series
                if isinstance(series, pd.Series):
                    transformed_series = self._transformation_function(series)
                    # Copy the result back to the DataFrame
                    result_df[self.column] = transformed_series
            except Exception as e:
                # In case of error, keep the original data
                print(f"Error transforming {self.column}: {e}")
        return result_df

    def get_description(self) -> str:
        """
        Creates a user-friendly description of the transformation.

        Returns
        -------
        str
            Description of the transformation
        """
        op_name = self.operation.name.replace('_', ' ').title()
        params_str = ', '.join(f"{k}={v}" for k, v in self.parameters.items())
        return f"{op_name} on '{self.column}'" + (f" ({params_str})" if params_str else "")


class DataFrameTransformer:
    """Manages all transformations for a DataFrame."""

    def __init__(self) -> None:
        """Initializes a new DataFrame transformer."""
        self.transformations: list[DataTransformation] = []

    def add_transformation(self, transformation: DataTransformation) -> None:
        """
        Adds a new transformation.

        Parameters
        ----------
        transformation : DataTransformation
            Transformation to add
        """
        self.transformations.append(transformation)

    def remove_transformation(self, index: int) -> None:
        """
        Removes a transformation by its index.

        Parameters
        ----------
        index : int
            Index of the transformation to remove
        """
        if 0 <= index < len(self.transformations):
            _ = self.transformations.pop(index)

    def clear_transformations(self) -> None:
        """Removes all transformations."""
        self.transformations.clear()

    def apply_all(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies all transformations to the DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            Input DataFrame

        Returns
        -------
        pd.DataFrame
            Transformed DataFrame
        """
        result_df = df.copy()
        for transformation in self.transformations:
            result_df = transformation.apply(result_df)
        return result_df

    def get_transformation_descriptions(self) -> list[str]:
        """
        Returns a list of all transformations as strings for the UI.

        Returns
        -------
        list[str]
            List of string representations of the transformations
        """
        return [t.get_description() for t in self.transformations]
