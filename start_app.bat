@echo off

echo ===============================
echo Employee Asset Portal Starting
echo ===============================

cd /d "%~dp0"


echo Installing required packages...

python -m pip install -r requirements.txt


echo Starting Application...

python -m streamlit run app.py


pause