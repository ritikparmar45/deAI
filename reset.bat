@echo off
setlocal
cd /d "%~dp0"
if "%~1"=="" (
    echo ❌ Error: Email required.
    echo Usage: reset.bat ^<email^>
    exit /b 1
)
.\venv\Scripts\python.exe reset_password.py %*
endlocal
