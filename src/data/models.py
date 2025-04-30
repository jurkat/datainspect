"""Data models for the application."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, TypeVar, Iterable, override, SupportsIndex, Optional, List, Dict
from pathlib import Path
import pandas as pd
import uuid
from ..utils.observer import Observable


T = TypeVar('T')


class _TrackingList(list[T]):
    """A list subclass that tracks modifications and calls a callback when modified."""

    def __init__(self, initial_items: Iterable[T], callback: Callable[[], None]) -> None:
        super().__init__(initial_items)
        self._callback = callback

    @override
    def __setitem__(self, key: SupportsIndex | slice, value: Any) -> None:
        super().__setitem__(key, value)
        self._callback()

    @override
    def __delitem__(self, key: SupportsIndex | slice) -> None:
        super().__delitem__(key)
        self._callback()

    @override
    def append(self, item: T) -> None:
        super().append(item)
        self._callback()

    @override
    def extend(self, iterable: Iterable[T]) -> None:
        super().extend(iterable)
        self._callback()

    @override
    def insert(self, index: SupportsIndex, item: T) -> None:
        super().insert(index, item)
        self._callback()

    @override
    def remove(self, item: T) -> None:
        super().remove(item)
        self._callback()

    @override
    def pop(self, index: SupportsIndex = -1) -> T:
        item = super().pop(index)
        self._callback()
        return item

    @override
    def clear(self) -> None:
        super().clear()
        self._callback()


@dataclass
class Column:
    """Represents a single column/variable in a Dataset."""
    name: str
    data_type: str  # e.g. 'numeric', 'text', 'date', 'categorical'
    original_type: str  # The original pandas data type
    stats: Dict[str, Any] = field(default_factory=dict)  # Statistical metrics
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional metadata

    @classmethod
    def from_series(cls, name: str, series: pd.Series) -> 'Column':
        """
        Creates a Column instance from a pandas Series.

        Parameters
        ----------
        name : str
            Name of the column
        series : pd.Series
            The column data

        Returns
        -------
        Column
            A new Column instance
        """
        # Determine data type
        if pd.api.types.is_numeric_dtype(series):
            data_type = 'numeric'
        elif pd.api.types.is_datetime64_dtype(series):
            data_type = 'date'
        elif isinstance(series.dtype, pd.CategoricalDtype):
            data_type = 'categorical'
        else:
            data_type = 'text'

        # Calculate statistical metrics
        stats = {}
        stats['count'] = series.count()
        stats['null_count'] = series.isna().sum()
        stats['unique_count'] = series.nunique()

        if data_type == 'numeric':
            # Check if the series is not empty before calculating statistics
            if not series.empty and series.notna().any():
                min_val = series.min()
                max_val = series.max()
                mean_val = series.mean()
                median_val = series.median()
                std_val = series.std()

                # Use isinstance to check if the value is a scalar
                # and then pd.isna() for null check
                stats['min'] = None if isinstance(min_val, float) and pd.isna(min_val) else min_val
                stats['max'] = None if isinstance(max_val, float) and pd.isna(max_val) else max_val
                stats['mean'] = None if isinstance(mean_val, float) and pd.isna(mean_val) else mean_val
                stats['median'] = None if isinstance(median_val, float) and pd.isna(median_val) else median_val
                stats['std'] = None if isinstance(std_val, float) and pd.isna(std_val) else std_val
            else:
                # Set default values for empty series
                stats['min'] = None
                stats['max'] = None
                stats['mean'] = None
                stats['median'] = None
                stats['std'] = None

        return cls(
            name=name,
            data_type=data_type,
            original_type=str(series.dtype),
            stats=stats,
            metadata={}
        )

    def get_summary(self) -> Dict[str, Any]:
        """
        Provides a summary of the column.

        Returns
        -------
        Dict[str, Any]
            Summary with type, statistics and metadata
        """
        return {
            'name': self.name,
            'data_type': self.data_type,
            'original_type': self.original_type,
            'stats': self.stats,
            'metadata': self.metadata
        }

@dataclass
class Dataset:
    """Represents a processed dataset."""
    data: pd.DataFrame
    metadata: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    columns: List[Column] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Initialize columns from DataFrame if not provided."""
        if not self.columns and not self.data.empty:
            self._initialize_columns()

    def _initialize_columns(self) -> None:
        """Initialize Column objects from DataFrame."""
        self.columns = []
        for col_name in self.data.columns:
            series = self.data[col_name]
            if isinstance(series, pd.Series):
                column = Column.from_series(col_name, series)
                self.columns.append(column)

    def get_preview(self, rows: int = 10) -> pd.DataFrame:
        """
        Provides a preview of the data.

        Parameters
        ----------
        rows : int, optional
            Number of rows in the preview, by default 10

        Returns
        -------
        pd.DataFrame
            DataFrame with the first `rows` rows
        """
        return self.data.head(rows)

    def get_column_types(self) -> Dict[str, str]:
        """
        Returns the data types of all columns.

        Returns
        -------
        Dict[str, str]
            Dictionary with column names as keys and data types as values
        """
        if self.columns:
            return {col.name: col.original_type for col in self.columns}
        return {col: str(dtype) for col, dtype in self.data.dtypes.items()}

    def get_column_by_name(self, name: str) -> Optional[Column]:
        """
        Returns a Column instance for the specified column name.

        Parameters
        ----------
        name : str
            Name of the column

        Returns
        -------
        Optional[Column]
            Column instance or None if the column does not exist
        """
        for column in self.columns:
            if column.name == name:
                return column
        return None

    def generate_metadata(self, source_info: Dict[str, Any] | None = None) -> None:
        """
        Generates metadata for the Dataset based on the data and optional source information.

        Parameters
        ----------
        source_info : Dict[str, Any] | None, optional
            Additional information about the data source, by default None
        """
        metadata = {
            "rows": len(self.data),
            "columns": len(self.data.columns),
            "column_types": self.get_column_types()
        }

        # Add source information if available
        if source_info is not None:
            metadata.update(source_info)

        self.metadata = metadata
        self.modified_at = datetime.now()

    def to_json(self) -> Dict[str, Any]:
        """
        Converts the Dataset to a JSON-serializable dictionary.

        Returns
        -------
        Dict[str, Any]
            JSON-serializable dictionary
        """
        columns_data = []
        for column in self.columns:
            # Convert NumPy data types to Python standard types
            stats = {}
            for key, value in column.stats.items():
                # Convert NumPy types to Python standard types
                if hasattr(value, 'item') and callable(getattr(value, 'item')):
                    stats[key] = value.item()
                else:
                    stats[key] = value

            columns_data.append({
                "name": column.name,
                "data_type": column.data_type,
                "original_type": column.original_type,
                "stats": stats,
                "metadata": column.metadata
            })

        return {
            "data": self.data.to_json(),
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
            "columns": columns_data
        }

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> 'Dataset':
        """
        Creates a Dataset from a JSON dictionary.

        Parameters
        ----------
        json_data : Dict[str, Any]
            JSON dictionary with Dataset data

        Returns
        -------
        Dataset
            New Dataset object
        """
        from io import StringIO

        # Create DataFrame from JSON
        df = pd.read_json(StringIO(json_data["data"]))

        # Restore data types from metadata if available
        if "metadata" in json_data and "column_types" in json_data["metadata"]:
            column_types = json_data["metadata"]["column_types"]
            for col, dtype in column_types.items():
                if col in df.columns:
                    # Try to restore the original data type
                    try:
                        if 'float' in dtype.lower():
                            df[col] = df[col].astype('float64')
                        elif 'int' in dtype.lower():
                            df[col] = df[col].astype('int64')
                        elif 'datetime' in dtype.lower():
                            df[col] = pd.to_datetime(df[col])
                        # Other types (object, etc.) remain unchanged
                    except (ValueError, TypeError):
                        # Leave the type unchanged in case of error
                        pass

        # Create Dataset
        dataset = cls(
            data=df,
            metadata=json_data["metadata"],
            created_at=datetime.fromisoformat(json_data["created_at"]),
            modified_at=datetime.fromisoformat(json_data["modified_at"])
        )

        # Create Columns from JSON if available
        if "columns" in json_data:
            dataset.columns = []
            for col_data in json_data["columns"]:
                column = Column(
                    name=col_data["name"],
                    data_type=col_data["data_type"],
                    original_type=col_data["original_type"],
                    stats=col_data["stats"],
                    metadata=col_data["metadata"]
                )
                dataset.columns.append(column)
        else:
            # Create Columns from DataFrame
            dataset._initialize_columns()

        return dataset


