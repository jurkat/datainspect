"""Application exceptions."""

class ProjectError(Exception):
    """Base exception for project-related errors."""

class ProjectNotFoundError(ProjectError):
    """Raised when a project file cannot be found."""

class ImportError(Exception):
    """Raised when data import fails."""

class ValidationError(Exception):
    """Raised when data validation fails."""
