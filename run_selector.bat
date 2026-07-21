@echo off
REM Run the combined QA platform home page
echo Starting QA Audit Platform Home...
set "PY=.venv-1\Scripts\python.exe"
if not exist "%PY%" set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
"%PY%" -m streamlit run home.py
pause
