@echo off
cd /d "%~dp0"
set "PY=%LOCALAPPDATA%\Programs\Python\Python314\python.exe"
if not exist "%PY%" (
  echo No se encontro Python 3.14 en: %PY%
  echo Abre VS Code y ejecuta la aplicacion desde la terminal.
  pause
  exit /b 1
)
"%PY%" -m streamlit run app.py
pause
