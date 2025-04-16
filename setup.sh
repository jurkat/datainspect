#!/bin/bash

# Creates a virtual environment and installs the dependencies
# Run this script to set up the development environment

# Check if Python is installed and which command to use
PYTHON_CMD=""

# Check first for 'python', e.g., with Homebrew or aliases
if command -v python &> /dev/null; then
    # Make sure it's Python 3
    PY_VERSION=$(python --version 2>&1)
    if [[ $PY_VERSION == *"Python 3"* ]]; then
        PYTHON_CMD="python"
        echo "Python 3 found: $PY_VERSION"
    fi
fi

# If 'python' was not found or not version 3, check for 'python3'
if [ -z "$PYTHON_CMD" ] && command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo "Python 3 found: $(python3 --version)"
fi

# If neither 'python' nor 'python3' was found, exit with error
if [ -z "$PYTHON_CMD" ]; then
    echo "Python 3 is not installed. Please install Python 3."
    exit 1
fi

# Create virtual environment if it doesn't exist yet
if [ ! -d "venv" ]; then
    echo "Creating virtual Python environment..."
    $PYTHON_CMD -m venv venv
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup completed. To activate the virtual environment, run 'source venv/bin/activate'."
echo "To start the application, run 'python main.py'."
