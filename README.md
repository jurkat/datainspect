# DataInspect

Eine Desktop-Anwendung zur Datenvisualisierung, entwickelt mit Python.

## Über das Projekt

DataInspect ermöglicht den Import, die grundlegende Vorverarbeitung und die Visualisierung von Daten aus verschiedenen Quellen wie CSV-, Excel- und JSON-Dateien. Die Anwendung bietet verschiedene Visualisierungsoptionen wie Balken-, Linien-, Kreis-, Streudiagramme und Heatmaps.

## Installation

### Voraussetzungen

- Python 3.8 oder höher

### Installation für macOS/Linux

1. Klone das Repository:
   ```bash
   git clone <repository-url>
   cd datainspect
   ```

2. Führe das Installations-Skript aus:
   ```bash
   sh setup.sh
   ```

3. Aktiviere die virtuelle Umgebung:
   ```bash
   source venv/bin/activate
   ```

### Installation für Windows

1. Klone das Repository:
   ```cmd
   git clone <repository-url>
   cd datainspect
   ```

2. Führe das Installations-Skript aus:
   ```cmd
   setup.bat
   ```

3. Aktiviere die virtuelle Umgebung:
   ```cmd
   venv\Scripts\activate.bat
   ```

## Anwendung starten

Nach der Installation und Aktivierung der virtuellen Umgebung kann die Anwendung gestartet werden mit:

```bash
python main.py
```

## Features

- Import von Daten aus CSV-, Excel- und JSON-Dateien
- Grundlegende Datenvorverarbeitung
- Verschiedene Visualisierungsoptionen:
  - Balkendiagramme
  - Liniendiagramme
  - Kreisdiagramme
  - Streudiagramme
  - Heatmaps
- Export-Funktionen für erstellte Visualisierungen