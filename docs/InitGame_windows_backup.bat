@echo off
setlocal

set VENV_DIR=venv

REM Step 1: Create virtual environment
echo Creating virtual environment...
python3 -m venv %VENV_DIR%
if errorlevel 1 (
    echo Failed to create virtual environment.
    exit /b 1
)

REM Step 2: Install dependencies using venv pip
echo Installing dependencies...
%VENV_DIR%\Scripts\pip install --upgrade pip
if exist requirements.txt (
    %VENV_DIR%\Scripts\pip install -r requirements.txt
) else (
    echo No requirements.txt found. Skipping dependency installation.
)

REM Step 3: Create launcher that uses full path to venv python
echo Creating run_main.bat launcher...
(
    echo @echo off
    echo "%~dp0%VENV_DIR%\Scripts\python.exe" "%~dp0sources\main.py"
) > "%~dp0run_main.bat"

REM Step 4: Delete this setup script
echo Cleaning up setup script...
del "%~f0"
