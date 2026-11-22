@echo off
setlocal
set "PYTHONUTF8=1"
py.exe -3 -c "import sys" >nul 2>&1
if errorlevel 1 (
    python.exe "%~dp0run_week2.py"
) else (
    py.exe -3 "%~dp0run_week2.py"
)
set "RESULT=%ERRORLEVEL%"
pause
exit /b %RESULT%
