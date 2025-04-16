# Spezifikationsdokument „DataInspect“

## Datenmodell
Das Datenmodell von DataInspect besteht aus mehreren Kernkomponenten, die die Struktur und Beziehungen der in der Anwendung verwendeten Daten definieren.

### Geschäftsobjekte
1. **DataSource**
   - Repräsentiert eine Datenquelle wie eine CSV-, Excel- oder JSON-Datei
   - Speichert Metainformationen wie den Quellentyp und Importzeitpunkt
   - Verwaltet die Rohdaten und bietet Methoden zum Laden und Aktualisieren
2. **Dataset**
   - Stellt einen verarbeiteten Datensatz dar, der aus einer DataSource abgeleitet wurde
   - Enthält die tatsächlichen Daten in einem strukturierten Format
   - Unterstützt Operationen wie Filtern, Sortieren und Gruppieren
   - Berechnet statistische Kennzahlen für numerische Spalten
3. **Column**
   - Repräsentiert eine einzelne Spalte/Variable in einem Dataset
   - Speichert Metadaten wie Name, Datentyp und statistische Informationen
   - Bietet Methoden zur Datentypkonvertierung und zum Umgang mit fehlenden Werten
4. **Visualization**
   - Repräsentiert ein einzelnes Diagramm oder eine Visualisierung
   - Ist mit einem Dataset verknüpft und definiert, welche Spalten visualisiert werden
   - Speichert Konfigurationen wie Diagrammtyp, Farben, Beschriftungen und Achseneinstellungen
5. **Project**
   - Repräsentiert ein Projekt in der Anwendung
   - Enthält DataSources, Datasets und Visualizations
   - Speichert Projektmetadaten wie Name, Erstellungsdatum und letzte Änderung
   - Ermöglicht das Speichern und Laden des gesamten Projektstatus

---

## UML-Klassendiagramm

<div align="center">

```mermaid
classDiagram
    direction LR
    
    DataSource "1" --> "1" Dataset
    Dataset "1" --> "*" Column
    Dataset "1" --> "*" Visualization
    Project "1" --> "*" DataSource
    Project "1" --> "*" Dataset
    Project "1" --> "*" Visualization
    
    class DataSource {
        -sourceType: String
        -path: String
        +loadData()
        +refresh()
    }
    
    class Dataset {
        -data: DataFrame
        -columns: Column[]
        -metadata: Object
        +filter(criteria)
        +sort(column, order)
        +group(columns, agg)
        +getStats()
    }
    
    class Column {
        -name: String
        -dataType: String
        -stats: Object
        +convert(type)
        +handleMissing(strategy)
    }
    
    class Visualization {
        -chartType: String
        -title: String
        -xAxis: String
        -yAxis: String
        -colors: String[]
        -labels: String[]
        +render()
        +export(format)
    }
    
    class Project {
        -name: String
        -created: Date
        -modified: Date
        -dataSources: DataSource[]
        -datasets: Dataset[]
        -visualizations: Visualization[]
        +save()
        +load()
    }
```

</div>

---

## Geschäftsprozesse
DataInspect unterstützt verschiedene Geschäftsprozesse, die zusammen den Workflow von der Datenquelle bis zur fertigen Visualisierung abbilden.

### Hauptprozesse
1. **Datenimport-Prozess**
   - Der Nutzer wählt eine Datenquelle aus (Datei auswählen oder Datenbankverbindung herstellen)
   - Das System überprüft die Datenquelle auf Gültigkeit und Format
   - Das System liest die Daten ein und zeigt eine Vorschau an
   - Der Nutzer kann Importoptionen anpassen (z.B. Trennzeichen bei CSV-Dateien)
   - Das System erstellt ein Dataset aus der Datenquelle
   - Der Nutzer kann den importierten Datensatz in der Anwendung verwenden
