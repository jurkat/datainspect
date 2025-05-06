@echo off
REM Creates a virtual environment and installs the dependencies for Windows
REM Run this script to set up the development environment on Windows

REM Check if Python is installed and if it's version 3.12
python --version > temp.txt 2>&1
set /p PY_VERSION=<temp.txt
del temp.txt

echo Found: %PY_VERSION%

if not "%PY_VERSION:~0,10%" == "Python 3.12" (
    echo Warning: %PY_VERSION% found, but Python 3.12 is required.
    echo The application may not work correctly with other versions.
    pause
)

if "%PY_VERSION%" == "" (
    echo Python is not installed. Please install Python 3.12.
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

REM Install development tools
echo Installing development tools...
pip install autoflake
pip install pyright

echo.
echo Setup completed. To activate the virtual environment, run 'venv\Scripts\activate.bat'.
echo To start the application, run 'python main.py'.
