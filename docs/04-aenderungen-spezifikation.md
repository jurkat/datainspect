# Dokumentation der Änderungen an der Spezifikation

## Übersicht der Änderungen

Im Laufe der Implementierung wurden einige Anpassungen an der ursprünglichen Spezifikation vorgenommen, um die Anwendung robuster, benutzerfreundlicher und wartbarer zu gestalten. Diese Änderungen betreffen hauptsächlich das Datenmodell und die Beziehungen zwischen den Hauptkomponenten.

## Datenmodell-Änderungen

### 1. Beziehung zwischen DataSource und Dataset

**Ursprüngliche Spezifikation:**
- Eine DataSource konnte mit mehreren Datasets verknüpft sein (1:n-Beziehung)
- Datasets waren direkt mit Project verknüpft

**Neue Implementierung:**
- Eine DataSource ist mit genau einem Dataset verknüpft (1:1-Beziehung)
- Nach dem Import wird ausschließlich mit den transformierten Daten gearbeitet, ohne Aktualisierungsmöglichkeit zur Originaldatenquelle

**Begründung:**
- Vermeidung von Inkonsistenzen zwischen Originaldaten und transformierten Daten
- Klarere Verantwortlichkeiten und einfachere Verwaltung von Beziehungen
- Intuitiveres Modell für Endbenutzer

### 2. Hierarchische Struktur für Visualisierungen

**Ursprüngliche Spezifikation:**
- Visualisierungen waren mit Datasets verknüpft
- Project hatte direkte Referenzen zu Visualisierungen

**Neue Implementierung:**
- Visualisierungen sind hierarchisch der DataSource untergeordnet (1:n-Beziehung)
- Project hat keine direkten Referenzen mehr zu Visualisierungen, sondern nur zu DataSources

**Begründung:**
- Einheitliche hierarchische Struktur (Project → DataSources → Dataset/Visualizations)
- Intuitivere Organisation in der UI mit Visualisierungen direkt unter der Datenquelle
- Direkter Zugriff auf alle Visualisierungen einer Datenquelle

### 3. Eindeutige IDs für alle Modelobjekte

**Ursprüngliche Spezifikation:**
- Keine explizite Anforderung für eindeutige IDs

**Neue Implementierung:**
- Alle Hauptobjekte (Project, DataSource, Visualization) haben eindeutige UUIDs

**Begründung:**
- Einfache und eindeutige Identifikation von Objekten
- Zuverlässige Identifikation auch nach Umbenennungen
- Vorbereitung für mögliche zukünftige Funktionen wie Versionierung oder Synchronisation

### 4. Erweiterte Column-Klasse

**Ursprüngliche Spezifikation:**
- Grundlegende Spaltenattribute waren definiert, aber keine Details zur Typbestimmung

**Neue Implementierung:**
- Automatische Erkennung und Klassifizierung von Datentypen (numerisch, Text, Datum, kategorisch)
- Berechnung statistischer Kennzahlen wie Min, Max, Mittelwert, Median, Standardabweichung
- Speicherung von Metadaten und statistischen Informationen

**Begründung:**
- Keine manuelle Typzuweisung erforderlich
- Bessere Standardeinstellungen für Visualisierungen basierend auf erkannten Typen
- Typspezifische statistische Berechnungen

## Prozess-Änderungen

### 1. Visualisierungserstellungs-Prozess

**Ursprüngliche Spezifikation:**
- Der Nutzer wählt einen Datensatz aus
- Die Visualisierung wird mit dem Dataset verknüpft

**Neue Implementierung:**
- Der Nutzer wählt eine Datenquelle aus
- Die Visualisierung wird der ausgewählten Datenquelle zugeordnet

**Begründung:**
- Konsistenz mit der hierarchischen Struktur
- Intuitivere Benutzerführung
- Vereinfachte Navigation in der Anwendung

## Technische Herausforderungen und Lösungen

### 1. Zirkuläre Importe

**Problem:**
- Bei der Integration der Column-Klasse traten zirkuläre Importprobleme auf

**Lösung:**
- Die Column-Klasse wurde direkt in die models.py-Datei integriert, anstatt sie als separates Modul zu implementieren

### 2. Serialisierung von NumPy-Datentypen

**Problem:**
- NumPy-Datentypen wie int64 sind nicht direkt JSON-serialisierbar

**Lösung:**
- Implementierung einer speziellen to_json-Methode, die NumPy-Datentypen in Python-Standardtypen konvertiert

## Auswirkungen auf die Benutzeroberfläche

Die Änderungen am Datenmodell haben zu einer klareren und intuitiveren Benutzeroberfläche geführt:

1. **Vereinfachte Navigation:** Die hierarchische Struktur ermöglicht eine einfachere Navigation durch die Daten und Visualisierungen
2. **Konsistente Darstellung:** Visualisierungen werden immer im Kontext ihrer Datenquelle angezeigt
3. **Verbesserte Datenanalyse:** Die erweiterte Column-Klasse ermöglicht eine detailliertere Analyse der Daten

## Zusammenfassung

Die vorgenommenen Änderungen an der Spezifikation haben zu einer robusteren, benutzerfreundlicheren und wartbareren Anwendung geführt. Die strikte 1:1-Beziehung zwischen DataSource und Dataset sowie die hierarchische Struktur für Visualisierungen vereinfachen die Architektur und verbessern die Benutzerfreundlichkeit. Die Einführung eindeutiger IDs und die Erweiterung der Column-Klasse bieten zusätzliche Funktionalität und Flexibilität für zukünftige Erweiterungen.