2. **Datenvorverarbeitungs-Prozess**
   - Der Nutzer wählt einen Datensatz aus
   - Das System zeigt die verfügbaren Daten in tabellarischer Form an
   - Der Nutzer kann Operationen wie Filtern, Sortieren oder Gruppieren auswählen
   - Das System führt die Operation aus und zeigt das Ergebnis an
   - Der Nutzer kann mehrere Operationen nacheinander ausführen
   - Der Nutzer kann den verarbeiteten Datensatz für Visualisierungen verwenden
3. **Visualisierungserstellungs-Prozess**
   - Der Nutzer wählt einen Datensatz aus
   - Der Nutzer wählt einen Diagrammtyp aus einer Liste verfügbarer Visualisierungen
   - Das System zeigt eine Vorschau der Standardvisualisierung
   - Der Nutzer wählt Spalten für die relevanten Achsen/Dimensionen aus
   - Der Nutzer passt Visualisierungsoptionen an (Farben, Titel, Beschriftungen)
   - Das System rendert die angepasste Visualisierung
   - Der Nutzer kann mit der Visualisierung interagieren (zoomen, filtern, usw.)
4. **Export-Prozess**
   - Der Nutzer wählt eine fertige Visualisierung aus
   - Der Nutzer wählt das gewünschte Exportformat (PNG, JPEG, PDF)
   - Der Nutzer passt ggf. Exportoptionen an (Auflösung, Qualität)
   - Das System generiert die Exportdatei
   - Der Nutzer wählt den Speicherort aus
   - Das System speichert die Datei am gewünschten Ort
5. **Projektverwaltungs-Prozess**
   - Der Nutzer kann ein neues Projekt erstellen
   - Der Nutzer kann das aktuelle Projekt speichern
   - Der Nutzer kann ein bestehendes Projekt laden
   - Das System lädt alle Datenquellen, Datensätze und Visualisierungen aus dem Projekt

---

## UML-Aktivitätsdiagramm für den Visualisierungserstellungs-Prozess

<div align="center">

```mermaid
flowchart TB
    %% Vorbereitung
    Start([Start]) --> A[Datensatz auswählen]
    A --> B[Diagrammtyp auswählen]
    B --> C[Vorschau anzeigen]
    C --> D[Spalten für Achsen wählen]
    D --> E{Standardoptionen OK?}
    
    %% Kompakte Anpassungsprozesse
   F[Optionen anpassen] --> G[Visualisierung rendern]
   J[Weitere Anpassungen] --> G
   G --> H{Mit Ergebnis zufrieden?}
   H -->|Nein| J
 
    %% Hauptflussverbindungen
    E -->|Nein| F
    E -->|Ja| G
    H -->|Ja| I[Visualisierung speichern]
    
    %% Export-Entscheidung
    I --> K{Exportieren?}
    K -->|Ja| L[Export starten]
    K -->|Nein| Ende([Ende])
    L --> Ende
    
    %% Visuelle Hinweise zur Gruppierung
    classDef vorbereitung fill:#e1f5fe,stroke:#01579b
    classDef anpassung fill:#e8f5e9,stroke:#2e7d32
    classDef abschluss fill:#fff3e0,stroke:#ff6f00
    
    class A,B,C,D,E vorbereitung
    class F,G,H,J anpassung
    class I,K,L,Ende abschluss
```

</div>

---

## Geschäftsregeln
Für DataInspect gelten folgende Geschäftsregeln, die für die korrekte Funktion und Nutzung der Anwendung essentiell sind:

### Datenquellen und Datensätze
- Eine Datenquelle muss mindestens eine Spalte und eine Zeile enthalten
- Jede Spalte muss einen eindeutigen Namen haben
- Datentypen müssen konsistent innerhalb einer Spalte sein oder konvertierbar sein
- Fehlende Werte müssen gekennzeichnet sein (z.B. durch NULL, NA, leere Zelle)
- Die maximale Größe einer importierbaren Datei ist auf 100 MB begrenzt

