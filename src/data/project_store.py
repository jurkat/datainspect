"""Project storage handling module."""

import json
import logging
from pathlib import Path
from datetime import datetime
import uuid
from typing import Dict, Any
from ..exceptions import ProjectError, ProjectNotFoundError
from ..config import PROJECT_FILE_EXTENSION
from src.data.models import Project, DataSource, Dataset, Visualization

logger = logging.getLogger(__name__)

class ProjectStore:
    """Handles project file storage and loading."""

    @staticmethod
    def save(project: Project, file_path: str | Path) -> None:
        """Save project to file."""
        try:
            file_path = Path(file_path)
            logger.info(f"Saving project to: {file_path}")

            # Ensure correct file extension
            if file_path.suffix != PROJECT_FILE_EXTENSION:
                file_path = file_path.with_suffix(PROJECT_FILE_EXTENSION)

            # Create project directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Prepare project data for serialization
            project_data = {
                "name": project.name,
                "id": project.id,
                "created": project.created.isoformat(),
                "modified": datetime.now().isoformat(),
                "data_sources": []
            }

            # Add data sources with their datasets and visualizations
            for ds in project.data_sources:
                data_source_data: Dict[str, Any] = {
                    "id": ds.id,
                    "name": ds.name,
                    "source_type": ds.source_type,
                    "file_path": str(ds.file_path),
                    "created_at": ds.created_at.isoformat(),
                    "dataset": None,
                    "visualizations": []
                }

                # Add dataset if available
                if ds.dataset:
                    data_source_data["dataset"] = ds.dataset.to_json()

                # Add visualizations
                visualizations_list = data_source_data["visualizations"]
                if isinstance(visualizations_list, list):
                    for vis in ds.visualizations:
                        visualizations_list.append({
                            "id": vis.id,
                            "name": vis.name,
                            "chart_type": vis.chart_type,
                            "config": vis.config,
                            "created_at": vis.created_at.isoformat(),
                            "modified_at": vis.modified_at.isoformat()
                        })

                data_sources_list = project_data["data_sources"]
                if isinstance(data_sources_list, list):
                    data_sources_list.append(data_source_data)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, indent=2)
            project.file_path = file_path
            logger.debug(f"Project saved successfully to {file_path}")
        except Exception as e:
            logger.error(f"Error saving project: {e}")
            raise ProjectError(f"Projekt konnte nicht gespeichert werden: {str(e)}")

        # After successful save, update the saved state
        # Use public methods to update the project state
        saved_state = {
            'name': project.name,
            'id': project.id,
            'modified': project.modified,
            'data_sources': project.data_sources.copy(),  # Create copies of the lists
        }
        project.set_saved_state(saved_state)
        project.set_collections_modified(False)  # Reset the modification flag after saving

    @staticmethod
    def load(file_path: str | Path) -> Project:
        """Load project from file."""
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"Project file not found: {file_path}")
            # User-facing message remains in German
            raise ProjectNotFoundError(f"Projektdatei nicht gefunden: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                project_data = json.load(f)

            # Create data sources with their datasets and visualizations
            data_sources = []

            for ds_data in project_data.get("data_sources", []):
                # Create visualizations
                visualizations = []
                for vis_data in ds_data.get("visualizations", []):
                    visualization = Visualization(
                        name=vis_data["name"],
                        chart_type=vis_data["chart_type"],
                        config=vis_data["config"],
                        created_at=datetime.fromisoformat(vis_data["created_at"]),
                        modified_at=datetime.fromisoformat(vis_data["modified_at"]),
                        id=vis_data.get("id", str(uuid.uuid4()))
                    )
                    visualizations.append(visualization)

                # Create dataset if available
                dataset = None
                if ds_data.get("dataset"):
                    dataset_data = ds_data["dataset"]
                    dataset = Dataset.from_json(dataset_data)

                # Create data source
                data_source = DataSource(
                    name=ds_data["name"],
                    source_type=ds_data["source_type"],
                    file_path=Path(ds_data["file_path"]),
                    created_at=datetime.fromisoformat(ds_data["created_at"]),
                    id=ds_data.get("id", str(uuid.uuid4())),
                    dataset=dataset,
                    visualizations=visualizations
                )
                data_sources.append(data_source)

            # Handle legacy format (pre-restructuring)
            if "datasets" in project_data or "visualizations" in project_data:
                logger.warning("Loading project in legacy format. Converting to new format.")

                # Create datasets from legacy format if needed
                if "datasets" in project_data and data_sources:
                    for ds_data in project_data["datasets"]:
                        # Find matching data source based on name convention
                        ds_name = ds_data["name"]
                        for ds in data_sources:
                            if ds_name.startswith(ds.file_path.stem):
                                # Create dataset
                                dataset = Dataset.from_json(ds_data)
                                # Assign to data source if it doesn't already have one
                                if ds.dataset is None:
                                    ds.dataset = dataset
                                break

                # Create visualizations from legacy format if needed
                if "visualizations" in project_data and data_sources:
                    for v_data in project_data["visualizations"]:
                        visualization = Visualization(
                            name=v_data["name"],
                            chart_type=v_data["chart_type"],
                            config=v_data["config"],
                            created_at=datetime.fromisoformat(v_data["created_at"]),
                            modified_at=datetime.fromisoformat(v_data["modified_at"]),
                            id=str(uuid.uuid4())
                        )
                        # Assign to first data source as a fallback
                        if data_sources:
                            data_sources[0].visualizations.append(visualization)

            # Create project
            project = Project(
                name=project_data["name"],
                created=datetime.fromisoformat(project_data["created"]),
                modified=datetime.fromisoformat(project_data["modified"]),
                data_sources=data_sources,
                file_path=file_path,
                id=project_data.get("id", str(uuid.uuid4()))
            )

            logger.debug(f"Project successfully loaded from {file_path}")
            return project

        except Exception as e:
            logger.error(f"Error loading project: {e}")
            raise ProjectError(f"Projekt konnte nicht geladen werden: {str(e)}")

    @staticmethod
    def create_new(name: str) -> Project:
        """Create a new project with the given name."""
        now = datetime.now()
        return Project(
            name=name,
            created=now,
            modified=now,
            data_sources=[],
            file_path=None
        )
