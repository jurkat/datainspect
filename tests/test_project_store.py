"""Tests for project store functionality."""
import unittest
import tempfile
import json
from pathlib import Path
from datetime import datetime
import pandas as pd
from unittest import mock
from typing import override

from src.data.models import Project, DataSource, Dataset, Visualization
from src.data.project_store import ProjectStore
from src.exceptions import ProjectNotFoundError, ProjectError
from src.config import PROJECT_FILE_EXTENSION

class TestProjectStore(unittest.TestCase):
    """Test cases for the ProjectStore class."""

    @override
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory to use for test files
        self.temp_dir = tempfile.TemporaryDirectory()

        # Create a test project
        now = datetime.now()
        self.test_project = Project(
            name="Test Project",
            created=now,
            modified=now,
            data_sources=[
                DataSource(
                    name="Test Source",
                    source_type="csv",
                    file_path=Path("test_data.csv"),
                    created_at=now
                )
            ],
            datasets=[
                Dataset(
                    name="Test Dataset",
                    data=pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c']}),
                    metadata={"columns": 2, "rows": 3},
                    created_at=now,
                    modified_at=now
                )
            ],
            visualizations=[
                Visualization(
                    name="Test Visualization",
                    chart_type="bar",
                    config={"x_axis": "A", "y_axis": "B"},
                    created_at=now,
                    modified_at=now
                )
            ]
        )

    @override
    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_create_new_project(self):
        """Test creating a new project."""
        project_name = "New Project"
        project = ProjectStore.create_new(project_name)

        self.assertEqual(project.name, project_name)
        self.assertIsNotNone(project.created)
        self.assertIsNotNone(project.modified)
        self.assertEqual(project.data_sources, [])
        self.assertEqual(project.datasets, [])
        self.assertEqual(project.visualizations, [])
        self.assertIsNone(project.file_path)

    def test_save_and_load_project(self):
        """Test saving and loading a project."""
        # Create file path in the temporary directory
        file_path = Path(self.temp_dir.name) / f"test_project{PROJECT_FILE_EXTENSION}"

        # Save the project
        ProjectStore.save(self.test_project, file_path)

        # Verify the file was created
        self.assertTrue(file_path.exists())

        # Verify file content is JSON
        with open(file_path, 'r') as f:
            project_data = json.load(f)
            self.assertEqual(project_data["name"], self.test_project.name)

        # Load the project
        loaded_project = ProjectStore.load(file_path)

        # Verify loaded project
        self.assertEqual(loaded_project.name, self.test_project.name)
        self.assertEqual(loaded_project.file_path, file_path)
        self.assertEqual(len(loaded_project.data_sources), 1)
        self.assertEqual(len(loaded_project.datasets), 1)
        self.assertEqual(len(loaded_project.visualizations), 1)

        # Verify dataset content
        pd.testing.assert_frame_equal(loaded_project.datasets[0].data,
                                      self.test_project.datasets[0].data)

    def test_load_nonexistent_project(self):
        """Test loading a project that does not exist."""
        nonexistent_path = Path(self.temp_dir.name) / "nonexistent_project.dinsp"

        with self.assertRaises(ProjectNotFoundError):
            _ = ProjectStore.load(nonexistent_path)

    def test_save_with_file_extension_handling(self):
        """Test automatic addition of file extension when saving."""
        # Path without extension
        file_path = Path(self.temp_dir.name) / "test_project_no_extension"

        # Save the project
        ProjectStore.save(self.test_project, file_path)

        # Check that the file has the correct extension
        expected_path = file_path.with_suffix(PROJECT_FILE_EXTENSION)
        self.assertTrue(expected_path.exists())

        # Check that the project's file_path was updated
        self.assertEqual(self.test_project.file_path, expected_path)

    def test_save_with_different_extension(self):
        """Test replacement of incorrect file extension when saving."""
        # Path with different extension
        file_path = Path(self.temp_dir.name) / "test_project.txt"

        # Save the project
        ProjectStore.save(self.test_project, file_path)

        # Check that the file has the correct extension (original extension replaced)
        expected_path = file_path.with_suffix(PROJECT_FILE_EXTENSION)
        self.assertTrue(expected_path.exists())
        self.assertFalse(file_path.exists())  # Original file should not exist

        # Check that the project's file_path was updated
        self.assertEqual(self.test_project.file_path, expected_path)

    @mock.patch('builtins.open', side_effect=IOError("Mock file error"))
    def test_save_project_error(self, mock_open):
        """Test error handling when saving a project fails."""
        file_path = Path(self.temp_dir.name) / f"test_project{PROJECT_FILE_EXTENSION}"

        with self.assertRaises(ProjectError):
            ProjectStore.save(self.test_project, file_path)

    @mock.patch('builtins.open', side_effect=IOError("Mock file error"))
    def test_load_project_error(self, mock_open):
        """Test error handling when loading a project fails."""
        # Create a dummy file to bypass the existence check
        file_path = Path(self.temp_dir.name) / f"test_project{PROJECT_FILE_EXTENSION}"
        file_path.touch()

        with self.assertRaises(ProjectError):
            _ = ProjectStore.load(file_path)

    def test_unsaved_changes_after_save(self):
        """Test that _last_saved_state is updated after save."""
        file_path = Path(self.temp_dir.name) / f"test_project{PROJECT_FILE_EXTENSION}"

        # Initially project should have unsaved changes
        self.assertTrue(self.test_project.has_unsaved_changes())

        # Save the project
        ProjectStore.save(self.test_project, file_path)

        # After saving, there should be no unsaved changes
        self.assertFalse(self.test_project.has_unsaved_changes())

        # Modify the project
        self.test_project.name = "Modified Project"

        # Now it should have unsaved changes again
        self.assertTrue(self.test_project.has_unsaved_changes())


if __name__ == '__main__':
    _ = unittest.main()
