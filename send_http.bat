@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"
python "%SCRIPT_DIR%send_http.py" %*
