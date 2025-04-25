#!/bin/bash

# cleanup.sh - Script für die Code-Bereinigung mit autoflake
# DataInspect Projekt
# Erstellt am 24. April 2025

set -e

echo "DataInspect Code-Bereinigung startet..."

# Aktiviere virtuelle Umgebung, falls vorhanden
if [ -d "venv" ]; then
    echo "Aktiviere virtuelle Umgebung..."
    source venv/bin/activate
    PIP_CMD="pip"
    PYTHON_CMD="python"
else
    echo "Warnung: Keine virtuelle Umgebung gefunden. Fahre mit System-Python fort."
    PIP_CMD="pip3"
    PYTHON_CMD="python3"
fi

# Prüfe, ob autoflake installiert ist
if ! $PYTHON_CMD -m autoflake --version &> /dev/null; then
    echo "autoflake ist nicht installiert. Installiere autoflake..."
    $PIP_CMD install autoflake || { echo "Fehler: Konnte autoflake nicht installieren."; exit 1; }
fi

echo "Entferne ungenutzte Imports..."
$PYTHON_CMD -m autoflake --remove-all-unused-imports --recursive --in-place src tests

echo "Entferne ungenutzte Variablen..."
$PYTHON_CMD -m autoflake --remove-unused-variables --recursive --in-place src tests

echo "Führe Pyright-Analyse durch..."
if command -v pyright &> /dev/null; then
    pyright src tests || { echo "Fehler: Pyright hat Typfehler gefunden."; exit 2; }
else
    echo "Warnung: Pyright ist nicht installiert oder nicht im PATH. Überspringe statische Typprüfung."
fi

echo "Code-Bereinigung abgeschlossen."

# Die virtuelle Umgebung wird nicht deaktiviert, da dies das Skript beenden würde
