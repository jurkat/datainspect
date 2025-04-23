"""Data models for the application."""
from dataclasses import dataclass
from datetime import datetime
from typing import List
from pathlib import Path
import pandas as pd

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
    metadata: dict
    created_at: datetime
    modified_at: datetime

@dataclass
class Visualization:
    """Represents a visualization configuration."""
    name: str
    chart_type: str
    config: dict
    created_at: datetime
    modified_at: datetime

@dataclass
class Project:
    """Represents a project in the application."""
    name: str
    created: datetime
    modified: datetime
    data_sources: List[DataSource]
    datasets: List[Dataset]
    visualizations: List[Visualization]
    file_path: Path | None = None
    _last_saved_state: dict | None = None  # For tracking changes
    
    def has_unsaved_changes(self) -> bool:
        """Check if the project has unsaved changes."""
        if self._last_saved_state is None:
            return True
            
        current_state = {
            'name': self.name,
            'modified': self.modified,
            'data_sources': self.data_sources,
            'datasets': self.datasets,
            'visualizations': self.visualizations
        }
        
        return current_state != self._last_saved_state
