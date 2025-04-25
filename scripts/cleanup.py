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
    
    # Security check: Verify we're in the project root directory
    git_dir = Path('.git')
    if not git_dir.exists() or not git_dir.is_dir():
        logger.warning("⚠️ Sie befinden sich möglicherweise nicht im Projektverzeichnis!")
        confirmation = input("Sind Sie sicher, dass Sie hier Dateien löschen möchten? (j/N): ")
        if confirmation.lower() not in ['j', 'ja']:
            logger.info("Vom Benutzer abgebrochen.")
            return
    
    # Directories to remove (only in specific locations for safety)
    dirs_to_remove = [
        '__pycache__',
        '.pytest_cache',
        '.ruff_cache',
        '.mypy_cache',
        '.tox',
        'build',
        'dist',
        'htmlcov',
    ]
    
    # Files to remove (only specific types for safety)
    files_to_remove = [
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '.coverage',
        '.DS_Store',  # macOS specific
        'Thumbs.db',  # Windows specific
    ]
    
    root = Path('.')
    removed_dirs = 0
    removed_files = 0
    
    # Safe directories: Only search recursively within these directories
    safe_dirs = ['src', 'tests', 'scripts', 'venv']
    
    # Key directories to check whether we're in the correct location
    key_dirs = ['src', 'tests', 'scripts']
    key_dirs_found = [d for d in key_dirs if (root / d).exists() and (root / d).is_dir()]
    
    if len(key_dirs_found) < 2:  # At least 2 of the key directories should be present
        logger.warning("⚠️ Not enough project directories were found!")
        logger.warning("You might not be in the project's root directory.")
        confirmation = input("Continue anyway? (y/N): ")
        if confirmation.lower() not in ['y', 'yes']:
            logger.info("Aborted by user.")
            return
    
    # Remove directories
    logger.info("Cleaning up temporary directories...")
    for safe_dir in safe_dirs:
        safe_path = root / safe_dir
        if safe_path.exists() and safe_path.is_dir():
            logger.info(f"Scanning {safe_dir}...")
            for dir_pattern in dirs_to_remove:
                # Only search within safe directories, not the entire project
                for dir_path in safe_path.rglob(dir_pattern):
                    if dir_path.is_dir():
                        try:
                            shutil.rmtree(dir_path)
                            logger.info(f"✓ Removed directory: {dir_path}")
                            removed_dirs += 1
                        except Exception as e:
                            logger.error(f"✗ Failed to remove {dir_path}: {e}")
    
    # Remove files
    logger.info("\nCleaning up temporary files...")
    for safe_dir in safe_dirs:
        safe_path = root / safe_dir
        if safe_path.exists() and safe_path.is_dir():
            for file_pattern in files_to_remove:
                # Only search within safe directories, not the entire project
                for file_path in safe_path.rglob(file_pattern):
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
