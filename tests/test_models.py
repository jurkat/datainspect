"""Tests for data models."""
import unittest
from datetime import datetime
from pathlib import Path
from typing import override
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
        self.assertIsNotNone(source.id)
        self.assertIsNone(source.dataset)
        self.assertEqual(source.visualizations, [])

    def test_dataset_creation(self):
        """Test Dataset object creation."""
        data = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c']})
        metadata = {"columns": 2, "rows": 3}
        created_at = datetime.now()
        modified_at = datetime.now()

        dataset = Dataset(
            data=data,
            metadata=metadata,
            created_at=created_at,
            modified_at=modified_at
        )

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
        self.assertIsNotNone(viz.id)

    def test_project_creation(self):
        """Test Project object creation."""
        name = "Test Project"
        created = datetime.now()
        modified = datetime.now()
        data_sources = []

        project = Project(
            name=name,
            created=created,
            modified=modified,
            data_sources=data_sources
        )

        self.assertEqual(project.name, name)
        self.assertEqual(project.created, created)
        self.assertEqual(project.modified, modified)
        self.assertEqual(project.data_sources, data_sources)
        self.assertIsNone(project.file_path)
        self.assertIsNotNone(project.id)
        self.assertIsNone(project.get_saved_state())

    def test_project_has_unsaved_changes(self):
        """Test Project.has_unsaved_changes method."""
        # New project should have unsaved changes
        project = Project(
            name="Test Project",
            created=datetime.now(),
            modified=datetime.now(),
            data_sources=[]
        )
        self.assertTrue(project.has_unsaved_changes())

        # Set saved state and test no changes
        saved_state = {
            'name': project.name,
            'id': project.id,
            'modified': project.modified,
            'data_sources': project.data_sources
        }
        project.set_saved_state(saved_state)
        self.assertFalse(project.has_unsaved_changes())

        # Make a name change and test for unsaved changes
        project.name = "Modified Project"
        self.assertTrue(project.has_unsaved_changes())

        # Reset saved state with updated data
        saved_state = {
            'name': project.name,
            'id': project.id,
            'modified': project.modified,
            'data_sources': project.data_sources
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


# Observer für die Project-Klasse (keine Testklasse)
class ProjectObserverForTests:
    """Test observer class for Project objects."""

    def __init__(self) -> None:
        """Initialize the test observer."""
        self.reset()

    def reset(self) -> None:
        """Reset the observer state."""
        self.updated = False
        self.update_count = 0
        self.last_subject = None
        self.last_event = None
        self.last_data_source = None
        self.last_dataset = None
        self.last_visualization = None

    def on_subject_change(self, subject, **kwargs) -> None:
        """Called when the observed subject changes."""
        self.updated = True
        self.update_count += 1
        self.last_subject = subject
        self.last_event = kwargs.get('event')
        self.last_data_source = kwargs.get('data_source')
        self.last_dataset = kwargs.get('dataset')
        self.last_visualization = kwargs.get('visualization')


class TestProjectObservable(unittest.TestCase):
    """Test cases for Project as Observable."""

    @override
    def setUp(self) -> None:
        """Set up test fixtures."""
        self.now = datetime.now()
        self.project = Project(
            name="Test Project",
            created=self.now,
            modified=self.now,
            data_sources=[]
        )
        self.observer = ProjectObserverForTests()
        self.project.add_observer(self.observer)

        # Create test objects
        self.data_source = DataSource(
            name="Test Source",
            source_type="csv",
            file_path=Path("/path/to/file.csv"),
            created_at=self.now
        )

        self.dataset = Dataset(
            data=pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c']}),
            metadata={"columns": 2, "rows": 3},
            created_at=self.now,
            modified_at=self.now
        )

        self.visualization = Visualization(
            name="Test Visualization",
            chart_type="bar",
            config={"x_axis": "A", "y_axis": "B"},
            created_at=self.now,
            modified_at=self.now
        )

    def test_add_data_source(self) -> None:
        """Test adding a data source to the project."""
        # Reset observer state
        self.observer.updated = False
        self.observer.update_count = 0

        # Add data source using the proper method
        self.project.add_data_source(self.data_source)

        # Check that observer was notified
        self.assertTrue(self.observer.updated)
        self.assertEqual(self.observer.update_count, 1)
        self.assertEqual(self.observer.last_subject, self.project)
        self.assertEqual(self.observer.last_event, "data_source_added")
        self.assertEqual(self.observer.last_data_source, self.data_source)

        # Check that data source was added
        self.assertEqual(len(self.project.data_sources), 1)
        self.assertEqual(self.project.data_sources[0], self.data_source)

        # Check that collections were modified
        # Wir verwenden hier absichtlich ein geschütztes Attribut für Testzwecke
        # pylint: disable=protected-access
        self.assertTrue(self.project._collections_modified)  # type: ignore

    def test_add_dataset_to_data_source(self) -> None:
        """Test adding a dataset to a data source."""
        # Add data source to project
        self.project.add_data_source(self.data_source)

        # Reset observer state
        self.observer.updated = False
        self.observer.update_count = 0

        # Add dataset to data source
        self.data_source.dataset = self.dataset

        # Manually notify observers since we modified the data source directly
        self.project.notify_observers(event="dataset_added", dataset=self.dataset)

        # Check that observer was notified
        self.assertTrue(self.observer.updated)
        self.assertEqual(self.observer.update_count, 1)
        self.assertEqual(self.observer.last_subject, self.project)
        self.assertEqual(self.observer.last_event, "dataset_added")
        self.assertEqual(self.observer.last_dataset, self.dataset)

        # Check that dataset was added to data source
        self.assertEqual(self.data_source.dataset, self.dataset)

        # Check that collections were modified
        # Wir verwenden hier absichtlich ein geschütztes Attribut für Testzwecke
        # pylint: disable=protected-access
        self.assertTrue(self.project._collections_modified)  # type: ignore

    def test_add_visualization_to_data_source(self) -> None:
        """Test adding a visualization to a data source."""
        # Add data source to project
        self.project.add_data_source(self.data_source)

        # Reset observer state
        self.observer.updated = False
        self.observer.update_count = 0

        # Add visualization to data source
        self.data_source.add_visualization(self.visualization)

        # Check that visualization was added to data source
        self.assertEqual(len(self.data_source.visualizations), 1)
        self.assertEqual(self.data_source.visualizations[0], self.visualization)

        # Manually notify observers since we modified the data source directly
        self.project.notify_observers(event="visualization_added", visualization=self.visualization)

        # Now the observer should be updated
        self.assertTrue(self.observer.updated)
        self.assertEqual(self.observer.update_count, 1)
        self.assertEqual(self.observer.last_subject, self.project)
        self.assertEqual(self.observer.last_event, "visualization_added")
        self.assertEqual(self.observer.last_visualization, self.visualization)

        # Test get_visualization_by_id method
        vis_id = self.visualization.id
        retrieved_vis = self.data_source.get_visualization_by_id(vis_id)
        self.assertEqual(retrieved_vis, self.visualization)

    def test_remove_data_source(self) -> None:
        """Test removing a data source from the project."""
        # Add data source first using the proper method
        self.project.add_data_source(self.data_source)

        # Reset observer state
        self.observer.updated = False
        self.observer.update_count = 0

        # Remove data source using the proper method
        self.project.remove_data_source(self.data_source)

        # Check that observer was notified
        self.assertTrue(self.observer.updated)
        self.assertEqual(self.observer.update_count, 1)
        self.assertEqual(self.observer.last_subject, self.project)
        self.assertEqual(self.observer.last_event, "data_source_removed")
        self.assertEqual(self.observer.last_data_source, self.data_source)

        # Check that data source was removed
        self.assertEqual(len(self.project.data_sources), 0)

        # Check that collections were modified
        # Wir verwenden hier absichtlich ein geschütztes Attribut für Testzwecke
        # pylint: disable=protected-access
        self.assertTrue(self.project._collections_modified)  # type: ignore

    def test_clear_data_sources(self) -> None:
        """Test clearing data sources in the project."""
        # Add data source with dataset and visualization
        self.project.add_data_source(self.data_source)
        self.data_source.dataset = self.dataset
        self.data_source.add_visualization(self.visualization)

        # Reset observer state and collections_modified flag
        self.observer.updated = False
        self.observer.update_count = 0
        # Wir verwenden hier absichtlich ein geschütztes Attribut für Testzwecke
        # pylint: disable=protected-access
        self.project._collections_modified = False  # type: ignore

        # Clear collections directly
        # This will call _on_collection_modified but not notify observers
        self.project.data_sources.clear()

        # Check that the collection was modified
        # Wir verwenden hier absichtlich ein geschütztes Attribut für Testzwecke
        # pylint: disable=protected-access
        self.assertTrue(self.project._collections_modified)  # type: ignore

        # Check that collection was cleared
        self.assertEqual(len(self.project.data_sources), 0)

        # But the observer was not notified since clear() doesn't call notify_observers
        self.assertFalse(self.observer.updated)

        # Manually notify observers to simulate what a clear_data_sources method would do
        self.project.notify_observers(event="data_sources_cleared")

        # Now the observer should be updated
        self.assertTrue(self.observer.updated)
        self.assertEqual(self.observer.update_count, 1)
        self.assertEqual(self.observer.last_subject, self.project)
        self.assertEqual(self.observer.last_event, "data_sources_cleared")

    def test_multiple_observers(self) -> None:
        """Test multiple observers on the same project."""
        # Create a second observer
        observer2 = ProjectObserverForTests()
        self.project.add_observer(observer2)

        # Reset observer states
        self.observer.updated = False
        self.observer.update_count = 0
        observer2.updated = False
        observer2.update_count = 0

        # Modify project
        self.project.name = "Modified Project"
        self.project.notify_observers(event="name_changed")

        # Check that both observers were notified
        self.assertTrue(self.observer.updated)
        self.assertEqual(self.observer.update_count, 1)
        self.assertEqual(self.observer.last_event, "name_changed")

        self.assertTrue(observer2.updated)
        self.assertEqual(observer2.update_count, 1)
        self.assertEqual(observer2.last_event, "name_changed")

    def test_remove_observer(self) -> None:
        """Test removing an observer from the project."""
        # Reset observer state
        self.observer.updated = False
        self.observer.update_count = 0

        # Remove observer
        self.project.remove_observer(self.observer)

        # Modify project
        self.project.name = "Modified Project"
        self.project.notify_observers(event="name_changed")

        # Check that observer was not notified
        self.assertFalse(self.observer.updated)
        self.assertEqual(self.observer.update_count, 0)


if __name__ == '__main__':
    _ = unittest.main()
