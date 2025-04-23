"""Application exceptions."""

class ProjectError(Exception):
    """Base exception for project-related errors."""
    pass

class ProjectNotFoundError(ProjectError):
    """Raised when a project file cannot be found."""
    pass

class ImportError(Exception):
    """Raised when data import fails."""
    pass

class ValidationError(Exception):
    """Raised when data validation fails."""
    pass
