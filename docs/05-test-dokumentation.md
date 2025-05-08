# Testdokument „DataInspect"

## Teststrategie

### Testmethodik

Die Qualitätssicherung für DataInspect folgt einem umfassenden Ansatz, der sowohl automatisierte als auch manuelle Tests umfasst. Der Fokus liegt auf der Sicherstellung der Funktionalität, Zuverlässigkeit und Benutzerfreundlichkeit der Anwendung.

#### Allgemeiner Testansatz

Der Testansatz für DataInspect basiert auf folgenden Prinzipien:

1. **Testgetriebene Entwicklung (TDD)**: Für kritische Komponenten wie Datenmodelle und Transformationen wurden Tests vor der eigentlichen Implementierung geschrieben.
2. **Kontinuierliche Integration**: Tests werden bei jeder Codeänderung automatisch ausgeführt, um Regressionen frühzeitig zu erkennen.
3. **Schichtenbasiertes Testen**: Tests wurden für verschiedene Schichten der Anwendung entwickelt, von einzelnen Funktionen bis hin zur Gesamtanwendung.
4. **Fokus auf Kernfunktionalität**: Besonderer Wert wurde auf die Testabdeckung der Kernfunktionalitäten (Datenimport, Transformation, Visualisierung) gelegt.

#### Testphasen und ihre Abfolge

Der Testprozess für DataInspect umfasst folgende Phasen:

1. **Entwicklungsphase**:
   - Unit-Tests für neue Funktionen und Komponenten
   - Integrationstests für das Zusammenspiel mehrerer Komponenten
   - Manuelle Tests der Benutzeroberfläche

2. **Vor-Release-Phase**:
   - Systemtests der Gesamtanwendung
   - Akzeptanztests basierend auf den Anforderungen
   - Leistungs- und Stabilitätstests

3. **Nach-Release-Phase**:
   - Überwachung und Fehlerbehebung
   - Regressionstest bei Fehlerbehebungen

#### Manuelle vs. automatisierte Tests

Die Teststrategie von DataInspect kombiniert automatisierte und manuelle Tests:

- **Automatisierte Tests**:
  - Unit-Tests für Datenmodelle, Importfunktionen und Transformationen
  - Integrationstests für das Zusammenspiel von Komponenten
  - Automatisierte Code-Qualitätsprüfungen (Linting, statische Typprüfung)

- **Manuelle Tests**:
  - Benutzeroberfläche und Benutzerinteraktion
  - Explorative Tests zur Entdeckung unerwarteter Fehler
  - Usability-Tests zur Bewertung der Benutzerfreundlichkeit

#### Testumgebung und -werkzeuge

Für die Tests von DataInspect werden folgende Werkzeuge eingesetzt:

- **pytest**: Framework für Unit- und Integrationstests
- **pytest-cov**: Messung der Testabdeckung
- **unittest.mock**: Mocking-Framework für isolierte Tests
- **pyright**: Statische Typprüfung
- **autoflake**: Automatische Entfernung ungenutzter Importe und Variablen
- **cleanup.sh**: Skript zur Durchführung von Codebereinigung und statischer Analyse

### Testebenen

#### Unit-Tests

Unit-Tests prüfen einzelne Komponenten der Anwendung isoliert von anderen Teilen:

- **Getestete Komponenten**:
  - Datenmodelle (`Project`, `DataSource`, `Dataset`, `Column`, `Visualization`)
  - Importfunktionen (CSV-Importer)
  - Datentransformationen
  - Observer-Pattern-Implementierung
  - Visualisierungskomponenten

- **Behandlung von Abhängigkeiten**:
  - Verwendung von Mock-Objekten für externe Abhängigkeiten
  - Erstellung von Test-Fixtures für häufig benötigte Objekte
  - Temporäre Dateien für Datei-I/O-Tests

- **Verwendete Frameworks**:
  - Python's `unittest`-Framework als Basis
  - `pytest` für erweiterte Testfunktionalitäten
  - `unittest.mock` für Mocking

#### Integrationstests

Integrationstests prüfen das Zusammenspiel mehrerer Komponenten:

