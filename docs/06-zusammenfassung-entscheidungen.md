# Zusammenfassung der Design- und Implementierungsentscheidungen

## Technologie-Stack

### Kernbibliotheken und -frameworks

- **Python 3.12.8:** Gewählt für seine umfangreichen Bibliotheken für Datenverarbeitung und Visualisierung, einfache Syntax und schnelle Entwicklung.

- **PyQt6:** Umfassendes GUI-Framework mit moderner Optik, guter Integration mit Python und umfangreicher Dokumentation.

- **Pandas 2.1.4:** Leistungsstarke Bibliothek für Datenmanipulation und -analyse mit effizienten Datenstrukturen für tabellarische Daten.

- **Matplotlib 3.8.2:** Flexible Bibliothek für Visualisierungen mit umfangreichen Anpassungsmöglichkeiten und guter Integration mit PyQt.

- **JSON:** Leichtgewichtiges, menschenlesbares Datenaustauschformat für die Persistenz von Projekten und Daten.

## Architektur

### Hauptvorteile des gewählten Architekturstils

- **Kombination aus MVC und MVVM:** Ermöglicht eine klare Trennung von Daten, Logik und Präsentation, was die Wartbarkeit und Testbarkeit der Anwendung verbessert.

- **Observer-Pattern:** Ermöglicht lose Kopplung zwischen Komponenten und automatische UI-Aktualisierung bei Datenänderungen.

- **Hierarchische Datenstruktur:** Klare Organisation mit Project → DataSources → Dataset/Visualizations für einfachere Navigation und Verwaltung von Beziehungen.

- **Factory-Pattern:** Kapselung der Objekterstellung und Vereinfachung der Instanziierung komplexer Objekte.

- **Strategy-Pattern:** Austauschbare Algorithmen für verschiedene Datenformate und Transformationen.

## Besondere Herausforderungen

### Gelöste Probleme und Lösungsansätze

1. **Zirkuläre Importe:**
   - **Problem:** Bei der Integration der Column-Klasse traten zirkuläre Importprobleme auf.
   - **Lösung:** Die Column-Klasse wurde direkt in die models.py-Datei integriert, anstatt sie als separates Modul zu implementieren.

2. **Serialisierung von NumPy-Datentypen:**
   - **Problem:** NumPy-Datentypen wie int64 sind nicht direkt JSON-serialisierbar.
   - **Lösung:** Implementierung einer speziellen to_json-Methode, die NumPy-Datentypen in Python-Standardtypen konvertiert.

3. **Tracking von Änderungen:**
   - **Problem:** Erkennung ungespeicherter Änderungen in verschachtelten Objektstrukturen.
   - **Lösung:** Implementierung einer _TrackingList-Klasse und eines Callback-Mechanismus, um Änderungen an Collections zu verfolgen.

4. **Automatische UI-Aktualisierung:**
   - **Problem:** Synchronisierung der UI mit dem Datenmodell bei Änderungen.
   - **Lösung:** Implementierung des Observer-Patterns mit spezifischen Events für verschiedene Änderungstypen.

## Wichtige Kompromisse

### Trade-offs und ihre Begründung

1. **1:1-Beziehung zwischen DataSource und Dataset:**
   - **Trade-off:** Einschränkung der Flexibilität zugunsten von Einfachheit und Konsistenz.
   - **Begründung:** Vermeidung von Inkonsistenzen zwischen Originaldaten und transformierten Daten, klarere Verantwortlichkeiten und intuitiveres Modell für Endbenutzer.

2. **JSON statt binärer Formate für Persistenz:**
   - **Trade-off:** Größere Dateien und langsamere Serialisierung/Deserialisierung zugunsten von Lesbarkeit und Debugbarkeit.
   - **Begründung:** Menschenlesbarkeit, einfaches Debugging und flexible Erweiterbarkeit sind wichtiger als optimale Performance bei der Persistenz.

3. **Automatische Typbestimmung statt manueller Konfiguration:**
   - **Trade-off:** Möglicherweise weniger Kontrolle für Experten zugunsten von Benutzerfreundlichkeit.
   - **Begründung:** Keine manuelle Typzuweisung erforderlich, bessere Standardeinstellungen für Visualisierungen und typspezifische statistische Berechnungen.

4. **Hierarchische Struktur statt flacher Struktur:**
   - **Trade-off:** Einschränkung der Flexibilität zugunsten von Klarheit und einfacherer Navigation.
   - **Begründung:** Einheitliche hierarchische Struktur, intuitivere Organisation in der UI und direkter Zugriff auf alle Visualisierungen einer Datenquelle.

## Aktueller Implementierungsstatus

### Bereits implementierte Funktionalitäten

1. **Datenimport:**
   - CSV-Import mit umfangreichen Konfigurationsoptionen
   - Automatische Erkennung von Trennzeichen
   - Vorschaufunktion für CSV-Daten
   - Validierung der importierten Daten

2. **Datenmodell:**
   - Vollständige Implementierung der Project-, DataSource-, Dataset-, Column- und Visualization-Klassen
   - Hierarchische Struktur mit 1:1-Beziehung zwischen DataSource und Dataset
   - Eindeutige IDs für alle Modelobjekte
   - Serialisierung und Deserialisierung in JSON

3. **Benutzeroberfläche:**
   - Hauptfenster mit hierarchischer Darstellung der Datenquellen und Visualisierungen
   - CSV-Import-Dialog mit Konfigurationsoptionen und Transformationen
   - Visualisierungserstellung mit Vorschau
   - Datenvorschau beim Klicken auf eine Quelle
   - Verbesserte Darstellung im Dark Mode

4. **Projektmanagement:**
   - Speichern und Laden von Projekten
   - Erkennung ungespeicherter Änderungen
   - Automatische UI-Aktualisierung bei Änderungen am Datenmodell

### Ausstehende Funktionalitäten

1. **Datenimport:**
   - Excel- und JSON-Import
   - Direkte Dateneingabe

2. **Datenvorverarbeitung:**
   - Dedizierte UI für Filterung, Sortierung und Gruppierung
   - Erweiterte Transformationen nach dem Import
   - Speichern und Laden von Transformationskonfigurationen

3. **Visualisierung:**
   - Implementierung weiterer Anpassungsoptionen für Diagramme
   - Interaktive Elemente (Zoom, Hover-Effekte)
   - Erweiterte Filterung direkt in Visualisierungen

4. **Export:**
   - Export als Bild oder PDF
   - Konfigurationsoptionen für den Export
