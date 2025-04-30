#!/bin/bash

# cleanup.sh - Script for code cleanup with autoflake
# DataInspect Project
# Created on April 24, 2025

set -e

echo "DataInspect code cleanup starting..."

# Activate virtual environment if available
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
    PIP_CMD="pip"
    PYTHON_CMD="python"
else
    echo "Warning: No virtual environment found. Continuing with system Python."
    PIP_CMD="pip3"
    PYTHON_CMD="python3"
fi

# Check if autoflake is installed
if ! $PYTHON_CMD -m autoflake --version &> /dev/null; then
    echo "autoflake is not installed. Installing autoflake..."
    $PIP_CMD install autoflake || { echo "Error: Could not install autoflake."; exit 1; }
fi

echo "Removing unused imports..."
$PYTHON_CMD -m autoflake --remove-all-unused-imports --recursive --in-place src tests

echo "Removing unused variables..."
$PYTHON_CMD -m autoflake --remove-unused-variables --recursive --in-place src tests

echo "Running Pyright analysis..."
if command -v pyright &> /dev/null; then
    pyright src tests || { echo "Error: Pyright found type errors."; exit 2; }
else
    echo "Warning: Pyright is not installed or not in PATH. Skipping static type checking."
fi

echo "Code cleanup completed."

# The virtual environment is not deactivated as this would terminate the script
