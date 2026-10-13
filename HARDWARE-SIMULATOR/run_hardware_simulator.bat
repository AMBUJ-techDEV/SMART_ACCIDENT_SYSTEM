@echo off
title SAFAR SARTHI -- HARDWARE SENSOR STIMULATOR
cd /d "%~dp0"
echo ======================================================================
echo   SAFAR SARTHI HARDWARE ACCIDENT STIMULATOR (ESP32 / MPU-6050)
echo ======================================================================
echo Streaming telemetry frames to http://localhost:5000...
python hardware_stimulator.py
pause
