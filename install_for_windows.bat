@echo off
REM Install dependencies for Windows Python installation

echo Installing dependencies for Project Zomboid MCP Server...
echo =======================================================

REM Use the same Python path that Claude Desktop is trying to use
set PYTHON_PATH=C:\Users\winkk\AppData\Local\Programs\Python\Python313\python.exe

echo Using Python: %PYTHON_PATH%

REM Check if Python exists
if not exist "%PYTHON_PATH%" (
    echo Error: Python not found at %PYTHON_PATH%
    echo Please check your Python installation
    pause
    exit /b 1
)

REM Run the Python installer script
cd /d "%~dp0"
echo.
echo Running Python dependency installer...
"%PYTHON_PATH%" install_windows_deps.py

echo.
echo Testing the standalone server...
"%PYTHON_PATH%" run_server_standalone.py

pause