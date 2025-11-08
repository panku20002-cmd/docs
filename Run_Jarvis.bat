@echo off
cd /d "%~dp0"
echo Installing dependencies (if needed)...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Starting server...
start pythonw server.py
timeout /t 1
start "" "http://127.0.0.1:5000"
exit
