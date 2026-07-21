@echo off
REM Run the Analytics Dashboard
echo Starting QA Audit Dashboard...
set "PY=.venv-1\Scripts\python.exe"
if not exist "%PY%" set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
"%PY%" -m streamlit run dashboard.py
pause
