@echo off
setlocal
cd /d "%~dp0"
echo ============================================
echo   SIRIES UNT - INSTALACION LOCAL
 echo ============================================
where py >nul 2>&1
if errorlevel 1 (
 echo ERROR: no se encontro Python Launcher.
 echo Instala Python 3.11, 3.12 o 3.13 para Windows (64 bits).
 pause
 exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
 py -m venv .venv
 if errorlevel 1 goto :error
)
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :error
".venv\Scripts\python.exe" configurar.py
if errorlevel 1 goto :error
echo.
echo Instalacion y configuracion terminadas.
echo Abre ahora 02_ABRIR_APLICATIVO.bat
pause
exit /b 0
:error
echo.
echo Se produjo un error. Revisa la salida anterior.
pause
exit /b 1
