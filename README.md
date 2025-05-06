# DataInspect

Eine Desktop-Anwendung zur Datenvisualisierung, entwickelt mit Python und PyQt6.

## Über das Projekt

DataInspect ermöglicht den Import, die grundlegende Vorverarbeitung und die Visualisierung von Daten. Die Anwendung bietet eine intuitive Benutzeroberfläche für die Analyse und Präsentation von Daten durch verschiedene Diagrammtypen.

## Systemanforderungen

- **Betriebssystem:** Windows 10/11, macOS oder Linux
- **Python:** Version 3.12 (gemäß pyrightconfig.json)
- **Festplattenspeicher:** Ca. 100 MB freier Speicherplatz für die Anwendung und Abhängigkeiten

## Installation

### Voraussetzungen

- Python 3.12
- Git (für das Klonen des Repositories)

### Installation für macOS/Linux

1. Klone das Repository:
   ```bash
   git clone https://github.com/jurkat/datainspect.git
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
   git clone https://github.com/jurkat/datainspect.git
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

### Manuelle Installation (falls die Skripte nicht funktionieren)

1. Klone das Repository und wechsle in das Verzeichnis:
   ```bash
   git clone https://github.com/jurkat/datainspect.git
   cd datainspect
   ```

2. Erstelle eine virtuelle Umgebung:
   ```bash
   python -m venv venv
   ```

3. Aktiviere die virtuelle Umgebung:
   - Unter macOS/Linux: `source venv/bin/activate`
   - Unter Windows: `venv\Scripts\activate.bat`

4. Installiere die Abhängigkeiten:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Anwendung starten

Nach der Installation und Aktivierung der virtuellen Umgebung kann die Anwendung gestartet werden mit:

```bash
python main.py
```

## Abhängigkeiten

Die Hauptabhängigkeiten des Projekts sind:

- **PyQt6 6.7.0:** GUI-Framework
- **Pandas 2.2.2:** Datenverarbeitung und -analyse
- **Matplotlib 3.8.4:** Visualisierungsbibliothek
- **NumPy 1.26.4:** Numerische Berechnungen
- **openpyxl 3.1.2:** Excel-Dateiunterstützung

Für die Entwicklung und Tests werden zusätzlich benötigt:
- **pytest 8.0.0:** Test-Framework
- **pytest-cov 4.1.0:** Test-Coverage-Analyse

Die vollständige Liste der Abhängigkeiten finden Sie in der Datei `requirements.txt`.

## Testdaten

Im Repository sind Testdaten enthalten, die zum Testen der Anwendung verwendet werden können. Diese befinden sich im Ordner `data/`. Um die Testdaten zu verwenden:

1. Starten Sie die Anwendung
2. Klicken Sie auf "Datenquelle hinzufügen" oder verwenden Sie die Drop-Zone
3. Navigieren Sie zum `data/`-Ordner und wählen Sie eine der CSV-Dateien aus

Folgende Testdatensätze sind verfügbar:

- **arbeit_deutschland_2000_2024.csv:** Bevölkerungs- und Arbeitsmarktdaten für Deutschland
- **basic_data.csv:** Einfache Personendaten mit Namen, Alter, Stadt und Gehalt
- **german_format.csv:** Daten im deutschen Format mit Semikolon als Trennzeichen und Komma als Dezimaltrennzeichen
- **missing_special.csv:** Daten mit fehlenden Werten und Sonderzeichen
- **mixed_types.csv:** Daten mit verschiedenen Datentypen (Text, Zahlen, Datum, Boolean)
- **no_header.csv:** Daten ohne Kopfzeile

Diese Datensätze eignen sich zum Testen verschiedener Import- und Transformationsfunktionen.

## Implementierte Features

- **Datenimport:**
  - CSV-Import mit Konfigurationsoptionen
  - Vorschaufunktion für CSV-Daten
  - Unterstützung für verschiedene Trennzeichen und Dateiformate

- **Datenvorverarbeitung:**
  - Transformationen während des Imports
  - Behandlung fehlender Werte
  - Typkonvertierungen

- **Visualisierung:**
  - Verschiedene Diagrammtypen
  - Anpassung von Achsen, Titeln und Farben
  - Vorschau von Visualisierungen

- **Projektmanagement:**
  - Speichern und Laden von Projekten
  - Hierarchische Struktur für Datenquellen und Visualisierungen

## Entwicklung und Tests

### Code-Qualität

Das Projekt verwendet:
- **Pyright:** Für statische Typprüfung
- **pytest:** Für Unit-Tests
- **autoflake:** Für das Entfernen ungenutzter Importe und Variablen

### Tests ausführen

Um die Tests auszuführen:

```bash
pytest
```

Für Tests mit Coverage-Bericht:

```bash
pytest --cov=src
```

### Code-Bereinigung

Das Projekt enthält ein Skript zur Code-Bereinigung:

```bash
sh cleanup.sh
```

Dieses Skript entfernt ungenutzte Importe und Variablen und führt eine statische Typprüfung durch.