- **Getestete Integrationen**:
  - Datenimport und Datentransformation
  - Datenspeicherung und -wiederherstellung
  - Visualisierungserstellung und -rendering

- **Ansatz**:
  - Bottom-up-Ansatz: Testen von niedrigeren Schichten (Datenmodelle) zu höheren Schichten (Visualisierung)
  - Verwendung realer Daten statt Mocks, wo sinnvoll

#### Systemtests

Systemtests prüfen die Gesamtanwendung:

- **End-to-End-Testszenarien**:
  - Import einer CSV-Datei, Anwendung von Transformationen und Erstellung einer Visualisierung
  - Speichern und Laden eines Projekts mit mehreren Datenquellen und Visualisierungen

- **Benutzeroberflächen-Tests**:
  - Manuelle Tests der GUI-Komponenten
  - Überprüfung der Reaktion auf Benutzerinteraktionen

#### Akzeptanztests

Akzeptanztests validieren, dass die Anwendung die Benutzeranforderungen erfüllt:

- **Validierung von Anforderungen**:
  - Überprüfung der Erfüllung der User Stories
  - Validierung der nichtfunktionalen Anforderungen (Benutzerfreundlichkeit, Performance)

### Testabdeckung

#### Angestrebte und erreichte Testabdeckung

- **Angestrebte Testabdeckung**:
  - Kernkomponenten (Datenmodelle, Transformationen): >90%
  - Geschäftslogik: >80%
  - GUI-Komponenten: >50%

- **Erreichte Testabdeckung**:
  - Datenmodelle: 83%
  - Datentransformationen: 96%
  - CSV-Importer: 83%
  - Visualisierungskomponenten: 26-96% (je nach Komponente)
  - Gesamtabdeckung: 17% (niedrig aufgrund der nicht getesteten GUI-Komponenten)

#### Kritische Funktionen mit besonderer Testintensität

Folgende Funktionen wurden besonders intensiv getestet:

1. **Datentransformationen**: Umfangreiche Tests für verschiedene Transformationsoperationen, da Fehler hier direkt die Datenqualität und Visualisierungen beeinflussen.
2. **Projektdatenspeicherung**: Gründliche Tests für Speichern und Laden von Projekten, um Datenverlust zu vermeiden.
3. **Observer-Pattern**: Intensive Tests der Benachrichtigungsmechanismen, da diese für die Konsistenz der UI mit dem Datenmodell entscheidend sind.

#### Bewusst nicht getestete Bereiche

Folgende Bereiche wurden bewusst nicht oder nur minimal automatisiert getestet:

1. **GUI-Komponenten**: Die GUI-Komponenten wurden hauptsächlich manuell getestet, da automatisierte GUI-Tests komplex und wartungsintensiv sind.
2. **Matplotlib-Integration**: Die direkte Interaktion mit Matplotlib wurde nur teilweise getestet, da sie stark von der Matplotlib-Bibliothek abhängt.

## Testprotokoll

### Übersicht der durchgeführten Tests

Die folgende Tabelle gibt einen Überblick über die durchgeführten Tests, kategorisiert nach Funktionsbereichen:

