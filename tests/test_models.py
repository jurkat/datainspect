"""Tests for data models."""
import unittest
from datetime import datetime
from pathlib import Path
import pandas as pd
from src.data.models import DataSource, Dataset, Visualization, Project

class TestDataModels(unittest.TestCase):
    """Test cases for data model classes."""

    def test_data_source_creation(self):
        """Test DataSource object creation."""
        name = "Test Source"
        source_type = "csv"
        file_path = Path("/path/to/file.csv")
        created_at = datetime.now()

        source = DataSource(
            name=name,
            source_type=source_type,
            file_path=file_path,
            created_at=created_at
        )

        self.assertEqual(source.name, name)
        self.assertEqual(source.source_type, source_type)
        self.assertEqual(source.file_path, file_path)
        self.assertEqual(source.created_at, created_at)

    def test_dataset_creation(self):
        """Test Dataset object creation."""
        name = "Test Dataset"
        data = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c']})
        metadata = {"columns": 2, "rows": 3}
        created_at = datetime.now()
        modified_at = datetime.now()

        dataset = Dataset(
            name=name,
            data=data,
            metadata=metadata,
            created_at=created_at,
            modified_at=modified_at
        )

        self.assertEqual(dataset.name, name)
        pd.testing.assert_frame_equal(dataset.data, data)
        self.assertEqual(dataset.metadata, metadata)
        self.assertEqual(dataset.created_at, created_at)
        self.assertEqual(dataset.modified_at, modified_at)

    def test_visualization_creation(self):
        """Test Visualization object creation."""
        name = "Test Visualization"
        chart_type = "bar"
        config = {"x_axis": "A", "y_axis": "B"}
        created_at = datetime.now()
        modified_at = datetime.now()

        viz = Visualization(
            name=name,
            chart_type=chart_type,
            config=config,
            created_at=created_at,
            modified_at=modified_at
        )

        self.assertEqual(viz.name, name)
        self.assertEqual(viz.chart_type, chart_type)
        self.assertEqual(viz.config, config)
        self.assertEqual(viz.created_at, created_at)
        self.assertEqual(viz.modified_at, modified_at)

    def test_project_creation(self):
        """Test Project object creation."""
        name = "Test Project"
        created = datetime.now()
        modified = datetime.now()
        data_sources = []
        datasets = []
        visualizations = []

        project = Project(
            name=name,
            created=created,
            modified=modified,
            data_sources=data_sources,
            datasets=datasets,
            visualizations=visualizations
        )

        self.assertEqual(project.name, name)
        self.assertEqual(project.created, created)
        self.assertEqual(project.modified, modified)
        self.assertEqual(project.data_sources, data_sources)
        self.assertEqual(project.datasets, datasets)
        self.assertEqual(project.visualizations, visualizations)
        self.assertIsNone(project.file_path)
        self.assertIsNone(project.get_saved_state())

    def test_project_has_unsaved_changes(self):
        """Test Project.has_unsaved_changes method."""
        # New project should have unsaved changes
        project = Project(
            name="Test Project",
            created=datetime.now(),
            modified=datetime.now(),
            data_sources=[],
            datasets=[],
            visualizations=[]
        )
        self.assertTrue(project.has_unsaved_changes())

        # Set saved state and test no changes
        saved_state = {
            'name': project.name,
            'modified': project.modified,
            'data_sources': project.data_sources,
            'datasets': project.datasets,
            'visualizations': project.visualizations
        }
        project.set_saved_state(saved_state)
        self.assertFalse(project.has_unsaved_changes())

        # Make a name change and test for unsaved changes
        project.name = "Modified Project"
        self.assertTrue(project.has_unsaved_changes())

        # Reset saved state with updated data
        saved_state = {
            'name': project.name,
            'modified': project.modified,
            'data_sources': project.data_sources,
            'datasets': project.datasets,
            'visualizations': project.visualizations
        }
        project.set_saved_state(saved_state)
        self.assertFalse(project.has_unsaved_changes())

        # Test with data source changes
        data_source = DataSource(
            name="Test Source",
            source_type="csv",
            file_path=Path("/path/to/file.csv"),
            created_at=datetime.now()
        )
        project.data_sources.append(data_source)
        self.assertTrue(project.has_unsaved_changes())


if __name__ == '__main__':
    _ = unittest.main()
