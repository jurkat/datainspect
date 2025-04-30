"""Tests for the Observer pattern implementation."""
import unittest
from datetime import datetime
from pathlib import Path
from typing import override

from src.data.models import Project, DataSource
from src.utils.observer import Observable

class ObserverForTests:
    """Observer class for testing the Observer pattern."""

    def __init__(self):
        """Initialize the test observer."""
        self.reset()

    def reset(self):
        """Reset the observer state."""
        self.updated = False
        self.update_count = 0
        self.last_subject = None
        self.last_event = None
        self.last_kwargs = {}

    def on_subject_change(self, subject, **kwargs):
        """Update method that gets called by Observable objects."""
        self.updated = True
        self.update_count += 1
        self.last_subject = subject
        self.last_event = kwargs.get('event')
        self.last_kwargs = kwargs

class TestObservableClass(unittest.TestCase):
    """Test cases for the Observable base class."""

    def test_add_remove_observer(self):
        """Test adding and removing observers from an Observable."""
        observable = Observable()
        observer = ObserverForTests()

        # Add observer
        observable.add_observer(observer)

        # Notify observers
        observable.notify_observers(event="test")

        # Check that the observer was updated
        self.assertTrue(observer.updated)
        self.assertEqual(observer.update_count, 1)
        self.assertEqual(observer.last_subject, observable)
        self.assertEqual(observer.last_event, "test")

        # Reset and remove observer
        observer.updated = False
        observable.remove_observer(observer)

        # Notify again
        observable.notify_observers(event="another_test")

        # Observer should not be updated
        self.assertFalse(observer.updated)
        self.assertEqual(observer.update_count, 1)  # Still 1 from before

    def test_invalid_observer(self):
        """Test adding an invalid observer."""
        observable = Observable()

        # Try to add an object without update method
        with self.assertRaises(TypeError):
            observable.add_observer(object())

class TestProjectAsObservable(unittest.TestCase):
    """Test cases for the Project class as Observable."""

    @override
    def setUp(self):
        """Set up test fixtures."""
        self.now = datetime.now()
        self.project = Project(
            name="Test Project",
            created=self.now,
            modified=self.now,
            data_sources=[]
        )
        self.observer = ObserverForTests()
        self.project.add_observer(self.observer)

    def test_rename_project(self):
        """Test that renaming a project notifies observers."""
        new_name = "Renamed Project"
        old_name = self.project.name

        # Rename the project
        self.project.rename(new_name)

        # Check that the observer was updated
        self.assertTrue(self.observer.updated)
        self.assertEqual(self.observer.last_event, "renamed")
        self.assertEqual(self.observer.last_kwargs.get("old_name"), old_name)
        self.assertEqual(self.observer.last_kwargs.get("new_name"), new_name)
        self.assertEqual(self.project.name, new_name)

    def test_add_data_source(self):
        """Test that adding a data source notifies observers."""
        data_source = DataSource(
            name="Test Source",
            source_type="csv",
            file_path=Path("test.csv"),
            created_at=self.now
        )

        # Add the data source
        self.project.add_data_source(data_source)

        # Check that the observer was updated
        self.assertTrue(self.observer.updated)
        self.assertEqual(self.observer.last_event, "data_source_added")
        self.assertEqual(self.observer.last_kwargs.get("data_source"), data_source)
        self.assertIn(data_source, self.project.data_sources)

    def test_remove_data_source(self):
        """Test that removing a data source notifies observers."""
        # Add a data source first
        data_source = DataSource(
            name="Test Source",
            source_type="csv",
            file_path=Path("test.csv"),
            created_at=self.now
        )
        self.project.add_data_source(data_source)

        # Reset observer state
        self.observer.updated = False
        self.observer.last_event = None

        # Remove the data source
        self.project.remove_data_source(data_source)

        # Check that the observer was updated
        self.assertTrue(self.observer.updated)
        self.assertEqual(self.observer.last_event, "data_source_removed")
        self.assertEqual(self.observer.last_kwargs.get("data_source"), data_source)
        self.assertNotIn(data_source, self.project.data_sources)

    def test_remove_nonexistent_data_source(self):
        """Test removing a data source that doesn't exist."""
        # Create a data source that isn't added to the project
        data_source = DataSource(
            name="Nonexistent Source",
            source_type="csv",
            file_path=Path("nonexistent.csv"),
            created_at=self.now
        )

        # Reset observer state
        self.observer.updated = False

        # Try to remove the data source
        self.project.remove_data_source(data_source)

        # Observer should not be updated
        self.assertFalse(self.observer.updated)

if __name__ == "__main__":
    _ = unittest.main()
