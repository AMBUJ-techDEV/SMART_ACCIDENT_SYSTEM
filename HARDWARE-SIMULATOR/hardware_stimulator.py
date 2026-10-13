"""
================================================================================
SAFAR SARTHI — IOT HARDWARE STIMULATED SENSOR SCRIPT (ESP32 / MPU-6050 SIMULATOR)
Simulates live hardware telemetry over Wi-Fi/HTTP to the Central Emergency Gateway.
Includes:
- Normal cruising telematics (smooth 1.0g gravity, small bumps)
- Speed bump non-crash impact (<50% threshold)
- High-speed frontal impact collision (>50% crash threshold -> triggers auto SOS)
- Vehicle rollover angular tilt & spin (>140 deg/s roll)
================================================================================
"""

import time
import math
import random
import requests
import sys

BACKEND_URL = "http://localhost:5000/api/iot/analyze-crash"
STATUS_URL  = "http://localhost:5000/api/sensors/ESP32-001"

def generate_telemetry_frame(scenario="NORMAL"):
    """Generates 6-DoF inertial sensor metrics (MPU-6050 3-Axis Accel + 3-Axis Gyro)."""
    if scenario == "NORMAL":
        ax = round(random.uniform(-0.15, 0.15), 2)
        ay = round(random.uniform(-0.15, 0.15), 2)
        az = round(random.uniform(0.95, 1.05), 2)
        gx = round(random.uniform(0.5, 3.5), 1)
        gy = round(random.uniform(0.5, 3.5), 1)
        gz = round(random.uniform(0.5, 2.5), 1)
        speed = round(random.uniform(45.0, 60.0), 1)
        speed_change = round(random.uniform(-1.0, 1.0), 1)
        orientation = round(random.uniform(-2.0, 2.0), 1)

    elif scenario == "SPEED_BUMP":
        ax = round(random.uniform(0.1, 0.4), 2)
        ay = round(random.uniform(-0.2, 0.2), 2)
        az = round(random.uniform(1.8, 2.4), 2)  # Vertical spike
        gx = round(random.uniform(5.0, 15.0), 1)
        gy = round(random.uniform(8.0, 20.0), 1)
        gz = round(random.uniform(1.0, 5.0), 1)
        speed = round(random.uniform(20.0, 30.0), 1)
        speed_change = round(random.uniform(-4.0, -2.0), 1)
        orientation = round(random.uniform(1.0, 4.0), 1)

    elif scenario == "FRONTAL_CRASH":
        ax = round(random.uniform(-5.5, -4.2), 2) # Severe deceleration impact
        ay = round(random.uniform(-0.6, 0.6), 2)
        az = round(random.uniform(0.8, 1.4), 2)
        gx = round(random.uniform(15.0, 40.0), 1)
        gy = round(random.uniform(25.0, 50.0), 1)
        gz = round(random.uniform(10.0, 30.0), 1)
        speed = round(random.uniform(60.0, 80.0), 1)
        speed_change = round(random.uniform(-55.0, -42.0), 1) # Velocity drop > 40 km/h
        orientation = round(random.uniform(-18.0, -10.0), 1)

    elif scenario == "ROLLOVER":
        ax = round(random.uniform(1.8, 3.2), 2)
        ay = round(random.uniform(3.5, 5.2), 2)  # Lateral G-spike
        az = round(random.uniform(-0.8, -0.2), 2) # Inversion
        gx = round(random.uniform(140.0, 210.0), 1) # High rotational angular rate
        gy = round(random.uniform(120.0, 180.0), 1)
        gz = round(random.uniform(70.0, 110.0), 1)
        speed = round(random.uniform(50.0, 70.0), 1)
        speed_change = round(random.uniform(-45.0, -35.0), 1)
        orientation = round(random.uniform(75.0, 110.0), 1)

    accel_mag = math.sqrt(ax**2 + ay**2 + az**2)
    return {
        "ax": ax, "ay": ay, "az": az,
        "gx": gx, "gy": gy, "gz": gz,
        "speed": speed, "speed_change": speed_change, "orientation": orientation,
        "accel_magnitude": round(accel_mag, 2),
        "scenario": scenario
    }

def run_hardware_simulation():
    print("=" * 75)
    print("  SAFAR SARTHI — IOT HARDWARE SENSOR STIMULATOR (ESP32 + MPU-6050)")
    print("  Connecting to Gateway: http://localhost:5000")
    print("=" * 75)

    test_sequence = [
        ("NORMAL", 3, "Cruising steadily on Highway NH-24 at 55 km/h..."),
        ("SPEED_BUMP", 2, "Encountered road rumble strip / speed breaker..."),
        ("NORMAL", 2, "Resuming steady driving..."),
        ("FRONTAL_CRASH", 1, "CRITICAL: Severe high-G frontal impact crash detected!"),
        ("ROLLOVER", 1, "CRITICAL: Severe multi-axis rollover detected!")
    ]

    for scenario, repeats, note in test_sequence:
        print(f"\n[PHASE] >> {note}")
        for i in range(repeats):
            frame = generate_telemetry_frame(scenario)
            print(f" -> Telemetry: Ax={frame['ax']}g, Ay={frame['ay']}g, Az={frame['az']}g | Mag={frame['accel_magnitude']}g | Speed={frame['speed']} km/h (Delta={frame['speed_change']})")
            
            try:
                resp = requests.post(BACKEND_URL, json=frame, timeout=3)
                if resp.status_code == 200:
                    data = resp.json()
                    score = data.get('confidencePercentage', 0)
                    pattern = data.get('crashPattern', 'UNKNOWN')
                    is_alert = data.get('isAboveThreshold50', False)
                    badge = "[CRASH SOS TRIGGERED > 50%]" if is_alert else "[NORMAL / SAFE]"
                    print(f"    <- Gateway AI Evaluation: {pattern} | Score: {score}% {badge}")
                else:
                    print(f"    <- Gateway Response: HTTP {resp.status_code}")
            except Exception as e:
                print(f"    <- [SIMULATOR OFFLINE/FALLBACK]: Simulated local computation (Backend unreachable: {e})")
            time.sleep(1.2)

    print("\n" + "=" * 75)
    print("  Hardware Simulation Sequence Complete.")
    print("=" * 75)

if __name__ == '__main__':
    run_hardware_simulation()
