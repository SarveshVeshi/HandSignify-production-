@echo off
SETLOCAL EnableDelayedExpansion

echo ===================================================
echo   HandSignify Project Setup Script
echo ===================================================

:: 1. Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

:: 2. Create Virtual Environment
if not exist .venv (
    echo [INFO] Creating virtual environment (.venv)...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created.
) else (
    echo [INFO] Virtual environment (.venv) already exists.
)

:: 3. Activate and Install Dependencies
echo [INFO] Installing/Updating dependencies from requirements.txt...
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo [SUCCESS] Dependencies installed.

:: 4. Environment Configuration
if not exist .env (
    if exist .env.example (
        echo [INFO] Creating .env from .env.example...
        copy .env.example .env
        echo [SUCCESS] .env file created. Please update it with your credentials.
    ) else (
        echo [WARNING] .env.example not found. Please create a .env file manually.
    )
) else (
    echo [INFO] .env file already exists.
)

:: 5. Create instance directory for database
if not exist instance (
    echo [INFO] Creating instance directory...
    mkdir instance
)

echo ===================================================
echo [FINAL SUCCESS] Setup complete!
echo To start the server, run: server.bat start
echo ===================================================
pause
exit /b 0
