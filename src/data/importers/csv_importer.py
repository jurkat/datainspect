"""CSV data importer for DataInspect application."""
import logging
from pathlib import Path
from typing import Optional, Tuple
import pandas as pd
from datetime import datetime

from src.data.models import DataSource, Dataset

logger = logging.getLogger(__name__)

class CSVImporter:
    """Handles importing CSV files into the application."""

    @staticmethod
    def import_file(
        file_path: Path,
        name: Optional[str] = None,
        delimiter: str = ',',
        encoding: str = 'utf-8',
        has_header: bool = True,
        skip_rows: int = 0,
        decimal: str = '.',
        thousands: str = ',',
        preview_only: bool = False,
        preview_rows: int = 5,
        transformed_data: Optional[pd.DataFrame] = None
    ) -> Tuple[Optional[DataSource], Optional[str]]:
        """Import a CSV file and create DataSource object with Dataset.

        Args:
            file_path: Path to the CSV file
            name: Custom name for the data source (defaults to file name if None)
            delimiter: Column delimiter character
            encoding: File encoding
            has_header: Whether the file has a header row
            skip_rows: Number of rows to skip at the beginning
            decimal: Decimal separator character
            thousands: Thousands separator character
            preview_only: If True, only return a preview without creating objects
            preview_rows: Number of rows to include in preview
            transformed_data: Optional DataFrame with transformed data to use instead of reading from file

        Returns:
            A tuple containing:
            - DataSource object with Dataset (None if preview_only is True)
            - Error message (None if successful)
        """
        try:
            # If transformed data is available, use it
            if transformed_data is not None:
                df = transformed_data
            else:
                # Determine header row setting
                header = 0 if has_header else None

                # Read the CSV file
                if preview_only:
                    # For preview, read only a few rows
                    df = pd.read_csv(
                        file_path,
                        delimiter=delimiter,
                        encoding=encoding,
                        header=header,
                        skiprows=skip_rows,
                        decimal=decimal,
                        thousands=thousands,
                        nrows=preview_rows
                    )
                    return None, None

                # For actual import, read the entire file
                df = pd.read_csv(
                    file_path,
                    delimiter=delimiter,
                    encoding=encoding,
                    header=header,
                    skiprows=skip_rows,
                    decimal=decimal,
                    thousands=thousands
                )

                # If no header, rename columns to more user-friendly format
                if not has_header:
                    df.columns = [f"Spalte_{i+1}" for i in range(len(df.columns))]

            # Collect source information
            now = datetime.now()
            source_info = {
                "delimiter": delimiter,
                "encoding": encoding,
                "has_header": has_header,
                "skip_rows": skip_rows,
                "decimal": decimal,
                "thousands": thousands
            }

            # Create DataSource and Dataset objects
            # Use the provided name if available, otherwise use the file name
            source_name = name if name else file_path.name

            # Create Dataset with empty metadata
            dataset = Dataset(
                data=df,
                metadata={},
                created_at=now,
                modified_at=now
            )

            # Generate metadata with source information
            dataset.generate_metadata(source_info)

            # Create DataSource with the Dataset
            data_source = DataSource(
                name=source_name,
                source_type="CSV",
                file_path=file_path,
                created_at=now,
                dataset=dataset
            )

            logger.info(f"Successfully imported CSV file: {file_path}")
            return data_source, None

        except Exception as e:
            error_msg = f"Error importing CSV file: {str(e)}"
            logger.error(f"Error importing CSV file {file_path}: {str(e)}")
            return None, error_msg

    @staticmethod
    def get_preview(
        file_path: Path,
        delimiter: str = ',',
        encoding: str = 'utf-8',
        has_header: bool = True,
        skip_rows: int = 0,
        preview_rows: int = 5
    ) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """Get a preview of the CSV file.

        Args:
            file_path: Path to the CSV file
            delimiter: Column delimiter character
            encoding: File encoding
            has_header: Whether the file has a header row
            skip_rows: Number of rows to skip at the beginning
            preview_rows: Number of rows to include in preview

        Returns:
            A tuple containing:
            - DataFrame with preview data (None if error)
            - Error message (None if successful)
        """
        try:
            # Determine header row setting
            header = 0 if has_header else None

            # Read the CSV file
            df = pd.read_csv(
                file_path,
                delimiter=delimiter,
                encoding=encoding,
                header=header,
                skiprows=skip_rows,
                nrows=preview_rows
            )

            # If no header, rename columns to more user-friendly format
            if not has_header:
                df.columns = [f"Spalte_{i+1}" for i in range(len(df.columns))]

            return df, None

        except Exception as e:
            error_msg = f"Error reading CSV file: {str(e)}"
            logger.error(f"Error reading CSV file {file_path}: {str(e)}")
            return None, error_msg

    @staticmethod
    def detect_delimiter(file_path: Path, encoding: str = 'utf-8') -> str:
        """Attempt to detect the delimiter used in a CSV file.

        Args:
            file_path: Path to the CSV file
            encoding: File encoding

        Returns:
            Detected delimiter character (defaults to ',' if detection fails)
        """
        try:
            # Read the first few lines of the file
            with open(file_path, 'r', encoding=encoding) as f:
                lines = [f.readline() for _ in range(3)]

            # Count occurrences of common delimiters
            delimiters = {',': 0, ';': 0, '\t': 0, '|': 0}

            for line in lines:
                for delimiter, count in delimiters.items():
                    delimiters[delimiter] += line.count(delimiter)

            # Find the delimiter with the most occurrences
            max_count = 0
            detected_delimiter = ','  # Default

            for delimiter, count in delimiters.items():
                if count > max_count:
                    max_count = count
                    detected_delimiter = delimiter

            return detected_delimiter

        except Exception as e:
            logger.warning(f"Error detecting delimiter for {file_path}: {str(e)}")
            return ','  # Default to comma if detection fails
