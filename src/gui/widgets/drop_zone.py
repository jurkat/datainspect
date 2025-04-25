"""Drop zone widgets for the DataInspect application."""
from typing import Callable, Sequence, override
from PyQt6.QtWidgets import QLabel, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent

class DropZone(QFrame):
    """Base class for drop zones with common drag and drop functionality."""

    def __init__(
        self,
        accepted_extensions: Sequence[str],
        drop_hint: str,
        on_file_dropped: Callable[[str], None]
    ) -> None:
        super().__init__()
        self.accepted_extensions = accepted_extensions
        self.on_file_dropped = on_file_dropped

        self._setup_ui(drop_hint)

        # Enable drop
        self.setAcceptDrops(True)

    def _setup_ui(self, drop_hint: str) -> None:
        """Set up the user interface."""
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border: 2px dashed #404040;
                border-radius: 8px;
                min-height: 200px;
            }
            QFrame:hover {
                border-color: #505050;
            }
        """)

        # Create hint label
        self.hint_label = QLabel(drop_hint)
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hint_label.setStyleSheet("""
            QLabel {
                color: #808080;
                font-size: 14px;
                padding: 20px;
                white-space: pre-wrap;
            }
        """)

        # Set layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(self.hint_label)

    @override
    def dragEnterEvent(self, a0: QDragEnterEvent | None) -> None:
        """Handle drag enter events."""
        # Defensives Programmieren mit frühen Returns
        if a0 is None:
            return

        mime_data = a0.mimeData()
        if mime_data is None:
            return

        if not mime_data.hasUrls():
            return

        urls = mime_data.urls()
        if not urls or len(urls) == 0:
            return

        file_path = urls[0].toLocalFile()
        if any(file_path.endswith(ext) for ext in self.accepted_extensions):
            a0.acceptProposedAction()

    @override
    def dropEvent(self, a0: QDropEvent | None) -> None:
        """Handle drop events."""
        # Rename parameter for internal use
        event = a0
        # Defensives Programmieren mit frühen Returns
        if event is None:
            return

        mime_data = event.mimeData()
        if mime_data is None:
            return

        if not mime_data.hasUrls():
            return

        urls = mime_data.urls()
        if not urls or len(urls) == 0:
            return

        file_path = urls[0].toLocalFile()
        event.acceptProposedAction()  # Explizit akzeptieren
        self.on_file_dropped(file_path)


class ProjectDropZone(DropZone):
    """Drop zone specifically for project files."""

    def __init__(self, on_file_dropped: Callable[[str], None]) -> None:
        super().__init__(
            accepted_extensions=['.dinsp'],
            drop_hint="Projektdatei hier ablegen\n(.dinsp)",
            on_file_dropped=on_file_dropped
        )
