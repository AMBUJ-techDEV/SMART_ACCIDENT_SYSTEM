@echo off
title SAFAR SARTHI -- CENTRAL SYSTEM LAUNCHER
cd /d "%~dp0"
echo ======================================================================
echo   SAFAR SARTHI -- SMART ACCIDENT RESPONSE SYSTEM
echo   Unified Production Launcher (Frontend + Backend + ML Engine)
echo ======================================================================
echo [1/3] Initializing SQLite database and loading Machine Learning models...
cd /d "%~dp0BACKEND"
start "Safar Sarthi Backend" /min cmd /c "python app.py"

echo [2/3] Waiting for backend gateway initialization (3 seconds)...
timeout /t 3 /nobreak >nul

echo [3/3] Opening Safar Sarthi Mobile/Desktop Web App...
start http://localhost:5000

echo ======================================================================
echo   SYSTEM ONLINE AT: http://localhost:5000
echo   - Citizen App & Central SOS Trigger
echo   - AI First-Responder & Anti-Panic Chatbot Companion
echo   - Dual OTP Verification (Phone + Email)
echo   - ERSS-112 & Police Control Room Radar Map
echo   - IoT 6-DoF Accident Telemetry Oscilloscope
echo ======================================================================
echo To stop the system, close the background backend window or command prompt.
pause
