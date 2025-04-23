"""Project storage handling module."""

import json
import logging
from pathlib import Path
from datetime import datetime
import pandas as pd
from typing import Dict, Any
from .models import Project, DataSource, Dataset, Visualization
from ..exceptions import ProjectError, ProjectNotFoundError
from ..config import PROJECT_FILE_EXTENSION

logger = logging.getLogger(__name__)

class ProjectStore:
    """Handles project file storage and loading."""
    
    @staticmethod
    def save(project: Project, file_path: Path | str) -> None:
        """
        Save project to a .dinsp file at the specified location.
        
        Args:
            project: Project to save
            file_path: Where to save the project file (user-specified)
        """
        file_path = Path(file_path)
        logger.info(f"Saving project to: {file_path}")
        
        # Ensure correct file extension
        if not str(file_path).endswith(PROJECT_FILE_EXTENSION):
            file_path = Path(str(file_path) + PROJECT_FILE_EXTENSION)
            
        # Create project directory if it doesn't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Prepare project data for serialization
        project_data = {
            "name": project.name,
            "created": project.created.isoformat(),
            "modified": datetime.now().isoformat(),
            "data_sources": [
                {
                    "name": ds.name,
                    "source_type": ds.source_type,
                    "file_path": str(ds.file_path),
                    "created_at": ds.created_at.isoformat()
                }
                for ds in project.data_sources
            ],
            "datasets": [
                {
                    "name": ds.name,
                    "data": ds.data.to_json(),
                    "metadata": ds.metadata,
                    "created_at": ds.created_at.isoformat(),
                    "modified_at": ds.modified_at.isoformat()
                }
                for ds in project.datasets
            ],
            "visualizations": [
                {
                    "name": v.name,
                    "chart_type": v.chart_type,
                    "config": v.config,
                    "created_at": v.created_at.isoformat(),
                    "modified_at": v.modified_at.isoformat()
                }
                for v in project.visualizations
            ]
        }
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, indent=2)
            project.file_path = file_path
            logger.debug(f"Project saved successfully to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save project: {e}")
            raise ProjectError(f"Failed to save project: {str(e)}")

        # After successful save, update the saved state
        project._last_saved_state = {
            'name': project.name,
            'modified': project.modified,
            'data_sources': project.data_sources,
            'datasets': project.datasets,
            'visualizations': project.visualizations
        }

    @staticmethod
    def load(file_path: Path | str) -> Project:
        """
        Load project from a .dinsp file.
        
        Args:
            file_path: Path to the project file (user-specified)
        """
        file_path = Path(file_path)
        logger.info(f"Loading project from: {file_path}")
        
        if not file_path.exists():
            raise ProjectNotFoundError(f"Project file not found: {file_path}")
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                project_data = json.load(f)
            
            # Create data sources
            data_sources = [
                DataSource(
                    name=ds["name"],
                    source_type=ds["source_type"],
                    file_path=Path(ds["file_path"]),
                    created_at=datetime.fromisoformat(ds["created_at"])
                )
                for ds in project_data["data_sources"]
            ]
            
            # Create datasets
            from io import StringIO
            datasets = [
                Dataset(
                    name=ds["name"],
                    data=pd.read_json(StringIO(ds["data"])),
                    metadata=ds["metadata"],
                    created_at=datetime.fromisoformat(ds["created_at"]),
                    modified_at=datetime.fromisoformat(ds["modified_at"])
                )
                for ds in project_data["datasets"]
            ]
            
            # Create visualizations
            visualizations = [
                Visualization(
                    name=v["name"],
                    chart_type=v["chart_type"],
                    config=v["config"],
                    created_at=datetime.fromisoformat(v["created_at"]),
                    modified_at=datetime.fromisoformat(v["modified_at"])
                )
                for v in project_data["visualizations"]
            ]
            
            # Create project
            project = Project(
                name=project_data["name"],
                created=datetime.fromisoformat(project_data["created"]),
                modified=datetime.fromisoformat(project_data["modified"]),
                data_sources=data_sources,
                datasets=datasets,
                visualizations=visualizations,
                file_path=file_path
            )
            
            logger.debug(f"Project loaded successfully from {file_path}")
            return project
            
        except Exception as e:
            logger.error(f"Failed to load project: {e}")
            raise ProjectError(f"Failed to load project: {str(e)}")

    @staticmethod
    def create_new(name: str) -> Project:
        """Create a new project with the given name."""
        now = datetime.now()
        return Project(
            name=name,
            created=now,
            modified=now,
            data_sources=[],
            datasets=[],
            visualizations=[],
            file_path=None
        )
