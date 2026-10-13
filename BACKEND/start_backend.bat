@echo off
title SAFAR SARTHI BACKEND SERVICE
cd /d "%~dp0"
echo ======================================================================
echo   SAFAR SARTHI -- SMART ACCIDENT RESPONSE SYSTEM (BACKEND SERVER)
echo ======================================================================
echo Starting Flask Server and ML Inference Pipeline...
python app.py
pause
