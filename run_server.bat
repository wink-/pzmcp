@echo off
REM Windows batch file to run the Project Zomboid MCP Server
REM This provides an alternative to Poetry for Claude Desktop integration

cd /d "%~dp0"

REM Try to find Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found in PATH
    echo Please install Python 3.11+ and add it to your PATH
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist ".venv\Scripts\activate.bat" (
    echo Using virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo No virtual environment found, using system Python
)

REM Run the MCP server
python run_server.py

pause