### Visualisierungen
- Jede Visualisierung muss mit genau einem Datensatz verknüpft sein
- Balken- und Liniendiagramme benötigen mindestens eine X-Achsen- und eine Y-Achsen-Spalte
- Kreisdiagramme benötigen eine Kategorie-Spalte und eine Werte-Spalte
- Streudiagramme benötigen zwei numerische Spalten (X und Y)
- Numerische Achsen müssen einen gültigen Minimalwert und Maximalwert haben
- Der Abstand von Werten auf den Achsen muss proportional zu den tatsächlichen Werten sein

### Datenbearbeitung
- Bei der Datenfilterung müssen alle anzuwendenden Filterbedingungen gültig sein
- Bei der Datensortierung muss mindestens eine Spalte als Sortierkriterium angegeben werden
- Bei der Datengruppierung müssen Aggregationsfunktionen für numerische Spalten angegeben werden
- Statistische Berechnungen sind nur für numerische Spalten zulässig
- Transformationen müssen den Datentyp einer Spalte respektieren oder eine explizite Typkonvertierung durchführen

### Projekte
- Jedes Projekt muss einen eindeutigen Namen haben
- Ein Projekt kann mehrere Datenquellen, Datensätze und Visualisierungen enthalten
- Änderungen am Projekt müssen explizit gespeichert werden, um persistiert zu werden
- Projektdateien müssen ein definiertes Format haben (.dinsp-Dateierweiterung)
- Beim Laden eines Projekts müssen alle referenzierten Datenquellen verfügbar sein

### Export
- Exportierte Bilddateien müssen mindestens eine Auflösung von 300 dpi haben
- Bei PDF-Export müssen alle Schriftarten eingebettet werden
- Die maximale Größe für exportierte Dateien beträgt 50 MB

---

## Systemschnittstellen
DataInspect kommuniziert mit verschiedenen externen Systemen und Datenquellen über definierte Schnittstellen:

1. **Dateisystem**
   - Zweck: Import von Datendateien, Speichern/Laden von Projekten, Export von Visualisierungen
   - Protokoll: Direkte Dateioperationen über das Betriebssystem
   - Datenformat: CSV, Excel (XLSX/XLS), JSON für Import; projektspezifisches Format (.dinsp) für Projekte; PNG, JPEG, PDF für Export
2. **SQLite-Datenbanken**
   - Zweck: Zugriff auf strukturierte Daten in lokalen SQLite-Datenbanken
   - Protokoll: SQLite3 API über entsprechende Python-Bibliothek
   - Datenformat: SQL-Abfragen und -Ergebnisse
3. **Zwischenablage**
   - Zweck: Ermöglicht Kopieren und Einfügen von Daten zwischen der Anwendung und anderen Programmen
   - Protokoll: Betriebssystem-Zwischenablage
   - Datenformat: Tabellendaten (TSV), Bilder
4. **Python-Bibliotheken**
   - Zweck: Nutzung externer Bibliotheken für Datenverarbeitung (Pandas) und Visualisierung (Matplotlib)
   - Protokoll: Python-Module und API-Aufrufe
   - Datenformat: Python-Objekte (Pandas DataFrames, Matplotlib-Figuren)

---

## Benutzerschnittstellen
DataInspect verfügt über eine grafische Benutzeroberfläche, die auf Benutzerfreundlichkeit und Intuitivität ausgelegt ist. Im Folgenden werden die wichtigsten Dialogelemente beschrieben:

### Hauptfenster
Das Hauptfenster ist das zentrale Element der Anwendung und besteht aus mehreren Bereichen:
- **Menüleiste:** Enthält Hauptmenüs für Datei, Bearbeiten, Ansicht, Daten, Visualisierung und Hilfe
- **Werkzeugleiste:** Bietet schnellen Zugriff auf häufig verwendete Funktionen
- **Datenverwaltungsbereich (linke Seitenleiste):** Zeigt verfügbare Datenquellen, Datensätze und Visualisierungen hierarchisch an
- **Hauptarbeitsbereich (zentral):** Zeigt je nach Kontext die aktuelle Datenvorschau oder Visualisierung
- **Eigenschaftenbereich (rechte Seitenleiste):** Zeigt Eigenschaften des aktuell ausgewählten Elements und ermöglicht Anpassungen
- **Statusleiste:** Zeigt Informationen zum aktuellen Status der Anwendung und laufenden Operationen

