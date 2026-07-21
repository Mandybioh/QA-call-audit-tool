@echo off
REM Install dependencies
echo Installing required packages...
set "PY=.venv-1\Scripts\python.exe"
if not exist "%PY%" set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
"%PY%" -m pip install -r requirements.txt
pause
