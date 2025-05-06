"""Dialog for creating visualizations in DataInspect application."""
from typing import Dict, Any, cast, Optional
from typing_extensions import override
import pandas as pd
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QGroupBox, QFormLayout, QDialogButtonBox, QLineEdit, QWidget,
    QSplitter, QTabWidget, QMessageBox, QFrame
)
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import Qt

from src.data.models import DataSource, Visualization
from src.config import VISUALIZATION_TYPES, VISUALIZATION_COLORS
from src.gui.widgets.chart_view import ChartView


class VisualizationCreationDialog(QDialog):
    """Dialog for creating and configuring visualizations."""

    def __init__(self, data_source: DataSource, parent=None, existing_visualization: Optional[Visualization] = None) -> None:
        """Initialize the dialog.

        Args:
            data_source: The data source to create a visualization for
            parent: Parent widget
            existing_visualization: Optional existing visualization to edit
        """
        import logging
        logger = logging.getLogger(__name__)

        if existing_visualization:
            logger.info("Initialisiere VisualizationCreationDialog zum Bearbeiten von Visualisierung: %s", existing_visualization.name)
        else:
            logger.info("Initialisiere VisualizationCreationDialog für Datenquelle: %s", data_source.name)

        super().__init__(parent)
        self.data_source = data_source
        self.dataset = data_source.dataset
        self.existing_visualization = existing_visualization
        self.is_edit_mode = existing_visualization is not None

        # Ensure we have a dataset
        if self.dataset is None:
            raise ValueError("Data source must have a dataset")

        # Initialize visualization config
        if existing_visualization:
            # Use existing visualization's config
            self.visualization_config = {
                'name': existing_visualization.name,
                'chart_type': existing_visualization.chart_type,
                'x_axis': existing_visualization.config.get('x_axis', ''),
                'y_axes': existing_visualization.config.get('y_axes', []),
                'filter': existing_visualization.config.get('filter', {}),
                'aggregation': existing_visualization.config.get('aggregation', {}),
                'style': existing_visualization.config.get('style', {})
            }
        else:
            # Default visualization config for new visualization
            self.visualization_config = {
                'name': f"Visualisierung von {data_source.name}",
                'chart_type': 'bar',  # Default to bar chart
                'x_axis': '',
                'y_axes': [],  # List of y-axes with their colors
                'filter': {'columns': [], 'x_axis_filter': {}},
                'aggregation': {},
                'style': {}
            }

        # Track widgets
        self.y_axis_widgets = []
        self.column_filter_widgets = []
        self.x_filter_value_widgets = {}

        # Initialize UI elements that will be set up later
        self.chart_options_group = None
        self.chart_options_layout = None
        self.chart_options_placeholder = None
        self.name_edit = None
        self.x_axis_combo = None
        self.y_axes_container = None
        self.y_axes_container_layout = None
        self.y_axes_layout = None
        self.chart_type_buttons = {}
        self.config_tabs = None
        self.column_names = []

        # Filter tab elements
        self.column_filters_container = None
        self.column_filters_container_layout = None

        # Set up the UI
        try:
            self.setup_ui()
            logger.info("VisualizationCreationDialog UI erfolgreich initialisiert")

            # If we're in edit mode, load the existing visualization settings
            if self.is_edit_mode and self.existing_visualization:
                self.load_existing_visualization_settings()
                logger.info("Bestehende Visualisierungseinstellungen geladen")
        except Exception as e:
            import traceback
            logger.error("Fehler bei der Initialisierung der VisualizationCreationDialog UI: %s", str(e))
            logger.error("Traceback: %s", traceback.format_exc())
            raise

    def setup_ui(self) -> None:
        """Set up the user interface."""
        if self.is_edit_mode and self.existing_visualization:
            self.setWindowTitle(f"Visualisierung bearbeiten: {self.existing_visualization.name}")
        else:
            self.setWindowTitle("Neue Visualisierung erstellen")
        self.resize(900, 700)  # Set a reasonable initial size

        # Main layout
        main_layout = QVBoxLayout(self)

        # Top section: Basic info
        info_layout = QHBoxLayout()

        # Visualization name
        name_label = QLabel("Name:")
        self.name_edit = QLineEdit(str(self.visualization_config['name']))
        self.name_edit.setMinimumWidth(200)
        info_layout.addWidget(name_label)
        info_layout.addWidget(self.name_edit, 1)  # Stretch factor 1

        main_layout.addLayout(info_layout)

        # Main splitter (configuration on top, preview on bottom)
        main_splitter = QSplitter(Qt.Orientation.Vertical)

        # Top widget: Configuration
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)

        # Chart type selection
        chart_type_group = QGroupBox("Diagrammtyp")
        chart_type_layout = QVBoxLayout(chart_type_group)

        # Chart type selection as a horizontal layout of options
        chart_type_options = QHBoxLayout()

        # Add each chart type as a selectable option
        self.chart_type_buttons = {}
        for chart_type, chart_info in VISUALIZATION_TYPES.items():
            chart_button = QPushButton(f"{chart_info['icon']} {chart_info['name']}")
            chart_button.setCheckable(True)
            _ = chart_button.setProperty("chart_type", chart_type)
            chart_button.setToolTip(chart_info['description'])
            chart_button.setMinimumWidth(120)
            chart_button.setMinimumHeight(60)

            # Set the default selected chart type
            if chart_type == self.visualization_config['chart_type']:
                chart_button.setChecked(True)

            # Connect button to handler
            _ = chart_button.clicked.connect(self.on_chart_type_selected)

            # Add to layout and store reference
            chart_type_options.addWidget(chart_button)
            self.chart_type_buttons[chart_type] = chart_button

        chart_type_layout.addLayout(chart_type_options)
        top_layout.addWidget(chart_type_group)

        # Configuration tabs
        self.config_tabs = QTabWidget()

        # Data tab
        data_tab = QWidget()
        self.setup_data_tab(data_tab)
        _ = self.config_tabs.addTab(data_tab, "Daten")

        # Filter tab
        filter_tab = QWidget()
        self.setup_filter_tab(filter_tab)
        _ = self.config_tabs.addTab(filter_tab, "Filter")

        # Hinweis: Aggregation und Darstellung sind vorübergehend ausgeblendet
        # und werden in einer zukünftigen Version implementiert

        top_layout.addWidget(self.config_tabs)

        # Add the top widget to the main splitter
        main_splitter.addWidget(top_widget)

        # Bottom widget: Chart preview
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)

        # Add preview title
        preview_title = QLabel("Vorschau")
        preview_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        bottom_layout.addWidget(preview_title)

        # Add chart view
        self.chart_view = ChartView()
        bottom_layout.addWidget(self.chart_view)

        # Add the bottom widget to the main splitter
        main_splitter.addWidget(bottom_widget)

        # Set the size proportions (50% for config, 50% for preview)
        main_splitter.setSizes([350, 350])

        main_layout.addWidget(main_splitter)

        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )

        # Change OK button text based on mode
        ok_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        if ok_button:
            if self.is_edit_mode:
                ok_button.setText("Speichern")
            else:
                ok_button.setText("Erstellen")

        _ = button_box.accepted.connect(self.accept)
        _ = button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

    def setup_data_tab(self, parent_widget: QWidget) -> None:
        """Set up the data configuration tab.

        Args:
            parent_widget: The parent widget to attach the data controls to
        """
        import logging
        logger = logging.getLogger(__name__)
        logger.info("Initialisiere Daten-Tab")

        try:
            data_layout = QVBoxLayout(parent_widget)

            # Column selection group
            column_group = QGroupBox("Spaltenauswahl")
            column_layout = QVBoxLayout(column_group)

            # Get column names from dataset
            self.column_names = [] if self.dataset is None else self.dataset.data.columns.tolist()
            logger.debug("Spalten aus Datensatz geladen: %s", len(self.column_names))

            # X-axis selection
            x_axis_layout = QFormLayout()
            self.x_axis_combo = QComboBox()
            self.x_axis_combo.addItem("-- Bitte wählen --")
            self.x_axis_combo.addItems(self.column_names)
            _ = self.x_axis_combo.currentTextChanged.connect(self.on_x_axis_changed)
            x_axis_layout.addRow("X-Achse:", self.x_axis_combo)
            column_layout.addLayout(x_axis_layout)

            # Y-axes section
            y_axes_group = QGroupBox("Y-Achsen")
            self.y_axes_layout = QVBoxLayout(y_axes_group)

            # Container for Y-axis widgets
            self.y_axes_container = QWidget()
            self.y_axes_container_layout = QVBoxLayout(self.y_axes_container)
            self.y_axes_container_layout.setContentsMargins(0, 0, 0, 0)
            self.y_axes_container_layout.setSpacing(5)

            # Add initial Y-axis
            self.add_y_axis_widget()

            # Add button for adding more Y-axes
            add_y_button = QPushButton("+ Weitere Y-Achse hinzufügen")
            _ = add_y_button.clicked.connect(self.add_y_axis_widget)

            self.y_axes_layout.addWidget(self.y_axes_container)
            self.y_axes_layout.addWidget(add_y_button)

            column_layout.addWidget(y_axes_group)
            data_layout.addWidget(column_group)

            # Chart-specific options (will be updated based on selected chart type)
            self.chart_options_group = QGroupBox("Diagrammoptionen")
            self.chart_options_layout = QVBoxLayout(self.chart_options_group)

            # Placeholder for chart-specific options
            self.chart_options_placeholder = QLabel("Wählen Sie einen Diagrammtyp und Achsen, um die Optionen anzuzeigen.")
            self.chart_options_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.chart_options_layout.addWidget(self.chart_options_placeholder)

            data_layout.addWidget(self.chart_options_group)
            data_layout.addStretch()

            logger.info("Daten-Tab erfolgreich initialisiert")
        except Exception as e:
            import traceback
            logger.error("Fehler bei der Initialisierung des Daten-Tabs: %s", str(e))
            logger.error("Traceback: %s", traceback.format_exc())
            raise

    def add_y_axis_widget(self) -> None:
        """Add a new Y-axis selection widget."""
        import logging
        logger = logging.getLogger(__name__)

        # Create a frame for this Y-axis row
        y_axis_frame = QFrame()
        y_axis_frame.setFrameShape(QFrame.Shape.StyledPanel)
        y_axis_frame.setStyleSheet("QFrame { background-color: #2d2d2d; border-radius: 4px; }")

        y_axis_layout = QHBoxLayout(y_axis_frame)
        y_axis_layout.setContentsMargins(5, 5, 5, 5)

        # Y-axis selection
        y_axis_combo = QComboBox()
        y_axis_combo.addItem("-- Bitte wählen --")
        y_axis_combo.addItems(self.column_names)

        # Color selection - use different default colors based on the index
        default_colors = [
            VISUALIZATION_COLORS['Blau']['mittel'],    # First Y-axis: Blue
            VISUALIZATION_COLORS['Rot']['mittel'],     # Second Y-axis: Red
            VISUALIZATION_COLORS['Grün']['mittel'],    # Third Y-axis: Green
            VISUALIZATION_COLORS['Gelb']['mittel'],    # Fourth Y-axis: Yellow
            VISUALIZATION_COLORS['Orange']['mittel'],  # Fifth Y-axis: Orange
            VISUALIZATION_COLORS['Lila']['mittel'],    # Sixth Y-axis: Purple
            VISUALIZATION_COLORS['Grau']['mittel']     # Seventh Y-axis: Gray
        ]

        # Choose a default color based on the number of existing widgets
        widget_count = len(self.y_axis_widgets)
        default_color = default_colors[widget_count % len(default_colors)]

        color_button = QPushButton("Farbe wählen")
        color_button.setStyleSheet(f"background-color: {default_color}; color: white;")
        _ = color_button.setProperty("color_value", default_color)
        _ = color_button.clicked.connect(lambda: self.select_color(color_button))
        y_axis_layout.addWidget(color_button)

        logger.debug("Neue Y-Achse hinzugefügt mit Standardfarbe: %s", default_color)

        # Connect the combo box change event after setting up the color
        _ = y_axis_combo.currentTextChanged.connect(self.on_y_axes_changed)
        y_axis_layout.addWidget(QLabel("Spalte:"))
        y_axis_layout.addWidget(y_axis_combo, 1)  # Stretch factor 1

        # Remove button (only for additional Y-axes)
        remove_button = QPushButton("×")
        remove_button.setToolTip("Entfernen")
        remove_button.setFixedSize(24, 24)
        remove_button.setStyleSheet("""
            QPushButton {
                border: none;
                color: #aaa;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                color: #fff;
                background-color: #d32f2f;
                border-radius: 12px;
            }
        """)

        # Only enable remove button if this is not the first Y-axis
        remove_button.setEnabled(len(self.y_axis_widgets) > 0)
        _ = remove_button.clicked.connect(lambda: self.remove_y_axis_widget(y_axis_frame))
        y_axis_layout.addWidget(remove_button)

        # Add to container
        if self.y_axes_container_layout is not None:
            self.y_axes_container_layout.addWidget(y_axis_frame)
        else:
            logger.error("y_axes_container_layout ist nicht initialisiert")

        # Store references to widgets
        self.y_axis_widgets.append({
            'frame': y_axis_frame,
            'combo': y_axis_combo,
            'color_button': color_button,
            'remove_button': remove_button
        })

        # Update the configuration
        self.on_y_axes_changed()

    def remove_y_axis_widget(self, frame: QFrame) -> None:
        """Remove a Y-axis widget.

        Args:
            frame: The frame widget to remove
        """
        import logging
        logger = logging.getLogger(__name__)

        # Find the widget in our list
        for i, widget_data in enumerate(self.y_axis_widgets):
            if widget_data.get('frame') == frame:
                # Remove from layout and delete
                if self.y_axes_container_layout is not None:
                    self.y_axes_container_layout.removeWidget(frame)
                    frame.deleteLater()
                else:
                    logger.error("y_axes_container_layout ist nicht initialisiert")

                # Remove from our list
                self.y_axis_widgets.pop(i)

                # If we removed all Y-axes and we're not in the process of loading settings,
                # add a new empty one to ensure there's always at least one Y-axis widget
                if not self.y_axis_widgets and not getattr(self, '_loading_settings', False):
                    logger.debug("Alle Y-Achsen wurden entfernt, füge eine neue leere hinzu")
                    self.add_y_axis_widget()

                break

        # Update the configuration
        self.on_y_axes_changed()

    def select_color(self, button: QPushButton) -> None:
        """Open color selection dialog.

        Args:
            button: The color button that was clicked
        """
        # Create a dialog for color selection
        color_dialog = QDialog(self)
        color_dialog.setWindowTitle("Farbe auswählen")
        color_dialog.setMinimumWidth(400)

        dialog_layout = QVBoxLayout(color_dialog)

        # Create a grid of color buttons
        color_grid = QVBoxLayout()

        # Add each color group
        for color_group, shades in VISUALIZATION_COLORS.items():
            group_layout = QHBoxLayout()
            group_layout.addWidget(QLabel(f"{color_group}:"))

            for shade_name, color_value in shades.items():
                shade_button = QPushButton()
                shade_button.setFixedSize(30, 30)
                shade_button.setStyleSheet(f"background-color: {color_value}; border: none;")
                shade_button.setToolTip(f"{color_group} ({shade_name})")

                # Connect button to color selection
                _ = shade_button.clicked.connect(
                    lambda checked=False, value=color_value, btn=button: self.apply_color(value, btn, color_dialog)
                )

                group_layout.addWidget(shade_button)

            color_grid.addLayout(group_layout)

        dialog_layout.addLayout(color_grid)

        # Add cancel button
        cancel_button = QPushButton("Abbrechen")
        _ = cancel_button.clicked.connect(color_dialog.reject)
        dialog_layout.addWidget(cancel_button)

        # Show the dialog
        _ = color_dialog.exec()

    def apply_color(self, color_value: str, button: QPushButton, dialog: QDialog) -> None:
        """Apply the selected color to the button.

        Args:
            color_value: The color value to apply
            button: The button to apply the color to
            dialog: The dialog to close
        """
        # Update button style
        button.setStyleSheet(f"background-color: {color_value}; color: white;")
        _ = button.setProperty("color_value", color_value)

        # Close the dialog
        dialog.accept()

        # Update the configuration
        self.on_y_axes_changed()

    def on_x_axis_changed(self, _: str) -> None:
        """Handle changes to X-axis selection."""
        import logging
        logger = logging.getLogger(__name__)

        # Ensure x_axis_combo is initialized
        if self.x_axis_combo is None:
            logger.warning("x_axis_combo ist nicht initialisiert, überspringe Update")
            return

        # Update the configuration
        try:
            self.visualization_config['x_axis'] = self.x_axis_combo.currentText()
            if self.visualization_config['x_axis'] == "-- Bitte wählen --":
                self.visualization_config['x_axis'] = ""

            logger.debug("X-Achse geändert zu: %s", self.visualization_config['x_axis'])
        except Exception as e:
            logger.error("Fehler beim Aktualisieren der X-Achse: %s", str(e))
            return

        # Update chart-specific options
        self.update_chart_options()

    def on_y_axes_changed(self) -> None:
        """Handle changes to Y-axes selections."""
        import logging
        logger = logging.getLogger(__name__)

        # Ensure y_axis_widgets is initialized
        if not hasattr(self, 'y_axis_widgets') or self.y_axis_widgets is None:
            logger.warning("y_axis_widgets ist nicht initialisiert, überspringe Update")
            return

        # Update the configuration with all Y-axes
        try:
            y_axes = []

            for i, widget_data in enumerate(self.y_axis_widgets):
                combo = widget_data.get('combo')
                color_button = widget_data.get('color_button')

                if combo is None or color_button is None:
                    continue

                column = combo.currentText()
                if column != "-- Bitte wählen --":
                    color = color_button.property("color_value")
                    # Ensure we have a valid color value
                    if not color:
                        logger.warning("Keine Farbwert für Y-Achse %d gefunden, verwende Standard", i)
                        color = '#3D78D6'  # Default blue

                    y_axes.append({
                        'column': column,
                        'color': color
                    })
                    logger.debug("Y-Achse %d: Spalte=%s, Farbe=%s", i, column, color)

            # Check if we're in loading mode to avoid unnecessary updates
            if not getattr(self, '_loading_settings', False):
                # Compare with previous configuration to detect changes
                old_y_axes = self.visualization_config.get('y_axes', [])

                # Check if the configuration has changed
                has_changed = False

                if len(old_y_axes) != len(y_axes):
                    has_changed = True
                else:
                    # Compare each y-axis configuration
                    for i, (old_axis, new_axis) in enumerate(zip(old_y_axes, y_axes)):
                        if isinstance(old_axis, dict) and isinstance(new_axis, dict):
                            if old_axis.get('column') != new_axis.get('column') or old_axis.get('color') != new_axis.get('color'):
                                has_changed = True
                                break

                if has_changed:
                    logger.debug("Y-Achsen-Konfiguration hat sich geändert")
                    logger.debug("Alt: %s", old_y_axes)
                    logger.debug("Neu: %s", y_axes)

            self.visualization_config['y_axes'] = y_axes
            logger.debug("Y-Achsen aktualisiert, Anzahl: %s", len(y_axes))
        except Exception as e:
            logger.error("Fehler beim Aktualisieren der Y-Achsen: %s", str(e))
            return

        # Update chart-specific options
        self.update_chart_options()

    def on_chart_type_selected(self) -> None:
        """Handle selection of a chart type."""
        import logging
        logger = logging.getLogger(__name__)

        try:
            # Find which button was clicked
            sender = self.sender()
            if not isinstance(sender, QPushButton):
                logger.warning("Sender ist kein QPushButton")
                return

            chart_type = sender.property("chart_type")
            if not chart_type:
                logger.warning("Kein chart_type in der Eigenschaft gefunden")
                return

            # Update the selected chart type
            self.visualization_config['chart_type'] = chart_type
            logger.debug("Diagrammtyp geändert zu: %s", chart_type)

            # Ensure chart_type_buttons is initialized
            if not hasattr(self, 'chart_type_buttons') or not self.chart_type_buttons:
                logger.warning("chart_type_buttons ist nicht initialisiert, überspringe UI-Update")
            else:
                # Update UI to reflect the selection
                for btn_type, button in self.chart_type_buttons.items():
                    button.setChecked(btn_type == chart_type)
        except Exception as e:
            logger.error("Fehler beim Aktualisieren des Diagrammtyps: %s", str(e))
            return

        # Update chart-specific options
        self.update_chart_options()

    def setup_filter_tab(self, parent_widget: QWidget) -> None:
        """Set up the filter configuration tab.

        Args:
            parent_widget: The parent widget to attach the filter controls to
        """
        import logging
        logger = logging.getLogger(__name__)
        logger.info("Initialisiere Filter-Tab")

        try:
            filter_layout = QVBoxLayout(parent_widget)

            # Hinweis zur Filterlogik
            filter_info = QLabel("Hinweis: Ab dem zweiten Filter kann pro Filter gewählt werden, ob dieser mit UND oder ODER verknüpft wird.")
            filter_info.setWordWrap(True)
            filter_layout.addWidget(filter_info)

            # Column filters section
            column_filters_group = QGroupBox("Spaltenfilter")
            column_filters_layout = QVBoxLayout(column_filters_group)

            # Container for column filter widgets
            self.column_filters_container = QWidget()
            self.column_filters_container_layout = QVBoxLayout(self.column_filters_container)
            self.column_filters_container_layout.setContentsMargins(0, 0, 0, 0)
            self.column_filters_container_layout.setSpacing(5)

            # Add button for adding column filters
            add_filter_button = QPushButton("+ Filter hinzufügen")
            _ = add_filter_button.clicked.connect(self.add_column_filter_widget)

            column_filters_layout.addWidget(self.column_filters_container)
            column_filters_layout.addWidget(add_filter_button)

            filter_layout.addWidget(column_filters_group)

            # Hinweis: X-Achsenfilter wurden in die Spaltenfilter integriert
            filter_layout.addStretch()

            # Add initial column filter if none exists
            if not self.column_filter_widgets:
                self.add_column_filter_widget()

            # Load existing filter settings if available
            if self.is_edit_mode and self.existing_visualization:
                self.load_filter_settings()

            _ = logger.info("Filter-Tab erfolgreich initialisiert")
        except Exception as e:
            import traceback
            logger.error("Fehler bei der Initialisierung des Filter-Tabs: %s", str(e))
            logger.error("Traceback: %s", traceback.format_exc())
            raise

    def add_column_filter_widget(self) -> None:
        """Add a new column filter widget."""
        import logging
        logger = logging.getLogger(__name__)

        # Create a frame for this filter row
        filter_frame = QFrame()
        filter_frame.setFrameShape(QFrame.Shape.StyledPanel)
        filter_frame.setStyleSheet("QFrame { background-color: #2d2d2d; border-radius: 4px; }")

        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(5, 5, 5, 5)
        filter_layout.setSpacing(5)  # Reduzierter Abstand zwischen Elementen

        # Verknüpfungslogik (UND/ODER) - nur ab dem zweiten Filter anzeigen
        logic_combo = QComboBox()
        logic_combo.addItem("UND")
        logic_combo.addItem("ODER")
        # Keine feste Breite, damit der Text vollständig angezeigt wird
        logic_combo.setMinimumWidth(90)  # Mindestbreite für bessere Lesbarkeit
        logic_combo.setStyleSheet("QComboBox { padding-left: 5px; }")  # Mehr Platz für Text und Checkbox
        logic_combo.setToolTip("UND: Dieser Filter muss zusätzlich zutreffen\nODER: Dieser Filter ist eine Alternative")
        _ = logic_combo.currentTextChanged.connect(self.update_filter_config)

        # Nur anzeigen, wenn es nicht der erste Filter ist
        if len(self.column_filter_widgets) > 0:
            filter_layout.addWidget(logic_combo)
        else:
            # Platzhalter für den ersten Filter, damit das Layout konsistent bleibt
            logic_combo.setVisible(False)
            filter_layout.addWidget(logic_combo)

        # Column selection
        column_combo = QComboBox()
        column_combo.addItem("-- Bitte wählen --")
        column_combo.addItems(self.column_names)
        _ = column_combo.currentTextChanged.connect(self.on_filter_column_changed)

        # Kompakteres Layout ohne feste Breiten für die Labels
        column_label = QLabel("Spalte:")
        # Keine feste Breite, damit der Text vollständig angezeigt wird
        filter_layout.addWidget(column_label)
        column_combo.setMinimumWidth(120)  # Mindestbreite für die Spaltenauswahl
        filter_layout.addWidget(column_combo, 2)  # Stretch factor 2

        # Filter type selection (will be updated based on column data type)
        filter_type_combo = QComboBox()
        filter_type_combo.addItem("-- Bitte wählen --")
        _ = filter_type_combo.currentTextChanged.connect(self.on_filter_type_changed)

        # Kompakteres Layout ohne feste Breiten für die Labels
        type_label = QLabel("Filtertyp:")
        # Keine feste Breite, damit der Text vollständig angezeigt wird
        filter_layout.addWidget(type_label)
        filter_type_combo.setMinimumWidth(120)  # Mindestbreite für die Filtertyp-Auswahl
        filter_layout.addWidget(filter_type_combo, 2)  # Stretch factor 2

        # Filter value container (will be updated based on filter type)
        filter_value_container = QWidget()
        filter_value_layout = QHBoxLayout(filter_value_container)  # Horizontal statt vertikal
        filter_value_layout.setContentsMargins(0, 0, 0, 0)
        filter_value_layout.setSpacing(5)  # Reduzierter Abstand
        filter_value_container.setMinimumWidth(150)  # Mindestbreite für den Wert-Container
        filter_layout.addWidget(filter_value_container, 4)  # Erhöhter Stretch-Faktor für mehr Platz

        # Remove button
        remove_button = QPushButton("×")
        remove_button.setToolTip("Entfernen")
        remove_button.setFixedSize(24, 24)
        remove_button.setStyleSheet("""
            QPushButton {
                border: none;
                color: #aaa;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                color: #fff;
                background-color: #d32f2f;
                border-radius: 12px;
            }
        """)
        _ = remove_button.clicked.connect(lambda: self.remove_column_filter_widget(filter_frame))
        filter_layout.addWidget(remove_button)

        # Add to container
        if self.column_filters_container_layout is not None:
            self.column_filters_container_layout.addWidget(filter_frame)
        else:
            logger.error("column_filters_container_layout ist nicht initialisiert")

        # Store references to widgets
        self.column_filter_widgets.append({
            'frame': filter_frame,
            'logic_combo': logic_combo,
            'column_combo': column_combo,
            'filter_type_combo': filter_type_combo,
            'value_container': filter_value_container,
            'value_layout': filter_value_layout,
            'remove_button': remove_button,
            'value_widgets': {}  # Will store references to value input widgets
        })

        # Update the configuration
        self.update_filter_config()

    def remove_column_filter_widget(self, frame: QFrame) -> None:
        """Remove a column filter widget.

        Args:
            frame: The frame widget to remove
        """
        import logging
        logger = logging.getLogger(__name__)

        # Find the widget in our list
        for i, widget_data in enumerate(self.column_filter_widgets):
            if widget_data.get('frame') == frame:
                # Remove from layout and delete
                if self.column_filters_container_layout is not None:
                    self.column_filters_container_layout.removeWidget(frame)
                    frame.deleteLater()
                else:
                    logger.error("column_filters_container_layout ist nicht initialisiert")

                # Remove from our list
                self.column_filter_widgets.pop(i)
                break

        # Update the configuration
        self.update_filter_config()

    def on_filter_column_changed(self, column_name: str) -> None:
        """Handle changes to filter column selection.

        Args:
            column_name: The selected column name
        """
        import logging
        logger = logging.getLogger(__name__)

        # Find the widget that triggered this event
        sender = self.sender()
        for widget_data in self.column_filter_widgets:
            if widget_data.get('column_combo') == sender:
                # Update filter type options based on column data type
                filter_type_combo = widget_data.get('filter_type_combo')
                if filter_type_combo is None:
                    _ = logger.warning("filter_type_combo ist None")
                    continue

                # Clear current options
                filter_type_combo.clear()
                filter_type_combo.addItem("-- Bitte wählen --")

                # Add options based on column data type
                if column_name != "-- Bitte wählen --" and self.dataset is not None:
                    column_data = self.dataset.data[column_name]

                    # Check if it's a year column (4-digit integer values)
                    is_year = False
                    if pd.api.types.is_numeric_dtype(column_data):
                        # Check if values are mostly 4-digit integers (years)
                        sample = column_data.dropna().astype(int).astype(str)
                        if len(sample) > 0:
                            year_pattern = sample.str.match(r'^\d{4}$')
                            if year_pattern.mean() > 0.8:  # If more than 80% match year pattern
                                is_year = True

                    # Allgemeine Filter für alle Spaltentypen
                    filter_type_combo.addItem("Jeden n-ten Wert")
                    filter_type_combo.addItem("Bestimmte Werte")
                    filter_type_combo.addItem("Erste n Werte")
                    filter_type_combo.addItem("Letzte n Werte")

                    if is_year:
                        # Year column
                        filter_type_combo.addItem("Gleich")
                        filter_type_combo.addItem("Größer als")
                        filter_type_combo.addItem("Kleiner als")
                        filter_type_combo.addItem("Zwischen")
                        filter_type_combo.addItem("Erste n Jahre")
                        filter_type_combo.addItem("Letzte n Jahre")
                    elif pd.api.types.is_numeric_dtype(column_data):
                        # Numeric column
                        filter_type_combo.addItem("Gleich")
                        filter_type_combo.addItem("Größer als")
                        filter_type_combo.addItem("Kleiner als")
                        filter_type_combo.addItem("Zwischen")
                        filter_type_combo.addItem("Teilbar durch")
                    elif pd.api.types.is_datetime64_dtype(column_data):
                        # Date column
                        filter_type_combo.addItem("Gleich")
                        filter_type_combo.addItem("Nach")
                        filter_type_combo.addItem("Vor")
                        filter_type_combo.addItem("Zwischen")
                    else:
                        # Text column
                        filter_type_combo.addItem("Enthält")
                        filter_type_combo.addItem("Gleich")
                        filter_type_combo.addItem("Beginnt mit")
                        filter_type_combo.addItem("Endet mit")

                break

        # Update the configuration
        self.update_filter_config()

    def on_filter_type_changed(self, filter_type: str) -> None:
        """Handle changes to filter type selection.

        Args:
            filter_type: The selected filter type
        """
        import logging
        logger = logging.getLogger(__name__)
        _ = logger.debug(f"Filtertyp geändert: {filter_type}")

        # Find the widget that triggered this event
        sender = self.sender()
        for widget_data in self.column_filter_widgets:
            if widget_data.get('filter_type_combo') == sender:
                # Update filter value widgets based on filter type
                value_layout = widget_data.get('value_layout')
                value_container = widget_data.get('value_container')
                if value_layout is None or value_container is None:
                    _ = logger.warning("value_layout oder value_container ist None")
                    continue

                # Clear current value widgets
                while value_layout.count():
                    item = value_layout.takeAt(0)
                    widget = item.widget() if item is not None else None
                    if widget is not None:
                        widget.deleteLater()
                widget_data['value_widgets'] = {}

                # Add value widgets based on filter type
                if filter_type == "Zwischen":
                    # Two value inputs for between filter
                    von_label = QLabel("Von:")
                    # Keine feste Breite, damit der Text vollständig angezeigt wird
                    value_layout.addWidget(von_label)

                    min_value = QLineEdit()
                    min_value.setValidator(QIntValidator())
                    min_value.setPlaceholderText("Min")
                    min_value.setMinimumWidth(60)  # Mindestbreite
                    # Kein setFixedWidth, damit das Feld den verfügbaren Platz nutzt
                    value_layout.addWidget(min_value, 1)  # Stretch-Faktor 1

                    bis_label = QLabel("Bis:")
                    # Keine feste Breite, damit der Text vollständig angezeigt wird
                    value_layout.addWidget(bis_label)

                    max_value = QLineEdit()
                    max_value.setValidator(QIntValidator())
                    max_value.setPlaceholderText("Max")
                    max_value.setMinimumWidth(60)  # Mindestbreite
                    # Kein setFixedWidth, damit das Feld den verfügbaren Platz nutzt
                    value_layout.addWidget(max_value, 1)  # Stretch-Faktor 1

                    widget_data['value_widgets'] = {
                        'min_value': min_value,
                        'max_value': max_value
                    }

                    # Connect to update config
                    _ = min_value.textChanged.connect(self.update_filter_config)
                    _ = max_value.textChanged.connect(self.update_filter_config)
                elif filter_type == "Jeden n-ten Wert":
                    # Kompaktes Layout
                    n_label = QLabel("n:")
                    # Keine feste Breite, damit der Text vollständig angezeigt wird
                    value_layout.addWidget(n_label)

                    n_value = QLineEdit()
                    n_value.setValidator(QIntValidator(1, 1000))
                    n_value.setPlaceholderText("z.B. 5")
                    n_value.setMinimumWidth(60)  # Mindestbreite
                    # Kein setFixedWidth, damit das Feld den verfügbaren Platz nutzt
                    value_layout.addWidget(n_value, 1)  # Stretch-Faktor 1, um den verfügbaren Platz zu nutzen

                    widget_data['value_widgets'] = {
                        'n_value': n_value
                    }

                    # Connect to update config
                    _ = n_value.textChanged.connect(self.update_filter_config)
                elif filter_type == "Bestimmte Werte":
                    # Kompaktes Layout
                    werte_label = QLabel("Werte:")
                    # Keine feste Breite, damit der Text vollständig angezeigt wird
                    value_layout.addWidget(werte_label)

                    values_input = QLineEdit()
                    values_input.setPlaceholderText("z.B. Wert1, Wert2, Wert3")
                    values_input.setMinimumWidth(120)  # Mindestbreite
                    # Kein setFixedWidth, damit das Feld den verfügbaren Platz nutzt
                    value_layout.addWidget(values_input, 1)  # Stretch-Faktor 1, um den verfügbaren Platz zu nutzen

                    widget_data['value_widgets'] = {
                        'values': values_input
                    }

                    # Connect to update config
                    _ = values_input.textChanged.connect(self.update_filter_config)
                elif filter_type in ["Erste n Werte", "Letzte n Werte", "Erste n Jahre", "Letzte n Jahre", "Teilbar durch"]:
                    # Kompaktes Layout
                    wert_label = QLabel("Wert:")
                    # Keine feste Breite, damit der Text vollständig angezeigt wird
                    value_layout.addWidget(wert_label)

                    value_input = QLineEdit()
                    value_input.setValidator(QIntValidator(1, 1000))
                    if filter_type in ["Erste n Werte", "Letzte n Werte"]:
                        value_input.setPlaceholderText("z.B. 10")
                    elif filter_type == "Teilbar durch":
                        value_input.setPlaceholderText("z.B. 5")
                    value_input.setMinimumWidth(60)  # Mindestbreite
                    # Kein setFixedWidth, damit das Feld den verfügbaren Platz nutzt
                    value_layout.addWidget(value_input, 1)  # Stretch-Faktor 1, um den verfügbaren Platz zu nutzen

                    widget_data['value_widgets'] = {
                        'n_value': value_input
                    }

                    # Connect to update config
                    _ = value_input.textChanged.connect(self.update_filter_config)
                elif filter_type != "-- Bitte wählen --":
                    # Single value input for other filter types
                    wert_label = QLabel("Wert:")
                    # Keine feste Breite, damit der Text vollständig angezeigt wird
                    value_layout.addWidget(wert_label)

                    value_input = QLineEdit()
                    if filter_type in ["Größer als", "Kleiner als", "Gleich"]:
                        value_input.setValidator(QIntValidator())
                    value_input.setMinimumWidth(80)  # Mindestbreite
                    # Kein setFixedWidth, damit das Feld den verfügbaren Platz nutzt
                    value_layout.addWidget(value_input, 1)  # Stretch-Faktor 1, um den verfügbaren Platz zu nutzen

                    widget_data['value_widgets'] = {
                        'value': value_input
                    }

                    # Connect to update config
                    _ = value_input.textChanged.connect(self.update_filter_config)

                break

        # Update the configuration
        self.update_filter_config()

    # Die Methode on_x_filter_type_changed wurde entfernt, da X-Achsenfilter
    # jetzt in die Spaltenfilter integriert sind

    def update_filter_config(self) -> None:
        """Update the filter configuration based on UI inputs."""
        import logging
        logger = logging.getLogger(__name__)

        try:
            # Initialize filter configuration
            filter_config: Dict[str, Any] = {
                'columns': []
            }

            # Collect column filter configurations
            for i, widget_data in enumerate(self.column_filter_widgets):
                column_combo = widget_data.get('column_combo')
                filter_type_combo = widget_data.get('filter_type_combo')
                logic_combo = widget_data.get('logic_combo')
                value_widgets = widget_data.get('value_widgets', {})

                if column_combo is None or filter_type_combo is None:
                    continue

                column = column_combo.currentText()
                filter_type_text = filter_type_combo.currentText()

                if column == "-- Bitte wählen --" or filter_type_text == "-- Bitte wählen --":
                    continue

                # Bestimme die Verknüpfungslogik (UND/ODER) für diesen Filter
                # Der erste Filter hat keine Logik, ab dem zweiten Filter kann gewählt werden
                logic = 'and'  # Standard ist UND
                if i > 0 and logic_combo is not None:
                    logic_text = logic_combo.currentText()
                    if logic_text == "ODER":
                        logic = 'or'

                # Determine filter type and operator
                data_type = 'text'
                operator = 'contains'

                if filter_type_text == "Gleich":
                    operator = 'equals'
                elif filter_type_text == "Größer als":
                    operator = 'greater_than'
                    data_type = 'numeric'
                elif filter_type_text == "Kleiner als":
                    operator = 'less_than'
                    data_type = 'numeric'
                elif filter_type_text == "Zwischen":
                    operator = 'between'
                    data_type = 'numeric'
                elif filter_type_text == "Teilbar durch":
                    operator = 'divisible_by'
                    data_type = 'numeric'
                elif filter_type_text == "Nach":
                    operator = 'after'
                    data_type = 'date'
                elif filter_type_text == "Vor":
                    operator = 'before'
                    data_type = 'date'
                elif filter_type_text == "Enthält":
                    operator = 'contains'
                elif filter_type_text == "Beginnt mit":
                    operator = 'starts_with'
                elif filter_type_text == "Endet mit":
                    operator = 'ends_with'
                elif filter_type_text == "Erste n Jahre":
                    operator = 'first_n'
                    data_type = 'year'
                elif filter_type_text == "Letzte n Jahre":
                    operator = 'last_n'
                    data_type = 'year'
                elif filter_type_text == "Jeden n-ten Wert":
                    operator = 'every_nth'
                    data_type = 'numeric'
                elif filter_type_text == "Bestimmte Werte":
                    operator = 'specific_values'
                    data_type = 'text'
                elif filter_type_text == "Erste n Werte":
                    operator = 'first_n'
                    data_type = 'numeric'
                elif filter_type_text == "Letzte n Werte":
                    operator = 'last_n'
                    data_type = 'numeric'

                # Get values from widgets
                value = None
                value2 = None

                if 'value' in value_widgets:
                    value = value_widgets['value'].text()
                if 'min_value' in value_widgets and 'max_value' in value_widgets:
                    value = value_widgets['min_value'].text()
                    value2 = value_widgets['max_value'].text()
                if 'values' in value_widgets:
                    value = value_widgets['values'].text()
                if 'n_value' in value_widgets:
                    value = value_widgets['n_value'].text()

                # Add filter configuration
                if isinstance(filter_config['columns'], list):
                    filter_config['columns'].append({
                        'column': column,
                        'type': data_type,
                        'operator': operator,
                        'value': value,
                        'value2': value2,
                        'logic': logic  # Speichere die Verknüpfungslogik pro Filter
                    })

            # Update the visualization configuration
            self.visualization_config['filter'] = filter_config
            logger.debug("Filter-Konfiguration aktualisiert: %s", filter_config)

            # Update chart preview
            self.update_chart_preview()
        except Exception as e:
            logger.error("Fehler beim Aktualisieren der Filter-Konfiguration: %s", str(e))
            import traceback
            logger.error("Traceback: %s", traceback.format_exc())

    def load_filter_settings(self) -> None:
        """Load filter settings from an existing visualization."""
        import logging
        logger = logging.getLogger(__name__)

        if not self.is_edit_mode or not self.existing_visualization:
            return

        try:
            # Get filter configuration from existing visualization
            filter_config = self.existing_visualization.config.get('filter', {})
            if not filter_config:
                return

            logger.debug("Lade Filter-Konfiguration: %s", filter_config)

            # Load column filters
            column_filters = filter_config.get('columns', [])

            # Remove any existing column filter widgets
            while self.column_filter_widgets:
                widget_data = self.column_filter_widgets[0]
                frame = widget_data.get('frame')
                if frame:
                    self.remove_column_filter_widget(frame)

            # Add column filter widgets for each filter in the configuration
            for column_filter in column_filters:
                # Add a new filter widget
                self.add_column_filter_widget()

                # Get the last added widget
                widget_data = self.column_filter_widgets[-1]

                # Set column
                column_combo = widget_data.get('column_combo')
                if column_combo and 'column' in column_filter:
                    column_name = column_filter['column']
                    index = column_combo.findText(column_name)
                    if index >= 0:
                        column_combo.setCurrentIndex(index)

                # Set filter type
                filter_type_combo = widget_data.get('filter_type_combo')
                if filter_type_combo:
                    data_type = column_filter.get('type', '')
                    operator = column_filter.get('operator', '')

                    # Map operator and data type to filter type text
                    filter_type_text = "-- Bitte wählen --"

                    if operator == 'equals':
                        filter_type_text = "Gleich"
                    elif operator == 'greater_than' and data_type in ['numeric', 'year']:
                        filter_type_text = "Größer als"
                    elif operator == 'less_than' and data_type in ['numeric', 'year']:
                        filter_type_text = "Kleiner als"
                    elif operator == 'between' and data_type in ['numeric', 'year', 'date']:
                        filter_type_text = "Zwischen"
                    elif operator == 'divisible_by' and data_type == 'numeric':
                        filter_type_text = "Teilbar durch"
                    elif operator == 'after' and data_type == 'date':
                        filter_type_text = "Nach"
                    elif operator == 'before' and data_type == 'date':
                        filter_type_text = "Vor"
                    elif operator == 'contains' and data_type == 'text':
                        filter_type_text = "Enthält"
                    elif operator == 'starts_with' and data_type == 'text':
                        filter_type_text = "Beginnt mit"
                    elif operator == 'ends_with' and data_type == 'text':
                        filter_type_text = "Endet mit"
                    elif operator == 'first_n' and data_type == 'year':
                        filter_type_text = "Erste n Jahre"
                    elif operator == 'last_n' and data_type == 'year':
                        filter_type_text = "Letzte n Jahre"
                    elif operator == 'every_nth' and data_type == 'numeric':
                        filter_type_text = "Jeden n-ten Wert"
                    elif operator == 'specific_values' and data_type == 'text':
                        filter_type_text = "Bestimmte Werte"
                    elif operator == 'first_n' and data_type == 'numeric':
                        filter_type_text = "Erste n Werte"
                    elif operator == 'last_n' and data_type == 'numeric':
                        filter_type_text = "Letzte n Werte"

                    # Find and select the filter type
                    index = filter_type_combo.findText(filter_type_text)
                    if index >= 0:
                        filter_type_combo.setCurrentIndex(index)

                # Set filter values
                value_widgets = widget_data.get('value_widgets', {})
                value = column_filter.get('value')
                value2 = column_filter.get('value2')

                if 'value' in value_widgets and value is not None:
                    value_widgets['value'].setText(str(value))
                if 'min_value' in value_widgets and value is not None:
                    value_widgets['min_value'].setText(str(value))
                if 'max_value' in value_widgets and value2 is not None:
                    value_widgets['max_value'].setText(str(value2))

            # Lade die Verknüpfungslogik für jeden Filter
            for i, widget_data in enumerate(self.column_filter_widgets):
                if i > 0:  # Der erste Filter hat keine Logik
                    logic_combo = widget_data.get('logic_combo')
                    if logic_combo is not None:
                        # Hole die Logik aus dem Filter (falls vorhanden)
                        if i-1 < len(column_filters):
                            filter_logic = column_filters[i-1].get('logic', 'and')
                            logic_text = "UND" if filter_logic == 'and' else "ODER"
                            index = logic_combo.findText(logic_text)
                            if index >= 0:
                                logic_combo.setCurrentIndex(index)

            logger.info("Filter-Einstellungen erfolgreich geladen")
        except Exception as e:
            logger.error("Fehler beim Laden der Filter-Einstellungen: %s", str(e))
            import traceback
            logger.error("Traceback: %s", traceback.format_exc())

    def update_chart_preview(self) -> None:
        """Update the chart preview based on the current configuration."""
        import logging
        logger = logging.getLogger(__name__)

        # Ensure we have a chart view
        if not hasattr(self, 'chart_view'):
            logger.warning("chart_view ist nicht initialisiert, überspringe Vorschau-Update")
            return

        # Ensure we have a dataset
        if not self.dataset:
            logger.warning("Kein Dataset vorhanden, überspringe Vorschau-Update")
            return

        # Get current configuration
        chart_type = self.visualization_config['chart_type']
        x_axis = self.visualization_config['x_axis']
        y_axes = self.visualization_config['y_axes']

        # Check if we have enough data to render a preview
        if not x_axis or not y_axes:
            logger.debug("Nicht genügend Daten für Vorschau, X-Achse: %s, Y-Achsen: %s", x_axis, len(y_axes))
            self.chart_view.clear_chart()
            return

        try:
            # Create a config for the preview
            preview_config = {
                'name': self.visualization_config['name'],
                'x_axis': x_axis,
                'y_axes': y_axes,
                'filter': self.visualization_config.get('filter', {}),
                'aggregation': self.visualization_config.get('aggregation', {}),
                'style': self.visualization_config.get('style', {})
            }

            # Display the preview
            logger.debug("Aktualisiere Diagramm-Vorschau")
            self.chart_view.display_preview(self.dataset, preview_config, str(chart_type))

        except Exception as e:
            logger.error("Fehler beim Aktualisieren der Diagramm-Vorschau: %s", str(e))
            import traceback
            logger.error("Traceback: %s", traceback.format_exc())

            # Clear the chart view in case of error
            self.chart_view.clear_chart()



    def update_chart_options(self) -> None:
        """Update the chart-specific options based on the selected chart type and axes."""
        import logging
        logger = logging.getLogger(__name__)

        # Ensure chart_options_layout is initialized
        if self.chart_options_layout is None:
            logger.warning("chart_options_layout ist nicht initialisiert, überspringe Update")
            return

        # Clear existing options
        try:
            while self.chart_options_layout.count():
                item = self.chart_options_layout.takeAt(0)
                widget = item.widget() if item is not None else None
                if widget is not None:
                    widget.deleteLater()
        except Exception as e:
            logger.error("Fehler beim Löschen der bestehenden Optionen: %s", str(e))
            return

        chart_type = self.visualization_config['chart_type']
        x_axis = self.visualization_config['x_axis']
        y_axes = self.visualization_config['y_axes']

        logger.debug("Update chart options - Typ: %s, X-Achse: %s, Y-Achsen: %s",
                    chart_type, x_axis, len(y_axes))

        # Check if chart type supports multiple Y-axes
        chart_info = VISUALIZATION_TYPES.get(str(chart_type), {})
        supports_multiple_y = bool(chart_info.get('supports_multiple_y', False))

        # If we have multiple Y-axes but the chart type doesn't support it, show warning
        if len(y_axes) > 1 and not supports_multiple_y:
            chart_name = VISUALIZATION_TYPES.get(str(chart_type), {}).get('name', str(chart_type))
            warning_label = QLabel(f"Achtung: {chart_name} unterstützt nur eine Y-Achse. "
                                  "Nur die erste ausgewählte Y-Achse wird verwendet.")
            warning_label.setStyleSheet("color: #FFD700;")  # Gold color for warning
            warning_label.setWordWrap(True)
            self.chart_options_layout.addWidget(warning_label)

        # If axes are not selected, show placeholder
        if not x_axis or not y_axes:
            self.chart_options_placeholder = QLabel("Wählen Sie X- und mindestens eine Y-Achse, um die Optionen anzuzeigen.")
            self.chart_options_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.chart_options_layout.addWidget(self.chart_options_placeholder)

            # Clear chart preview
            if hasattr(self, 'chart_view'):
                self.chart_view.clear_chart()

            return

        # Update chart preview
        self.update_chart_preview()

        # Add chart-specific options based on the chart type
        if chart_type == 'bar':
            # Bar chart options
            label = QLabel("Optionen für Balkendiagramm:")
            label.setStyleSheet("font-weight: bold;")
            self.chart_options_layout.addWidget(label)

            # Show selected axes
            axes_info = QLabel(f"X-Achse: {x_axis}")
            axes_info.setWordWrap(True)
            self.chart_options_layout.addWidget(axes_info)

            y_axes_text = "Y-Achsen: " + ", ".join([str(cast(Dict[str, Any], y).get('column', '')) for y in y_axes])
            y_axes_label = QLabel(y_axes_text)
            y_axes_label.setWordWrap(True)
            self.chart_options_layout.addWidget(y_axes_label)

            # Placeholder for actual options
            self.chart_options_layout.addWidget(QLabel("Balkendiagramm-Optionen werden in einer zukünftigen Version implementiert."))

        elif chart_type == 'line':
            # Line chart options
            label = QLabel("Optionen für Liniendiagramm:")
            label.setStyleSheet("font-weight: bold;")
            self.chart_options_layout.addWidget(label)

            # Show selected axes
            axes_info = QLabel(f"X-Achse: {x_axis}")
            axes_info.setWordWrap(True)
            self.chart_options_layout.addWidget(axes_info)

            y_axes_text = "Y-Achsen: " + ", ".join([str(cast(Dict[str, Any], y).get('column', '')) for y in y_axes])
            y_axes_label = QLabel(y_axes_text)
            y_axes_label.setWordWrap(True)
            self.chart_options_layout.addWidget(y_axes_label)

            # Placeholder for actual options
            self.chart_options_layout.addWidget(QLabel("Liniendiagramm-Optionen werden in einer zukünftigen Version implementiert."))

        elif chart_type == 'pie':
            # Pie chart options
            label = QLabel("Optionen für Kreisdiagramm:")
            label.setStyleSheet("font-weight: bold;")
            self.chart_options_layout.addWidget(label)

            # Show selected axes
            axes_info = QLabel(f"X-Achse (Kategorien): {x_axis}")
            axes_info.setWordWrap(True)
            self.chart_options_layout.addWidget(axes_info)

            if y_axes:
                first_y_axis = y_axes[0] if isinstance(y_axes, list) and len(y_axes) > 0 else {}
                y_axis_info = QLabel(f"Y-Achse (Werte): {str(cast(Dict[str, Any], first_y_axis).get('column', ''))}")
                y_axis_info.setWordWrap(True)
                self.chart_options_layout.addWidget(y_axis_info)

            # Placeholder for actual options
            self.chart_options_layout.addWidget(QLabel("Kreisdiagramm-Optionen werden in einer zukünftigen Version implementiert."))

        elif chart_type == 'scatter':
            # Scatter plot options
            label = QLabel("Optionen für Streudiagramm:")
            label.setStyleSheet("font-weight: bold;")
            self.chart_options_layout.addWidget(label)

            # Show selected axes
            axes_info = QLabel(f"X-Achse: {x_axis}")
            axes_info.setWordWrap(True)
            self.chart_options_layout.addWidget(axes_info)

            if y_axes:
                first_y_axis = y_axes[0] if isinstance(y_axes, list) and len(y_axes) > 0 else {}
                y_axis_info = QLabel(f"Y-Achse: {str(cast(Dict[str, Any], first_y_axis).get('column', ''))}")
                y_axis_info.setWordWrap(True)
                self.chart_options_layout.addWidget(y_axis_info)

            # Placeholder for actual options
            self.chart_options_layout.addWidget(QLabel("Streudiagramm-Optionen werden in einer zukünftigen Version implementiert."))

        elif chart_type == 'heatmap':
            # Heatmap options
            label = QLabel("Optionen für Heatmap:")
            label.setStyleSheet("font-weight: bold;")
            self.chart_options_layout.addWidget(label)

            # Show selected axes
            axes_info = QLabel(f"X-Achse: {x_axis}")
            axes_info.setWordWrap(True)
            self.chart_options_layout.addWidget(axes_info)

            if y_axes:
                first_y_axis = y_axes[0] if isinstance(y_axes, list) and len(y_axes) > 0 else {}
                y_axis_info = QLabel(f"Y-Achse: {str(cast(Dict[str, Any], first_y_axis).get('column', ''))}")
                y_axis_info.setWordWrap(True)
                self.chart_options_layout.addWidget(y_axis_info)

            # Placeholder for actual options
            self.chart_options_layout.addWidget(QLabel("Heatmap-Optionen werden in einer zukünftigen Version implementiert."))

    @override
    def accept(self) -> None:
        """Handle dialog acceptance."""
        # Update the visualization name from the UI
        if self.name_edit is not None:
            self.visualization_config['name'] = self.name_edit.text()
        else:
            import logging
            logger = logging.getLogger(__name__)
            logger.error("name_edit ist nicht initialisiert")

        # Validate the configuration
        if not self.validate_configuration():
            return

        # Call the parent accept method
        super().accept()

    def validate_configuration(self) -> bool:
        """Validate the visualization configuration.

        Returns:
            True if the configuration is valid, False otherwise
        """
        # Check if name is provided
        if not self.visualization_config['name']:
            # Show error message
            _ = QMessageBox.warning(
                self,
                "Ungültige Konfiguration",
                "Bitte geben Sie einen Namen für die Visualisierung ein."
            )
            return False

        # Check if X-axis is selected
        if not self.visualization_config['x_axis']:
            # Show error message
            _ = QMessageBox.warning(
                self,
                "Ungültige Konfiguration",
                "Bitte wählen Sie eine X-Achse aus."
            )
            return False

        # Check if at least one Y-axis is selected
        if not self.visualization_config['y_axes']:
            # Show error message
            _ = QMessageBox.warning(
                self,
                "Ungültige Konfiguration",
                "Bitte wählen Sie mindestens eine Y-Achse aus."
            )
            return False

        # Check if chart type supports multiple Y-axes
        chart_type = str(self.visualization_config['chart_type'])
        chart_info = VISUALIZATION_TYPES.get(chart_type, {})
        supports_multiple_y = bool(chart_info.get('supports_multiple_y', False))

        if len(self.visualization_config['y_axes']) > 1 and not supports_multiple_y:
            # Show warning message
            result = QMessageBox.question(
                self,
                "Mehrere Y-Achsen",
                f"Der Diagrammtyp '{chart_info.get('name', chart_type)}' unterstützt nur eine Y-Achse. "
                "Nur die erste ausgewählte Y-Achse wird verwendet. Möchten Sie fortfahren?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if result == QMessageBox.StandardButton.No:
                return False

        return True

    def load_existing_visualization_settings(self) -> None:
        """Load settings from an existing visualization into the UI elements."""
        import logging
        logger = logging.getLogger(__name__)

        if not self.is_edit_mode or not self.existing_visualization:
            logger.warning("Keine bestehende Visualisierung zum Laden vorhanden")
            return

        try:
            # Set a flag to indicate we're loading settings
            # This prevents automatic creation of Y-axis widgets when removing existing ones
            self._loading_settings = True

            # Set the name
            if self.name_edit:
                self.name_edit.setText(self.existing_visualization.name)

            # Set the chart type
            chart_type = self.existing_visualization.chart_type
            if chart_type in self.chart_type_buttons:
                # Uncheck all buttons first
                for btn in self.chart_type_buttons.values():
                    btn.setChecked(False)

                # Check the selected chart type
                self.chart_type_buttons[chart_type].setChecked(True)

            # Set the X-axis
            x_axis = self.existing_visualization.config.get('x_axis', '')
            if self.x_axis_combo and x_axis:
                index = self.x_axis_combo.findText(x_axis)
                if index >= 0:
                    self.x_axis_combo.setCurrentIndex(index)

            # Set the Y-axes
            y_axes = self.existing_visualization.config.get('y_axes', [])
            if y_axes:
                # Log the Y-axes configuration for debugging
                logger.debug("Lade Y-Achsen aus Konfiguration: %s", y_axes)

                # Remove any existing Y-axis widgets
                while self.y_axis_widgets:
                    widget_data = self.y_axis_widgets[0]
                    frame = widget_data.get('frame')
                    if frame:
                        self.remove_y_axis_widget(frame)

                # Add Y-axis widgets for each Y-axis in the config
                for i, y_axis in enumerate(y_axes):
                    # Log the current Y-axis being processed
                    logger.debug("Verarbeite Y-Achse %d: %s", i, y_axis)

                    # Add a new Y-axis widget
                    self.add_y_axis_widget()

                    # Get the last added widget
                    widget_data = self.y_axis_widgets[-1]
                    combo = widget_data.get('combo')
                    color_button = widget_data.get('color_button')

                    # First set the color to ensure it's properly applied
                    if color_button and 'color' in y_axis:
                        color_value = y_axis['color']
                        logger.debug("Setze Farbe für Y-Achse %d: %s", i, color_value)
                        color_button.setStyleSheet(f"background-color: {color_value}; color: white;")
                        _ = color_button.setProperty("color_value", color_value)

                    # Then set the column (this might trigger events that update the configuration)
                    if combo and 'column' in y_axis:
                        column_name = y_axis['column']
                        logger.debug("Setze Spalte für Y-Achse %d: %s", i, column_name)
                        index = combo.findText(column_name)
                        if index >= 0:
                            combo.setCurrentIndex(index)
            else:
                # If no Y-axes, ensure we have at least one empty widget
                if not self.y_axis_widgets:
                    self.add_y_axis_widget()

            # Clear the loading flag
            self._loading_settings = False

            # Update chart options based on the loaded settings
            self.update_chart_options()

            # Update chart preview with the correct configuration
            # Make sure the configuration has the correct colors
            logger.debug("Aktuelle Y-Achsen-Konfiguration vor der Vorschau: %s", self.visualization_config['y_axes'])
            self.update_chart_preview()

            logger.info("Bestehende Visualisierungseinstellungen erfolgreich geladen")
        except Exception as e:
            # Clear the loading flag in case of error
            self._loading_settings = False

            logger.error("Fehler beim Laden der bestehenden Visualisierungseinstellungen: %s", str(e))
            import traceback
            logger.error("Traceback: %s", traceback.format_exc())

    def get_visualization(self) -> Visualization:
        """Get the configured visualization.

        Returns:
            A Visualization object with the configured settings.
            If in edit mode, returns the updated existing visualization.
            Otherwise, returns a new visualization.
        """
        from datetime import datetime
        import logging
        logger = logging.getLogger(__name__)

        # Check if chart type supports multiple Y-axes
        chart_type = str(self.visualization_config['chart_type'])
        chart_info = VISUALIZATION_TYPES.get(chart_type, {})
        supports_multiple_y = bool(chart_info.get('supports_multiple_y', False))

        # If chart doesn't support multiple Y-axes, only use the first one
        y_axes = self.visualization_config['y_axes']
        if not supports_multiple_y and len(y_axes) > 1:
            y_axes = [y_axes[0]] if isinstance(y_axes, list) and len(y_axes) > 0 else []

        # Create config dictionary
        config = {
            'x_axis': self.visualization_config['x_axis'],
            'y_axes': y_axes,
            'filter': self.visualization_config['filter'],
            'aggregation': self.visualization_config['aggregation'],
            'style': self.visualization_config['style']
        }

        if self.is_edit_mode and self.existing_visualization:
            # Update existing visualization
            logger.info("Aktualisiere bestehende Visualisierung: %s", self.existing_visualization.name)
            self.existing_visualization.name = str(self.visualization_config['name'])
            self.existing_visualization.chart_type = str(self.visualization_config['chart_type'])
            self.existing_visualization.config = config
            self.existing_visualization.modified_at = datetime.now()
            return self.existing_visualization
        else:
            # Create new visualization
            logger.info("Erstelle neue Visualisierung: %s", self.visualization_config['name'])
            return Visualization(
                name=str(self.visualization_config['name']),
                chart_type=str(self.visualization_config['chart_type']),
                config=config,
                created_at=datetime.now(),
                modified_at=datetime.now()
            )
