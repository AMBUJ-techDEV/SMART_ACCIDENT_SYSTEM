# SAFAR SARTHI — FULL SYSTEM INTEGRATION ARCHITECTURE

## 1. Overview
Safar Sarthi connects vehicular IoT nodes, smartphone sensors, machine learning accident classification, and an ERSS-112 emergency response network into a unified life-saving pipeline.

```
  +-------------------------+         +-------------------------------+
  |  IoT Node (ESP32/MPU)   |         | Smartphone Android / PWA App |
  |  - 3-Axis Accel (ax,ay) |         | - DeviceMotionEvent Streaming |
  |  - 3-Axis Gyro (gx,gy)  |         | - Real-time GPS Geolocation   |
  +------------+------------+         +---------------+---------------+
               |                                      |
               +------------------+-------------------+
                                  |
                                  v
             +-----------------------------------------+
             | Flask REST Gateway (Backend: Port 5000)  |
             +--------------------+--------------------+
                                  |
            +---------------------+---------------------+
            |                                           |
            v                                           v
+-----------------------+                   +-----------------------+
|  Scikit-Learn ML API  |                   | SQLite3 Persistent DB |
|  - IoT Crash RF Model |                   | - Users, Incidents    |
|  - Phone Impact Model |                   | - Hospitals, Garages  |
|  - Volunteer Dispatch |                   | - Volunteers, OTPs    |
+-----------+-----------+                   +-----------+-----------+
            |                                           |
            +---------------------+---------------------+
                                  |
                                  v
            +-----------------------------------------+
            |      Emergency Response & Safety Hub     |
            |  - Strict 50% Crash Score Threshold     |
            |  - 5-Min Verification Countdown (05:00) |
            |  - Web Audio Siren & Voice Synthesis    |
            |  - AI First-Aid & Anti-Panic Chatbot    |
            |  - Police PCR Van Crowd Control Dispatch|
            |  - Decline Volunteer Victim Safety Cutoff|
            |  - Dual OTP Verification (SMS + Email)  |
            +-----------------------------------------+
```

## 2. Component Directory Reference

| Module | Location | Key Files |
| :--- | :--- | :--- |
| **Frontend** | `C:\MINI PROJECT\FRONTEND` | `index.html`, `style.css`, `manifest.json`, `sw.js`, `icon.svg` |
| **Backend** | `C:\MINI PROJECT\BACKEND` | `app.py`, `safar_sarthi.db`, `requirements.txt`, `start_backend.bat` |
| **Machine Learning** | `C:\MINI PROJECT\ML-SERVICE` | `accident_rf_model.pkl`, `smartphone_accident_model.pkl`, `volunteer_dispatch_model.pkl` |
| **IoT Device Firmware** | `C:\MINI PROJECT\IOT-FIRMWARE` | `firmware.ino` (ESP32 + MPU-6050 + HTTP client) |
| **Android Application** | `C:\MINI PROJECT\ANDROID-APP` | `AccidentDetectionService.kt`, `VerificationActivity.kt`, `AndroidManifest.xml` |
| **Hardware Simulator** | `C:\MINI PROJECT\HARDWARE-SIMULATOR` | `hardware_stimulator.py`, `run_hardware_simulator.bat` |
| **Master Launcher** | `C:\MINI PROJECT\` | `run-safar-sarthi.bat` |
| **Telecom Outbox Log** | `C:\MINI PROJECT\` | `email_dispatch_log.txt` |

## 3. Communication Endpoints

- `POST /api/iot/analyze-crash`: 6-DoF sensor vector classification ($a_x, a_y, a_z, g_x, g_y, g_z, \text{speed}, \Delta v, \theta$).
- `POST /api/predict-smartphone-crash`: Native device motion acceleration analysis.
- `POST /api/chatbot/message`: AI anti-panic and trauma guidance engine.
- `POST /api/auth/send-otp-call`: Mobile phone OTP generation.
- `POST /api/auth/send-otp-email`: Email verification OTP generation.
- `POST /api/auth/register`: Dual-verified registration & email credentials dispatch.
- `POST /api/incidents/<id>/dispatch-police`: Police PCR patrol squad dispatch.
- `POST /api/volunteers/<id>/decline`: Victim safety cutoff revoking live GPS coordinates to suspicious responders.