| ID | Titel | Beschreibung | Status | Bemerkungen |
|----|-------|-------------|--------|-------------|
| **Datenmodelle** |
| DM-001 | Erstellung von DataSource | Test der korrekten Erstellung und Initialisierung von DataSource-Objekten | Bestanden | |
| DM-002 | Erstellung von Dataset | Test der korrekten Erstellung und Initialisierung von Dataset-Objekten | Bestanden | |
| DM-003 | Erstellung von Visualization | Test der korrekten Erstellung und Initialisierung von Visualization-Objekten | Bestanden | |
| DM-004 | Erstellung von Project | Test der korrekten Erstellung und Initialisierung von Project-Objekten | Bestanden | |
| DM-005 | Änderungsverfolgung im Project | Test der has_unsaved_changes-Methode in verschiedenen Szenarien | Bestanden | |
| DM-006 | Hinzufügen von DataSource zu Project | Test des korrekten Hinzufügens einer DataSource zu einem Project | Bestanden | |
| DM-007 | Hinzufügen von Dataset zu DataSource | Test des korrekten Hinzufügens eines Dataset zu einer DataSource | Bestanden | |
| DM-008 | Hinzufügen von Visualization zu DataSource | Test des korrekten Hinzufügens einer Visualization zu einer DataSource | Bestanden | |
| DM-009 | Entfernen von DataSource aus Project | Test des korrekten Entfernens einer DataSource aus einem Project | Bestanden | |
| DM-010 | Leeren der DataSources in Project | Test des korrekten Leerens der DataSources in einem Project | Bestanden | |
| DM-011 | Mehrere Observer für Project | Test der korrekten Benachrichtigung mehrerer Observer | Bestanden | |
| DM-012 | Entfernen von Observer aus Project | Test des korrekten Entfernens eines Observers aus einem Project | Bestanden | |
| **CSV-Import** |
| CI-001 | Grundlegender CSV-Import | Test des Imports einer CSV-Datei mit Standardoptionen | Bestanden | |
| CI-002 | CSV-Import mit Semikolon-Trennzeichen | Test des Imports einer CSV-Datei mit Semikolon als Trennzeichen | Bestanden | |
| CI-003 | CSV-Import ohne Kopfzeile | Test des Imports einer CSV-Datei ohne Kopfzeile | Bestanden | |
| CI-004 | Import einer leeren CSV-Datei | Test des Verhaltens beim Import einer leeren CSV-Datei | Bestanden | Korrekte Fehlermeldung wird zurückgegeben |
| CI-005 | Erkennung des Trennzeichens | Test der automatischen Erkennung des Trennzeichens in CSV-Dateien | Bestanden | |
| CI-006 | Generierung einer Vorschau | Test der Generierung einer Vorschau für CSV-Dateien | Bestanden | |
| **Datentransformation** |
| DT-001 | Erstellung von Transformationsoperationen | Test der korrekten Erstellung verschiedener Transformationsoperationen | Bestanden | |
| DT-002 | Anwendung von Transformationen auf DataFrame | Test der korrekten Anwendung von Transformationen auf einen DataFrame | Bestanden | |
| DT-003 | Umgang mit fehlenden Werten | Test der korrekten Behandlung fehlender Werte in Transformationen | Bestanden | |
| DT-004 | Typkonvertierung | Test der korrekten Konvertierung von Datentypen | Bestanden | |
| DT-005 | Validierung von Transformationsparametern | Test der korrekten Validierung von Parametern für Transformationen | Bestanden | |
| DT-006 | Serialisierung von Transformationen | Test der korrekten Serialisierung und Deserialisierung von Transformationen | Bestanden | |
| **Projektdatenspeicherung** |
| PS-001 | Speichern eines Projekts | Test des korrekten Speicherns eines Projekts in eine Datei | Bestanden | |
| PS-002 | Laden eines Projekts | Test des korrekten Ladens eines Projekts aus einer Datei | Bestanden | |
| PS-003 | Laden eines nicht existierenden Projekts | Test des Verhaltens beim Laden eines nicht existierenden Projekts | Bestanden | Korrekte Fehlermeldung wird ausgelöst |
| PS-004 | Speichern mit Dateiendungsbehandlung | Test der automatischen Hinzufügung der korrekten Dateiendung | Bestanden | |
| PS-005 | Speichern mit anderer Dateiendung | Test des Ersetzens einer falschen Dateiendung | Bestanden | |
| PS-006 | Änderungsverfolgung nach Speichern | Test der Aktualisierung des gespeicherten Zustands nach dem Speichern | Bestanden | |
| PS-007 | Erstellen eines neuen Projekts | Test der korrekten Erstellung eines neuen Projekts | Bestanden | |
| PS-008 | Speichern und Laden komplexer Projekte | Test des Speicherns und Ladens von Projekten mit mehreren Datenquellen und Visualisierungen | Bestanden | |
| **Observer-Pattern** |
| OP-001 | Hinzufügen und Entfernen von Observern | Test des korrekten Hinzufügens und Entfernens von Observern | Bestanden | |
| OP-002 | Benachrichtigung von Observern | Test der korrekten Benachrichtigung von Observern bei Änderungen | Bestanden | |
| OP-003 | Ungültiger Observer | Test des Verhaltens beim Hinzufügen eines ungültigen Observers | Bestanden | Korrekte Fehlermeldung wird ausgelöst |
| OP-004 | Project als Observable | Test der korrekten Implementierung des Observable-Patterns in der Project-Klasse | Bestanden | |
| OP-005 | Benachrichtigung bei Namensänderung | Test der korrekten Benachrichtigung bei Änderung des Projektnamens | Bestanden | |
| OP-006 | Benachrichtigung bei Änderungen an DataSources | Test der korrekten Benachrichtigung bei Änderungen an DataSources | Bestanden | |
| **Visualisierung** |
| VS-001 | Balkendiagramm-Datenabruf | Test des korrekten Abrufs von Daten für Balkendiagramme | Bestanden | |
| VS-002 | Liniendiagramm-Datenabruf | Test des korrekten Abrufs von Daten für Liniendiagramme | Bestanden | |
| VS-003 | Streudiagramm-Datenabruf | Test des korrekten Abrufs von Daten für Streudiagramme | Bestanden | |
| VS-004 | Kreisdiagramm-Datenabruf | Test des korrekten Abrufs von Daten für Kreisdiagramme | Bestanden | |
| VS-005 | X-Achsen-Datenabruf | Test des korrekten Abrufs von X-Achsen-Daten für verschiedene Diagrammtypen | Bestanden | |
| VS-006 | Y-Achsen-Datenabruf | Test des korrekten Abrufs von Y-Achsen-Daten für verschiedene Diagrammtypen | Bestanden | |
| VS-007 | Diagramm-Rendering | Test des korrekten Renderings verschiedener Diagrammtypen | Bestanden | |
| VS-008 | Farbkonfiguration | Test der korrekten Anwendung von Farbkonfigurationen | Bestanden | |
| VS-009 | Achsenbeschriftungen | Test der korrekten Anwendung von Achsenbeschriftungen | Bestanden | |
| VS-010 | Diagrammtitel | Test der korrekten Anwendung von Diagrammtiteln | Bestanden | |

