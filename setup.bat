@echo off
REM Creates a virtual environment and installs the dependencies for Windows
REM Run this script to set up the development environment on Windows

REM Check if Python is installed
python --version > NUL 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.
    exit /b 1
)

REM Create virtual environment if it doesn't exist yet
if not exist venv\ (
    echo Creating virtual Python environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Setup completed. To activate the virtual environment, run 'venv\Scripts\activate.bat'.
echo To start the application, run 'python main.py'.
