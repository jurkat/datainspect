"""Data models for the application."""
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, TypeVar, Iterable, override, SupportsIndex
from pathlib import Path
import pandas as pd
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
class DataSource:
    """Represents a data source."""
    name: str
    source_type: str
    file_path: Path
    created_at: datetime

@dataclass
class Dataset:
    """Represents a processed dataset."""
    name: str
    data: pd.DataFrame
    metadata: dict[str, Any]
    created_at: datetime
    modified_at: datetime

@dataclass
class Visualization:
    """Represents a visualization configuration."""
    name: str
    chart_type: str
    config: dict[str, Any]
    created_at: datetime
    modified_at: datetime

@dataclass
class Project(Observable):
    """Represents a project in the application."""
    name: str
    created: datetime
    modified: datetime
    data_sources: list[DataSource]
    datasets: list[Dataset]
    visualizations: list[Visualization]
    file_path: Path | None = None
    _last_saved_state: dict[str, Any] | None = None  # For tracking changes
    _collections_modified: bool = False  # Additional flag to track collection modifications

    def __post_init__(self) -> None:
        """Initialize the Observable parent class and setup collection tracking."""
        Observable.__init__(self)

        # Replace the default lists with custom tracking lists
        self.data_sources = _TrackingList(self.data_sources, self._on_collection_modified)
        self.datasets = _TrackingList(self.datasets, self._on_collection_modified)
        self.visualizations = _TrackingList(self.visualizations, self._on_collection_modified)

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
        saved_datasets = self._last_saved_state.get('datasets', [])
        saved_visualizations = self._last_saved_state.get('visualizations', [])

        # If the lists are different lengths, something has changed
        if len(self.data_sources) != len(saved_data_sources):
            return True

        if len(self.datasets) != len(saved_datasets):
            return True

        if len(self.visualizations) != len(saved_visualizations):
            return True

        # Direct modification to the data_sources list is tracked by _collections_modified,
        # which we checked earlier. Simple length comparison is sufficient for the remaining
        # checks

        return False

    def mark_as_saved(self, state: dict[str, Any]) -> None:
        """Mark the current state as saved."""
        self._last_saved_state = state
        self._collections_modified = False

    def add_data_source(self, data_source: 'DataSource') -> None:
        """Add a data source to the project.

        Args:
            data_source: The data source to add
        """
        self.data_sources.append(data_source)
        self.modified = datetime.now()
        self.notify_observers(event="data_source_added", data_source=data_source)

    def remove_data_source(self, data_source: 'DataSource') -> None:
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

    def get_saved_state(self) -> dict[str, Any] | None:
        """Get the last saved state of the project.

        Returns:
            The last saved state or None if the project has never been saved
        """
        return self._last_saved_state

    def set_saved_state(self, state: dict[str, Any]) -> None:
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