### Dialog: Datenimport
Der Datenimport-Dialog wird geöffnet, wenn der Nutzer neue Daten importieren möchte:
- **Dateityp-Auswahl:** Dropdown-Menü zur Auswahl des zu importierenden Dateityps (CSV, Excel, JSON)
- **Dateiauswahl:** Datei-Browser zur Auswahl der zu importierenden Datei
- **Vorschaubereich:** Zeigt eine Vorschau der zu importierenden Daten
- **Importoptionen:** Spezifische Optionen je nach Dateityp (z.B. Trennzeichen für CSV)
- **Schaltflächen:** "Importieren", "Abbrechen"

### Dialog: Diagrammerstellung
Der Diagrammerstellungs-Dialog wird verwendet, um neue Visualisierungen zu erstellen:
- **Diagrammtyp-Auswahl:** Visuelle Auswahl der verfügbaren Diagrammtypen mit Miniaturansichten
- **Spaltenzuordnung:** Drag-and-Drop-Bereich zur Zuordnung von Datenspalten zu Diagrammelementen (X-Achse, Y-Achse, Farbe, Größe, etc.)
- **Diagrammvorschau:** Live-Vorschau des aktuell konfigurierten Diagramms
- **Anpassungsoptionen:** Einstellungen für Farben, Beschriftungen, Skalen, etc.
- **Schaltflächen:** "Erstellen", "Abbrechen"

### Dialog: Exportoptionen
Der Export-Dialog ermöglicht die Konfiguration des Exports:
- **Format-Auswahl:** Auswahl des Exportformats (PNG, JPEG, PDF)
- **Größeneinstellungen:** Eingabefelder für Breite und Höhe der Ausgabe
- **Qualitätseinstellungen:** Schieberegler für Qualität/Kompression (bei JPEG)
- **Optionen:** Zusätzliche formatspezifische Optionen
- **Vorschau:** Vorschau des zu exportierenden Elements
- **Schaltflächen:** "Exportieren", "Abbrechen"

---

## Dialogflüsse
Die Hauptdialogflüsse in der Anwendung sind:
1. **Datenimport-Fluss:** Hauptfenster → Menü "Datei" → "Daten importieren" → Datenimport-Dialog → Dateiauswahl → Importoptionen anpassen → Vorschau prüfen → "Importieren" → Hauptfenster (mit importierten Daten)
2. **Visualisierungserstellungs-Fluss:** Hauptfenster → Menü "Visualisierung" → "Neue Visualisierung" → Diagrammerstellungs-Dialog → Diagrammtyp auswählen → Spalten zuordnen → Anpassungen vornehmen → "Erstellen" → Hauptfenster (mit neuer Visualisierung)
3. **Export-Fluss:** Hauptfenster (mit ausgewählter Visualisierung) → Menü "Datei" → "Exportieren" → Exportoptionen-Dialog → Format und Optionen wählen → "Exportieren" → Datei-Browser (zur Speicherortwahl) → Hauptfenster

---

## Eingabevalidierung
Die Anwendung validiert Benutzereingaben nach folgenden Regeln:
- **Dateinamen:** Müssen gültige Dateipfade ohne unerlaubte Zeichen sein
- **Numerische Eingaben:** Müssen gültige Zahlen im erlaubten Bereich sein
- **Textfelder:** Dürfen keine leeren Werte haben, wenn sie erforderlich sind
- **Formatierungsangaben:** Müssen syntaktisch korrekt sein (z.B. Datumsformate)

Bei ungültigen Eingaben werden dem Benutzer klare Fehlermeldungen angezeigt, die das Problem und mögliche Lösungen beschreiben.
