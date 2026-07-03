@echo off
REM This script runs Jarvis and keeps the window open so you can see the output

REM Navigate to this script's directory
cd /d "%~dp0"

REM Run Python script
python jarvis.py

REM Keep window open so you can see results
pause
