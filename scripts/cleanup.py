"""Clean up project files and directories."""
import logging
import shutil
from pathlib import Path

def setup_logging():
    """Setup basic logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )

def cleanup():
    """Remove temporary files and directories."""
    logger = logging.getLogger(__name__)
    
    # Directories to remove
    dirs_to_remove = [
        '__pycache__',
        '.pytest_cache',
        '.ruff_cache',
        '.mypy_cache',
        '.tox',
        'build',
        'dist',
        'htmlcov',
        '.coverage',
        '*.egg-info',
    ]
    
    # Files to remove
    files_to_remove = [
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '.coverage',
        '*.egg-info',
        '.DS_Store',  # macOS specific
        'Thumbs.db',  # Windows specific
    ]
    
    root = Path('.')
    removed_dirs = 0
    removed_files = 0
    
    # Remove directories
    logger.info("Cleaning up directories...")
    for dir_pattern in dirs_to_remove:
        for dir_path in root.rglob(dir_pattern):
            if dir_path.is_dir():
                try:
                    shutil.rmtree(dir_path)
                    logger.info(f"✓ Removed directory: {dir_path}")
                    removed_dirs += 1
                except Exception as e:
                    logger.error(f"✗ Failed to remove {dir_path}: {e}")
    
    # Remove files
    logger.info("\nCleaning up files...")
    for file_pattern in files_to_remove:
        for file_path in root.rglob(file_pattern):
            if file_path.is_file():
                try:
                    file_path.unlink()
                    logger.info(f"✓ Removed file: {file_path}")
                    removed_files += 1
                except Exception as e:
                    logger.error(f"✗ Failed to remove {file_path}: {e}")
    
    logger.info(f"\nCleanup completed: removed {removed_dirs} directories and {removed_files} files")

if __name__ == '__main__':
    setup_logging()
    cleanup()