# Projektdokumentation „DataInspect“

## Projektübersicht

### Projektziel
Das Projekt "DataInspect" zielt auf die Entwicklung einer benutzerfreundlichen Desktop-Anwendung, die es Nutzern ermöglicht, Daten aus verschiedenen Quellen zu importieren, grundlegende Datenvorverarbeitungen durchzuführen und die Daten durch interaktive Visualisierungen zu analysieren und präsentieren. Die Anwendung soll eine intuitive Benutzeroberfläche bieten und verschiedene Diagrammtypen unterstützen, die anpassbar sind und als Bild oder PDF exportiert werden können.

### Projektumfang
1. **Datenimport:** Import von Daten aus CSV-, Excel- und JSON-Dateien.
2. **Datenvorverarbeitung:** Grundlegende Datenbereinigung, einfache Transformationen und Berechnung von Statistiken.
3. **Visualisierung:** Verschiedene Diagrammtypen (Balken, Linien, Kreis, Streudiagramm, Heatmap) mit Anpassungsmöglichkeiten und interaktiven Elementen.
4. **Export und Sharing:** Export als Bild oder PDF sowie Speichern von Projekten zur späteren Bearbeitung.
5. **Benutzeroberfläche:** Intuitive, benutzerfreundliche Oberfläche mit Drag-and-Drop-Funktionalität und Vorlagen für gängige Diagrammtypen.

---

## Risikomanagement

### Risiko 1: Zeitdruck
- **Beschreibung:** Das Projekt muss innerhalb von 19 Tagen abgeschlossen werden, mit Ostern (18.-21. April) in der Mitte der Entwicklungsphase.
- **Eintrittswahrscheinlichkeit:** Hoch (5/5)
- **Auswirkung:** Hoch (5/5)
- **Gegenmaßnahmen:**
  - Erstellung eines detaillierten Zeitplans mit klaren Prioritäten
  - Fokus auf Kernfunktionen und MVP (Minimum Viable Product)
  - Modularer Entwicklungsansatz, um Funktionen bei Bedarf weglassen zu können
  - Bereitstellung von Extra-Arbeitszeit vor und nach Ostern

### Risiko 2: Technische Komplexität
- **Beschreibung:** Die Integration verschiedener Bibliotheken (PyQt, Matplotlib, Pandas) könnte zu Kompatibilitätsproblemen oder unerwarteten Herausforderungen führen.
- **Eintrittswahrscheinlichkeit:** Mittel (3/5)
- **Auswirkung:** Hoch (4/5)
- **Gegenmaßnahmen:**
  - Frühe Erstellung eines technischen Prototyps zur Validierung des Konzepts
  - Verwendung bewährter, gut dokumentierter Bibliotheken
  - Einplanung von Zeit für technische Recherche und Problemlösung
  - Backup-Plan mit alternativen Bibliotheken bei Kompatibilitätsproblemen

### Risiko 3: Umfangserweiterung
- **Beschreibung:** Die Versuchung, zusätzliche Features zu implementieren, könnte zu Verzögerungen führen.
- **Eintrittswahrscheinlichkeit:** Mittel (3/5)
- **Auswirkung:** Mittel (3/5)
- **Gegenmaßnahmen:**
  - Klare Definition des MVP
  - Priorisierung von Features und strikte Einhaltung der Prioritätenliste
  - Zeitpuffer für unvorhergesehene Probleme einplanen
  - Regelmäßige Überprüfung des Projektfortschritts

### Risiko 4: Begrenzte GUI-Erfahrung
- **Beschreibung:** Möglicherweise begrenzte Erfahrung mit PyQt könnte zu einer ineffizienten Implementierung der Benutzeroberfläche führen.
- **Eintrittswahrscheinlichkeit:** Mittel (3/5)
- **Auswirkung:** Mittel (3/5)
- **Gegenmaßnahmen:**
  - Recherche und Nutzung von Best-Practice-Beispielen
  - Fokus auf Funktionalität vor Ästhetik
  - Frühe Prototypen der GUI zur Validierung des Konzepts

