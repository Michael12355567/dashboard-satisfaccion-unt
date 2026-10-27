@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
 echo Primero ejecuta 01_INSTALAR_Y_CONFIGURAR.bat
 pause
 exit /b 1
)
echo Abre en el navegador: http://127.0.0.1:8501
echo Para detener el servidor, cierra esta ventana o pulsa Ctrl+C.
".venv\Scripts\python.exe" -m streamlit run app.py --server.address=127.0.0.1 --server.port=8501
pause
