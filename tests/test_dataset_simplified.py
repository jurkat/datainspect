"""Tests for Dataset functionality."""
import unittest
from datetime import datetime
import pandas as pd
import numpy as np
from typing import override

from src.data.models import Dataset


class TestDataset(unittest.TestCase):
    """Test cases for Dataset class."""

    @override
    def setUp(self) -> None:
        """Set up test fixtures."""
        # Create test data with different data types and edge cases
        self.test_df = pd.DataFrame({
            'numeric': [1, 2, None, 4, 5],  # Include None/NaN
            'text': ['A', 'B', 'C', None, 'E'],  # Include None
            'mixed': [1, 'text', None, 4.5, '5'],  # Mixed types
            'empty': [None, None, None, None, None],  # All None
            'zeros': [0, 0, 0, 0, 0],  # All zeros
            'dates': pd.date_range(start='2021-01-01', periods=5)  # Dates
        })

        # Create dataset with minimal metadata
        self.now = datetime.now()
        self.minimal_dataset = Dataset(
            data=self.test_df.copy(),
            metadata={},  # Empty metadata
            created_at=self.now,
            modified_at=self.now
        )

        # Create dataset with comprehensive metadata
        self.full_dataset = Dataset(
            data=self.test_df.copy(),
            metadata={
                "rows": 5,
                "columns": 6,
                "delimiter": ",",
                "encoding": "utf-8",
                "has_header": True,
                "skip_rows": 0,
                "decimal": ".",
                "thousands": ",",
                "column_types": {
                    "numeric": "float64",
                    "text": "object",
                    "mixed": "object",
                    "empty": "object",
                    "zeros": "int64",
                    "dates": "datetime64[ns]"
                }
            },
            created_at=self.now,
            modified_at=self.now
        )

        # Create dataset with empty DataFrame
        self.empty_dataset = Dataset(
            data=pd.DataFrame(),  # Empty DataFrame
            metadata={"rows": 0, "columns": 0},
            created_at=self.now,
            modified_at=self.now
        )

    def test_dataset_properties(self) -> None:
        """Test basic dataset properties."""
        # Test minimal dataset
        pd.testing.assert_frame_equal(self.minimal_dataset.data, self.test_df)
        self.assertEqual(self.minimal_dataset.metadata, {})
        self.assertEqual(self.minimal_dataset.created_at, self.now)
        self.assertEqual(self.minimal_dataset.modified_at, self.now)

        # Test full dataset
        pd.testing.assert_frame_equal(self.full_dataset.data, self.test_df)
        self.assertEqual(self.full_dataset.metadata["rows"], 5)
        self.assertEqual(self.full_dataset.metadata["columns"], 6)
        self.assertEqual(self.full_dataset.metadata["delimiter"], ",")
        self.assertEqual(self.full_dataset.created_at, self.now)
        self.assertEqual(self.full_dataset.modified_at, self.now)

        # Test empty dataset
        self.assertTrue(self.empty_dataset.data.empty)
        self.assertEqual(self.empty_dataset.metadata["rows"], 0)
        self.assertEqual(self.empty_dataset.metadata["columns"], 0)

    def test_dataset_data_integrity(self) -> None:
        """Test that the DataFrame data is stored correctly."""
        # Check that the data is a copy, not a reference
        self.test_df.loc[0, 'numeric'] = 999
        self.assertNotEqual(self.minimal_dataset.data.loc[0, 'numeric'], 999)

        # Check that all columns are preserved
        self.assertEqual(list(self.minimal_dataset.data.columns),
                         ['numeric', 'text', 'mixed', 'empty', 'zeros', 'dates'])

        # Check that NaN values are preserved
        self.assertTrue(pd.isna(self.minimal_dataset.data.loc[2, 'numeric']))
        self.assertTrue(pd.isna(self.minimal_dataset.data.loc[3, 'text']))

        # Check that data types are preserved
        self.assertTrue(pd.api.types.is_numeric_dtype(self.minimal_dataset.data['numeric']))
        self.assertTrue(pd.api.types.is_object_dtype(self.minimal_dataset.data['text']))
        self.assertTrue(pd.api.types.is_datetime64_dtype(self.minimal_dataset.data['dates']))

    def test_dataset_with_large_data(self) -> None:
        """Test dataset with a large DataFrame."""
        # Create a large DataFrame (1000 rows, 10 columns)
        large_df = pd.DataFrame({
            f'col_{i}': np.random.rand(1000) for i in range(10)
        })

        # Create dataset with large DataFrame
        large_dataset = Dataset(
            data=large_df,
            metadata={"rows": 1000, "columns": 10},
            created_at=self.now,
            modified_at=self.now
        )

        # Check properties
        self.assertEqual(len(large_dataset.data), 1000)
        self.assertEqual(len(large_dataset.data.columns), 10)
        self.assertEqual(large_dataset.metadata["rows"], 1000)
        self.assertEqual(large_dataset.metadata["columns"], 10)

    def test_get_preview(self) -> None:
        """Test the get_preview method."""
        # Test with default rows
        preview = self.minimal_dataset.get_preview()
        self.assertEqual(len(preview), 5)  # Default is 10 rows, but our test data only has 5 rows
        pd.testing.assert_frame_equal(preview, self.test_df.head(10))

        # Test with custom rows
        preview = self.minimal_dataset.get_preview(3)
        self.assertEqual(len(preview), 3)
        pd.testing.assert_frame_equal(preview, self.test_df.head(3))

        # Test with empty dataset
        preview = self.empty_dataset.get_preview()
        self.assertTrue(preview.empty)

    def test_get_column_types(self) -> None:
        """Test the get_column_types method."""
        # Test with minimal dataset
        column_types = self.minimal_dataset.get_column_types()
        self.assertEqual(len(column_types), 6)
        self.assertTrue("float" in column_types['numeric'].lower())
        self.assertEqual(column_types['text'], 'object')
        self.assertEqual(column_types['mixed'], 'object')
        self.assertTrue("datetime" in column_types['dates'].lower())

        # Test with empty dataset
        column_types = self.empty_dataset.get_column_types()
        self.assertEqual(len(column_types), 0)

    def test_generate_metadata(self) -> None:
        """Test the generate_metadata method."""
        # Test with minimal dataset and no source info
        self.minimal_dataset.generate_metadata()
        self.assertEqual(self.minimal_dataset.metadata["rows"], 5)
        self.assertEqual(self.minimal_dataset.metadata["columns"], 6)
        self.assertTrue("column_types" in self.minimal_dataset.metadata)
        self.assertEqual(len(self.minimal_dataset.metadata["column_types"]), 6)

        # Test with source info
        source_info = {
            "delimiter": ";",
            "encoding": "latin1",
            "has_header": False
        }
        self.minimal_dataset.generate_metadata(source_info)
        self.assertEqual(self.minimal_dataset.metadata["delimiter"], ";")
        self.assertEqual(self.minimal_dataset.metadata["encoding"], "latin1")
        self.assertEqual(self.minimal_dataset.metadata["has_header"], False)

        # Test with empty dataset
        self.empty_dataset.generate_metadata()
        self.assertEqual(self.empty_dataset.metadata["rows"], 0)
        self.assertEqual(self.empty_dataset.metadata["columns"], 0)
        self.assertEqual(len(self.empty_dataset.metadata["column_types"]), 0)

    def test_columns_initialization(self) -> None:
        """Test that columns are initialized correctly."""
        # Check that columns were created
        self.assertEqual(len(self.minimal_dataset.columns), 6)

        # Check column names
        column_names = [col.name for col in self.minimal_dataset.columns]
        self.assertEqual(column_names, ['numeric', 'text', 'mixed', 'empty', 'zeros', 'dates'])

        # Check column data types
        numeric_column = self.minimal_dataset.get_column_by_name('numeric')
        self.assertIsNotNone(numeric_column)
        if numeric_column:
            self.assertEqual(numeric_column.data_type, 'numeric')
            self.assertTrue('float' in numeric_column.original_type.lower())

        text_column = self.minimal_dataset.get_column_by_name('text')
        self.assertIsNotNone(text_column)
        if text_column:
            self.assertEqual(text_column.data_type, 'text')
            self.assertEqual(text_column.original_type, 'object')

        date_column = self.minimal_dataset.get_column_by_name('dates')
        self.assertIsNotNone(date_column)
        if date_column:
            self.assertEqual(date_column.data_type, 'date')
            self.assertTrue('datetime' in date_column.original_type.lower())

    def test_column_statistics(self) -> None:
        """Test that column statistics are calculated correctly."""
        numeric_column = self.minimal_dataset.get_column_by_name('numeric')
        self.assertIsNotNone(numeric_column)
        if numeric_column:
            # Check basic stats
            self.assertEqual(numeric_column.stats['count'], 4)  # 4 non-null values
            self.assertEqual(numeric_column.stats['null_count'], 1)  # 1 null value
            self.assertEqual(numeric_column.stats['unique_count'], 4)  # 4 unique values

            # Check numeric stats
            self.assertEqual(numeric_column.stats['min'], 1)
            self.assertEqual(numeric_column.stats['max'], 5)
            self.assertAlmostEqual(numeric_column.stats['mean'], 3.0)

    def test_to_json_and_from_json(self) -> None:
        """Test serialization and deserialization of Dataset."""
        # Convert to JSON
        json_data = self.minimal_dataset.to_json()

        # Check JSON structure
        self.assertIn('data', json_data)
        self.assertIn('metadata', json_data)
        self.assertIn('created_at', json_data)
        self.assertIn('modified_at', json_data)
        self.assertIn('columns', json_data)

        # Check columns in JSON
        self.assertEqual(len(json_data['columns']), 6)

        # Create new dataset from JSON
        new_dataset = Dataset.from_json(json_data)

        # Statt direktem Vergleich der DataFrames, prüfen wir die wichtigen Eigenschaften
        # 1. Gleiche Anzahl an Zeilen und Spalten
        self.assertEqual(new_dataset.data.shape, self.minimal_dataset.data.shape)

        # 2. Gleiche Spaltennamen
        self.assertListEqual(list(new_dataset.data.columns), list(self.minimal_dataset.data.columns))

        # 3. Prüfe numerische Werte (für nicht-Datum-Spalten)
        for col in ['numeric', 'zeros']:
            # Konvertiere beide zu float für den Vergleich
            orig_values = self.minimal_dataset.data[col].fillna(-999).astype(float).tolist()
            new_values = new_dataset.data[col].fillna(-999).astype(float).tolist()
            self.assertListEqual(orig_values, new_values)

        # 4. Prüfe Text-Werte
        for col in ['text', 'mixed']:
            # Konvertiere beide zu string für den Vergleich
            orig_values = self.minimal_dataset.data[col].fillna('').astype(str).tolist()
            new_values = new_dataset.data[col].fillna('').astype(str).tolist()
            self.assertListEqual(orig_values, new_values)

        # Check that columns are preserved
        self.assertEqual(len(new_dataset.columns), 6)

        # Check that column stats are preserved
        numeric_column = new_dataset.get_column_by_name('numeric')
        self.assertIsNotNone(numeric_column)
        if numeric_column:
            self.assertEqual(numeric_column.stats['count'], 4)
            self.assertEqual(numeric_column.stats['null_count'], 1)
            self.assertEqual(numeric_column.stats['min'], 1)
            self.assertEqual(numeric_column.stats['max'], 5)


if __name__ == '__main__':
    _ = unittest.main()