---

## Zeitplanung

**10.-15. April:**
- Projektplanung
- Planung der grundlegenden Anwendungsarchitektur

**16.-17. April:**
- Fertigstellung/Einreichung der Phase-1-Dokumente
- Einrichten der Entwicklungsumgebung
- Erstellung eines GitHub-Repositories
- Auswahl und Installation der notwendigen Bibliotheken
- Start der GUI-Entwicklung

**22.-25. April:**
- Implementierung der Datenimport-Funktionen (CSV, Excel)
- Grundlegende Datenvorverarbeitung
- Implementierung erster Visualisierungskomponenten
- Implementierung der Export-Funktionen
- Feinabstimmung der Benutzeroberfläche
- Erstellung von Testfällen
- Bugfixing und Optimierung
- Fertigstellung/Einreichung der Phase-2-Dokumente

**28.-29. April:**
- Abschluss der Implementierung
- Finalisierung der Dokumentation
- Finale Tests und Bugfixing
- Einreichung der finalen Dokumentation und des Produkts (Phase 3)

Diese Zeitplanung berücksichtigt die kritischen Punkte des Projekts und legt den Fokus auf die frühzeitige Implementierung der Kernfunktionalitäten. Die Osterzeit wird als Periode mit reduzierter Aktivität eingeplant, wobei die Hauptentwicklungsarbeit auf die Tage vor und nach den Feiertagen konzentriert wird.

---

## Projektfortschritt und Abweichungen

### Abweichungen vom Zeitplan
Die Implementierung hat sich gegenüber dem ursprünglichen Zeitplan um etwa eine Woche verzögert. Dies ist auf folgende Faktoren zurückzuführen:

1. **Technische Herausforderungen:** Die Integration der Column-Klasse in die Dataset-Struktur erwies sich als komplexer als erwartet, insbesondere bei der Serialisierung von NumPy-Datentypen für die JSON-Speicherung.

2. **Architekturanpassungen:** Die Umstellung auf eine strikte 1:1-Beziehung zwischen DataSource und Dataset sowie die hierarchische Struktur für Visualisierungen erforderten umfangreichere Änderungen am Datenmodell als ursprünglich geplant.

3. **Testaufwand:** Die Implementierung robuster Tests für die neuen Komponenten nahm mehr Zeit in Anspruch als vorgesehen.

### Gegenmaßnahmen
Um trotz der Verzögerungen das Projekt erfolgreich abzuschließen, wurden folgende Maßnahmen ergriffen:

1. **Fokussierung auf Kernfunktionalitäten:** Priorisierung der wichtigsten Features (Datenimport, grundlegende Visualisierungen) vor optionalen Funktionen.

2. **Erhöhter Zeitaufwand:** Zusätzliche Entwicklungszeit wurde investiert, um den Rückstand aufzuholen.

3. **Vereinfachung einiger Komponenten:** Weniger kritische Funktionen wurden vereinfacht, um Zeit zu sparen.

### Aktueller Stand
Trotz der Verzögerungen konnten die Kernfunktionalitäten erfolgreich implementiert werden:

- CSV-Import mit umfangreichen Konfigurationsoptionen und Transformationen
- Integration der Column-Klasse für verbesserte Datenanalyse
- Hierarchische Struktur für DataSource, Dataset und Visualization
- Grundlegende Visualisierungsfunktionen mit mehreren Diagrammtypen (Balken, Linien, Kreis, Streu, Heatmap)
- Visualisierungserstellung mit Vorschau und Konfigurationsoptionen

Folgende Funktionalitäten sind für die nächste Phase geplant:

- Export von Visualisierungen als Bild oder PDF
- Excel- und JSON-Import
- Erweiterte Filterung, Sortierung und Gruppierung von Daten
- Interaktive Elemente für Visualisierungen

Das GitHub-Repository ist unter [https://github.com/jurkat/datainspect](https://github.com/jurkat/datainspect) verfügbar.