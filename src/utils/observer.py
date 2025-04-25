"""Observer pattern implementation for model-view communication.

This module provides a simple implementation of the Observer pattern,
allowing model objects to notify UI components about data changes.
"""
from typing import Any, Set, TypeVar

T = TypeVar('T')

# Using standard duck typing approach instead of Protocol to avoid metaclass conflicts
class Observable:
    """Base class for objects that can be observed."""
    
    def __init__(self) -> None:
        """Initialize the observable object."""
        self._observers: Set[Any] = set()
        
    def add_observer(self, observer: Any) -> None:
        """Add an observer to this object.
        
        Args:
            observer: An object with an 'on_subject_change' method to notify of changes
        """
        if hasattr(observer, 'on_subject_change') and callable(observer.on_subject_change):
            self._observers.add(observer)
        else:
            raise TypeError("Observer must have an 'on_subject_change' method")
        
    def remove_observer(self, observer: Any) -> None:
        """Remove an observer from this object.
        
        Args:
            observer: The observer to remove
        """
        self._observers.discard(observer)
        
    def notify_observers(self, *args: Any, **kwargs: Any) -> None:
        """Notify all observers of a change.
        
        Args:
            args: Additional positional arguments to pass to observers
            kwargs: Additional keyword arguments to pass to observers
        """
        for observer in self._observers:
            observer.on_subject_change(self, *args, **kwargs)
