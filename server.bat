@echo off
SET PORT=5001

if "%1"=="start" (
    echo [INFO] Starting HandSignify Server on port %PORT%...
    :: Check if port is already in use (more specific check)
    netstat -ano | findstr /R /C:":%PORT% " > nul
    if not errorlevel 1 (
        echo [ERROR] Port %PORT% is already in use. Try 'server.bat stop' first.
        exit /b 1
    )
    :: Start in background using virtual environment
    start /B .\.venv\Scripts\python.exe app.py
    echo [SUCCESS] Server starting in background. Please wait 10 seconds...
    exit /b 0
)

if "%1"=="stop" (
    echo [INFO] Stopping HandSignify Server...
    :: Check if port is in use first
    netstat -ano | findstr /R /C:":%PORT% " > nul
    if errorlevel 1 (
        echo [INFO] No server found running on port %PORT%.
        exit /b 0
    )
    :: Kill process using port 5000 via PowerShell for accuracy
    powershell -Command "Get-NetTCPConnection -LocalPort %PORT% -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }"
    
    :: Verify it stopped
    timeout /t 2 /nobreak > nul
    netstat -ano | findstr /R /C:":%PORT% " > nul
    if errorlevel 1 (
        echo [SUCCESS] Server stopped.
    ) else (
        echo [ERROR] Failed to stop server. Port %PORT% is still in use.
    )
    exit /b 0
)

echo Usage: server.bat [start^|stop]
exit /b 1
