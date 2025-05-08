# Abstract „DataInspect"

## Projektzusammenfassung

DataInspect ist eine Desktop-Anwendung zur Datenvisualisierung und -analyse, die es Benutzern ermöglicht, Daten aus verschiedenen Quellen zu importieren, zu transformieren und durch interaktive Visualisierungen zu analysieren. Die Anwendung wurde mit Python 3.12 und PyQt6 entwickelt und nutzt Pandas für die Datenverarbeitung sowie Matplotlib für die Visualisierung.

### Ziele und Zielgruppe

Das Hauptziel von DataInspect ist es, eine benutzerfreundliche Alternative zu komplexen Datenanalysetools zu bieten, die keine Programmierkenntnisse erfordert. Die Anwendung richtet sich an:

1. **Studierende**, die Daten für Projekte und Abschlussarbeiten visualisieren müssen
2. **Fachleute in kleinen bis mittleren Unternehmen**, die regelmäßig Datenvisualisierungen für Berichte erstellen
3. **Datenanalysten**, die ein schnelles Tool für explorative Datenanalyse benötigen

### Kernfunktionalitäten

DataInspect bietet folgende Kernfunktionalitäten:

1. **Datenimport**: Import von CSV-Dateien mit umfangreichen Konfigurationsoptionen (Trennzeichen, Encoding, Kopfzeilen)
2. **Datenvorverarbeitung**: Automatische Typbestimmung, Behandlung fehlender Werte, Transformationen
3. **Datenvisualisierung**: Erstellung verschiedener Diagrammtypen (Balken, Linien, Kreis, Streu, Heatmap)
4. **Projektmanagement**: Speichern und Laden von Projekten mit allen Datenquellen und Visualisierungen

### Technische Highlights

Die Anwendung zeichnet sich durch folgende technische Merkmale aus:

1. **Modulare Architektur**: Klare Trennung von Datenmodell, Geschäftslogik und Benutzeroberfläche (MVC/MVVM-Pattern)
2. **Observer-Pattern**: Automatische Aktualisierung der UI bei Änderungen am Datenmodell
3. **Hierarchische Datenstruktur**: Intuitive Organisation von Datenquellen, Datensätzen und Visualisierungen
4. **Erweiterbarkeit**: Flexibles Design für zukünftige Erweiterungen (weitere Datenquellen, Visualisierungstypen)

## Making-of

### Entwicklungsverlauf

Die Entwicklung von DataInspect erfolgte in drei Hauptphasen:

1. **Konzeptionsphase (10.04. - 16.04.)**:
   - Erstellung der Projektdokumentation, des Anforderungsdokuments und des Spezifikationsdokuments
   - Definition der Architektur und des Datenmodells
   - Entwurf der Benutzeroberfläche

2. **Erarbeitungs- und Reflexionsphase (16.04. - 30.04.)**:
   - Implementierung des Datenmodells und der Grundstruktur
   - Entwicklung des CSV-Imports und der Datenvorverarbeitung
   - Implementierung der Benutzeroberfläche und der Visualisierungskomponenten
   - Anpassung der Architektur basierend auf Erkenntnissen während der Implementierung

3. **Finalisierungsphase (30.04. - 09.05.)**:
   - Abschluss der Implementierung
   - Erstellung und Durchführung von Tests
   - Fehlerbehebung und Optimierung (bis 06.05., Abgabe Phase 2)
   - Finalisierung der Dokumentation (07.05. - 08.05.)
   - Projektabgabe (09.05.)

### Technische Herausforderungen und Lösungen

Während der Entwicklung traten verschiedene technische Herausforderungen auf:

1. **Zirkuläre Importe**:
   - **Problem**: Bei der Integration der Column-Klasse traten zirkuläre Importprobleme auf
   - **Lösung**: Die Column-Klasse wurde direkt in die models.py-Datei integriert, anstatt sie als separates Modul zu implementieren

2. **Serialisierung von NumPy-Datentypen**:
   - **Problem**: NumPy-Datentypen wie int64 sind nicht direkt JSON-serialisierbar
   - **Lösung**: Implementierung einer speziellen to_json-Methode, die NumPy-Datentypen in Python-Standardtypen konvertiert

3. **Tracking von Änderungen**:
   - **Problem**: Erkennung ungespeicherter Änderungen in verschachtelten Objektstrukturen
   - **Lösung**: Implementierung einer _TrackingList-Klasse und eines Callback-Mechanismus, um Änderungen an Collections zu verfolgen

