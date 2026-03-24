@echo off
echo Installing requirements...
pip install -r requirements.txt
echo Running AnyQR...
cd src
python main.py
pause
