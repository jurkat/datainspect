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