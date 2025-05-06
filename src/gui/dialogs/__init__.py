"""Dialog collection for the DataInspect application."""
from .new_project_dialog import NewProjectDialog
from .rename_project_dialog import RenameProjectDialog
from .csv_import_dialog import CSVImportDialog
from .csv_import_with_transform_dialog import CSVImportDialogWithTransformation
from .visualization_creation_dialog import VisualizationCreationDialog

__all__ = [
    'NewProjectDialog',
    'RenameProjectDialog',
    'CSVImportDialog',
    'CSVImportDialogWithTransformation',
    'VisualizationCreationDialog'
]