@dataclass
class Visualization:
    """Represents a visualization configuration."""
    name: str
    chart_type: str
    config: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class DataSource:
    """Represents a data source."""
    name: str
    source_type: str
    file_path: Path
    created_at: datetime = field(default_factory=datetime.now)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    dataset: Optional[Dataset] = None
    visualizations: List[Visualization] = field(default_factory=list)

    def add_visualization(self, visualization: Visualization) -> None:
        """Add a visualization to the data source."""
        self.visualizations.append(visualization)

    def remove_visualization(self, visualization_id: str) -> None:
        """Remove a visualization from the data source."""
        self.visualizations = [v for v in self.visualizations if v.id != visualization_id]

    def get_visualization_by_id(self, visualization_id: str) -> Optional[Visualization]:
        """Get a visualization by its ID."""
        for vis in self.visualizations:
            if vis.id == visualization_id:
                return vis
        return None


@dataclass
class Project(Observable):
    """Represents a project in the application."""
    name: str
    created: datetime
    modified: datetime
    data_sources: List[DataSource]
    file_path: Optional[Path] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    _last_saved_state: Dict[str, Any] | None = None  # For tracking changes
    _collections_modified: bool = False  # Additional flag to track collection modifications

    def __post_init__(self) -> None:
        """Initialize the Observable parent class and setup collection tracking."""
        Observable.__init__(self)

        # Replace the default lists with custom tracking lists
        self.data_sources = _TrackingList(self.data_sources, self._on_collection_modified)

    def _on_collection_modified(self) -> None:
        """Called when any collection is modified."""
        self._collections_modified = True
        self.modified = datetime.now()

    def has_unsaved_changes(self) -> bool:
        """Check if the project has unsaved changes."""
        if self._last_saved_state is None:
            return True

        # Check if collections have been modified
        if self._collections_modified:
            return True

        # Check basic attributes first
        if self.name != self._last_saved_state.get('name'):
            return True

        # Modified time is expected to change during saves

        # Check if collections themselves have changed in length
        saved_data_sources = self._last_saved_state.get('data_sources', [])

        # If the lists are different lengths, something has changed
        if len(self.data_sources) != len(saved_data_sources):
            return True

        # Direct modification to the data_sources list is tracked by _collections_modified,
        # which we checked earlier. Simple length comparison is sufficient for the remaining
        # checks

        return False

    def mark_as_saved(self, state: Dict[str, Any]) -> None:
        """Mark the current state as saved."""
        self._last_saved_state = state
        self._collections_modified = False

    def add_data_source(self, data_source: DataSource) -> None:
        """Add a data source to the project.

        Args:
            data_source: The data source to add
        """
        self.data_sources.append(data_source)
        self.modified = datetime.now()
        self.notify_observers(event="data_source_added", data_source=data_source)

    def remove_data_source(self, data_source: DataSource) -> None:
        """Remove a data source from the project.

        Args:
            data_source: The data source to remove
        """
        if data_source in self.data_sources:
            self.data_sources.remove(data_source)
            self.modified = datetime.now()
            self.notify_observers(event="data_source_removed", data_source=data_source)

    def rename(self, new_name: str) -> None:
        """Rename the project.

        Args:
            new_name: The new name for the project
        """
        old_name = self.name
        self.name = new_name
        self.modified = datetime.now()
        self.notify_observers(event="renamed", old_name=old_name, new_name=new_name)

    def get_saved_state(self) -> Dict[str, Any] | None:
        """Get the last saved state of the project.

        Returns:
            The last saved state or None if the project has never been saved
        """
        return self._last_saved_state

    def set_saved_state(self, state: Dict[str, Any]) -> None:
        """Set the last saved state of the project.

        Args:
            state: The state to set as the last saved state
        """
        self._last_saved_state = state

    def set_collections_modified(self, modified: bool) -> None:
        """Set the collections modified flag.

        Args:
            modified: Whether the collections have been modified
        """
        self._collections_modified = modified

    def get_data_source_by_id(self, data_source_id: str) -> Optional[DataSource]:
        """Get a data source by its ID.

        Args:
            data_source_id: The ID of the data source to find

        Returns:
            The data source with the given ID, or None if not found
        """
        for ds in self.data_sources:
            if ds.id == data_source_id:
                return ds
        return None

    def get_visualization_by_id(self, visualization_id: str) -> Optional[Visualization]:
        """Get a visualization by its ID.

        Args:
            visualization_id: The ID of the visualization to find

        Returns:
            The visualization with the given ID, or None if not found
        """
        for ds in self.data_sources:
            for vis in ds.visualizations:
                if vis.id == visualization_id:
                    return vis
        return None