### Testmetriken

- **Gesamtzahl der Tests**: 81
- **Erfolgsquote**: 100% (alle Tests bestanden)
- **Testabdeckung**: 17% Gesamtabdeckung, mit höherer Abdeckung in kritischen Bereichen:
  - Datenmodelle: 83%
  - Datentransformationen: 96%
  - CSV-Importer: 83%
  - Visualisierungskomponenten: 26-96% (je nach Komponente)

### Gefundene und behobene Fehler

Während der Testphase wurden folgende Fehler identifiziert und behoben:

1. **Inkonsistente Serialisierung von NumPy-Datentypen**: Bei der Serialisierung von Datasets mit NumPy-Datentypen kam es zu Fehlern. Dies wurde durch eine spezielle Behandlung dieser Datentypen behoben.

2. **Fehlerhafte Behandlung leerer CSV-Dateien**: Der CSV-Importer konnte mit leeren Dateien nicht korrekt umgehen. Dies wurde durch eine verbesserte Fehlerbehandlung behoben.

3. **Unvollständige Benachrichtigung bei Änderungen an Collections**: Änderungen an Collections (z.B. Hinzufügen/Entfernen von DataSources) führten nicht immer zu Benachrichtigungen. Dies wurde durch die Implementierung von _TrackingList behoben.

4. **Probleme bei der Typkonvertierung**: Bei der Konvertierung bestimmter Datentypen kam es zu Fehlern. Dies wurde durch robustere Konvertierungsfunktionen behoben.

### Verbleibende bekannte Probleme

Folgende bekannte Probleme bestehen noch:

1. **FutureWarning bei pd.read_json()**: Bei der Verwendung von pd.read_json() mit literalen Strings wird eine FutureWarning-Meldung ausgegeben. Dies sollte durch die Verwendung von io.StringIO-Objekten behoben werden.

2. **Begrenzte Testabdeckung für GUI-Komponenten**: Die GUI-Komponenten haben eine geringe automatisierte Testabdeckung. Dies ist ein bewusstes Design-Entscheidung aufgrund der Komplexität automatisierter GUI-Tests.
