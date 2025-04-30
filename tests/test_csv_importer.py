"""Tests for the CSV importer."""
import unittest
from pathlib import Path
import tempfile
import os
import sys
import pandas as pd
from typing import override

# Add parent directory to path to allow imports from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.importers.csv_importer import CSVImporter
from src.data.models import DataSource


class TestCSVImporter(unittest.TestCase):
    """Test cases for the CSV importer."""

    @override
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary CSV file for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.csv_path = Path(os.path.join(self.temp_dir.name, "test.csv"))

        # Create a simple CSV file
        self.test_data = pd.DataFrame({
            "Name": ["Alice", "Bob", "Charlie"],
            "Age": [25, 30, 35],
            "City": ["New York", "London", "Paris"]
        })
        self.test_data.to_csv(self.csv_path, index=False)

        # Create a CSV file with different delimiter
        self.csv_path_semicolon = Path(os.path.join(self.temp_dir.name, "test_semicolon.csv"))
        self.test_data.to_csv(self.csv_path_semicolon, index=False, sep=";")

        # Create a CSV file without header
        self.csv_path_no_header = Path(os.path.join(self.temp_dir.name, "test_no_header.csv"))
        _ = self.test_data.to_csv(self.csv_path_no_header, index=False, header=False)

        # Create an empty CSV file
        self.csv_path_empty = Path(os.path.join(self.temp_dir.name, "empty.csv"))
        with open(self.csv_path_empty, "w") as f:
            _ = f.write("")

    @override
    def tearDown(self):
        """Tear down test fixtures."""
        self.temp_dir.cleanup()

    def test_import_file_basic(self):
        """Test basic CSV import with default options."""
        data_source, error = CSVImporter.import_file(self.csv_path)

        self.assertIsNone(error)
        self.assertIsNotNone(data_source)

        if data_source:
            self.assertIsInstance(data_source, DataSource)
            self.assertIsNotNone(data_source.dataset)

            # Check data source properties
            self.assertEqual(data_source.name, self.csv_path.name)
            self.assertEqual(data_source.source_type, "CSV")
            self.assertEqual(data_source.file_path, self.csv_path)

            # Check dataset properties
            dataset = data_source.dataset
            if dataset:
                self.assertEqual(len(dataset.data), 3)  # 3 rows
                self.assertEqual(len(dataset.data.columns), 3)  # 3 columns

                # Check metadata
                self.assertEqual(dataset.metadata["rows"], 3)
                self.assertEqual(dataset.metadata["columns"], 3)
                self.assertEqual(dataset.metadata["delimiter"], ",")
                self.assertEqual(dataset.metadata["has_header"], True)

    def test_import_file_semicolon(self):
        """Test CSV import with semicolon delimiter."""
        data_source, error = CSVImporter.import_file(
            self.csv_path_semicolon,
            delimiter=";"
        )

        self.assertIsNone(error)
        self.assertIsNotNone(data_source)

        if data_source:
            self.assertIsInstance(data_source, DataSource)
            self.assertIsNotNone(data_source.dataset)

            dataset = data_source.dataset
            if dataset:
                self.assertEqual(len(dataset.data), 3)  # 3 rows
                self.assertEqual(len(dataset.data.columns), 3)  # 3 columns
                self.assertEqual(dataset.metadata["delimiter"], ";")

    def test_import_file_no_header(self):
        """Test CSV import without header."""
        data_source, error = CSVImporter.import_file(
            self.csv_path_no_header,
            has_header=False
        )

        self.assertIsNone(error)
        self.assertIsNotNone(data_source)

        if data_source:
            self.assertIsInstance(data_source, DataSource)
            self.assertIsNotNone(data_source.dataset)

            dataset = data_source.dataset
            if dataset:
                self.assertEqual(len(dataset.data), 3)  # 3 rows
                self.assertEqual(len(dataset.data.columns), 3)  # 3 columns
                self.assertEqual(dataset.metadata["has_header"], False)

                # Column names should be in the format "Spalte_X" when no header is present
                self.assertTrue(all(str(col).startswith("Spalte_") for col in dataset.data.columns))

    def test_import_empty_file(self):
        """Test importing an empty CSV file."""
        data_source, error = CSVImporter.import_file(self.csv_path_empty)

        self.assertIsNotNone(error)
        self.assertIsNone(data_source)
        # Die Fehlermeldung enthält "No columns to parse from file"
        if error:
            self.assertIn("no columns", error.lower())

    def test_detect_delimiter(self):
        """Test delimiter detection."""
        # Test with comma delimiter
        delimiter = CSVImporter.detect_delimiter(self.csv_path)
        self.assertEqual(delimiter, ",")

        # Test with semicolon delimiter
        delimiter = CSVImporter.detect_delimiter(self.csv_path_semicolon)
        self.assertEqual(delimiter, ";")

    def test_get_preview(self):
        """Test preview generation."""
        preview_df, error = CSVImporter.get_preview(self.csv_path, preview_rows=2)

        self.assertIsNone(error)
        self.assertIsInstance(preview_df, pd.DataFrame)
        if preview_df is not None:
            self.assertEqual(len(preview_df), 2)  # Should have 2 rows
            self.assertEqual(len(preview_df.columns), 3)  # Should have 3 columns


if __name__ == "__main__":
    _ = unittest.main()