4. **Automatische UI-Aktualisierung**:
   - **Problem**: Synchronisierung der UI mit dem Datenmodell bei Änderungen
   - **Lösung**: Implementierung des Observer-Patterns mit spezifischen Events für verschiedene Änderungstypen

### Zeitplanung und Verzögerungen

Die ursprüngliche Zeitplanung sah vor, dass die Implementierung bis zum 30.04. abgeschlossen sein sollte. Aufgrund der folgenden Faktoren kam es jedoch zu Verzögerungen:

1. **Komplexität des Datenmodells**: Die Integration der Column-Klasse und die Implementierung der hierarchischen Struktur erwiesen sich als komplexer als erwartet
2. **Technische Herausforderungen**: Die Lösung der oben genannten technischen Probleme nahm mehr Zeit in Anspruch als geplant
3. **Umfang der Tests**: Die Erstellung robuster Tests für die neuen Komponenten erforderte zusätzliche Zeit

Um diese Verzögerungen zu kompensieren, wurden folgende Maßnahmen ergriffen:

1. **Fokussierung auf Kernfunktionalitäten**: Priorisierung der wichtigsten Features vor optionalen Funktionen
2. **Erhöhter Zeitaufwand**: Zusätzliche Entwicklungszeit wurde investiert, insbesondere am 7. und 8. Mai 2023
3. **Vereinfachung einiger Komponenten**: Weniger kritische Funktionen wurden vereinfacht, um Zeit zu sparen

## Kritische Reflexion

### Stärken des Projekts

1. **Modulare Architektur**: Die klare Trennung von Datenmodell, Geschäftslogik und Benutzeroberfläche ermöglicht eine gute Wartbarkeit und Erweiterbarkeit
2. **Robustes Datenmodell**: Die Implementierung der Column-Klasse mit automatischer Typbestimmung und statistischen Berechnungen bietet eine solide Grundlage für Datenanalysen
3. **Benutzerfreundlichkeit**: Die intuitive Benutzeroberfläche mit hierarchischer Darstellung von Datenquellen und Visualisierungen erleichtert die Navigation
4. **Testabdeckung**: Die kritischen Komponenten (Datenmodelle, Transformationen, CSV-Importer) haben eine hohe Testabdeckung

### Schwächen und Verbesserungspotenzial

1. **Begrenzte Funktionalität**: Aufgrund der Zeitbeschränkungen konnten nicht alle geplanten Funktionen implementiert werden (Excel- und JSON-Import, Export, erweiterte Filterung)
2. **GUI-Testabdeckung**: Die Benutzeroberfläche hat eine geringe automatisierte Testabdeckung, was die Zuverlässigkeit beeinträchtigen könnte
3. **Performance bei großen Datensätzen**: Die Anwendung wurde nicht für sehr große Datensätze (>100.000 Zeilen) optimiert
4. **Begrenzte Visualisierungsoptionen**: Die Anpassungsmöglichkeiten für Visualisierungen sind noch eingeschränkt

### Lessons Learned

1. **Realistische Zeitplanung**: Die Komplexität technischer Herausforderungen wurde unterschätzt, was zu Verzögerungen führte. In zukünftigen Projekten sollten großzügigere Pufferzeiten eingeplant werden.
2. **Frühe Prototypen**: Die Erstellung früher Prototypen für kritische Komponenten hätte technische Probleme früher aufdecken können.
3. **Testgetriebene Entwicklung**: Der testgetriebene Ansatz hat sich bewährt und sollte in zukünftigen Projekten noch konsequenter angewendet werden.
4. **Fokus auf MVP**: Die Konzentration auf ein Minimum Viable Product (MVP) mit den wichtigsten Funktionen war richtig, hätte aber noch konsequenter umgesetzt werden können.

### Empfehlungen für die Weiterentwicklung

1. **Kurzfristige Prioritäten**:
   - Implementierung der Filterfunktionalität für Datenanalysen
   - Erweiterung der Visualisierungsoptionen
   - Export von Visualisierungen als Bild oder PDF

2. **Mittelfristige Ziele**:
   - Unterstützung für Excel- und JSON-Import
   - Implementierung interaktiver Elemente für Visualisierungen
   - Verbesserung der Performance für große Datensätze

3. **Langfristige Vision**:
   - Integration von maschinellem Lernen für automatische Mustererkennung
   - Kollaborative Funktionen für Teamarbeit
   - Web-basierte Version für plattformunabhängigen Zugriff
