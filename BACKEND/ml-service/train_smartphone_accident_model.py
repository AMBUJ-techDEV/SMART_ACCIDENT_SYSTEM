"""
============================================================================
SAFAR SARTHI - Smartphone Sensor Crash Detection ML Model Trainer
Trains a Scikit-Learn Classifier on Built-in Smartphone Sensors:
- 3-Axis Accelerometer (g-force)
- 3-Axis Gyroscope (deg/s)
- GPS Speed & Velocity Drop (km/h)
- Phone Rollover / Orientation Angle
============================================================================
"""

import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

def generate_smartphone_sensor_data(num_samples=10000):
    np.random.seed(101)
    
    num_normal = int(num_samples * 0.70)  # 70% Normal driving, handling & phone drops
    num_crash = num_samples - num_normal   # 30% Actual vehicle crashes
    
    # --- 1. NORMAL SMARTPHONE MOTION DATA ---
    # Phone in pocket, dashboard mount, gentle handling, phone accidentally dropped on floor
    norm_ax = np.random.normal(0.0, 0.4, num_normal)
    norm_ay = np.random.normal(0.0, 0.4, num_normal)
    norm_az = np.random.normal(1.0, 0.15, num_normal) # Earth gravity ~ 1.0g
    norm_gx = np.random.normal(0.0, 18.0, num_normal)
    norm_gy = np.random.normal(0.0, 18.0, num_normal)
    norm_gz = np.random.normal(0.0, 18.0, num_normal)
    norm_speed = np.random.uniform(5.0, 110.0, num_normal)
    norm_speed_drop = np.random.normal(0.0, 4.0, num_normal) # Minimal speed drop
    norm_rollover = np.random.normal(0.0, 8.0, num_normal)
    norm_jerk = np.random.normal(0.1, 0.5, num_normal)
    norm_labels = np.zeros(num_normal, dtype=int)
    
    # --- 2. VEHICLE ACCIDENT / CRASH SMARTPHONE DATA ---
    # Violent impact spikes (4g - 16g), sharp angular spin (100 - 500 deg/s), massive speed drop (-30 to -100 km/h)
    crash_ax = np.random.uniform(3.8, 16.0, num_crash) * np.random.choice([-1, 1], num_crash)
    crash_ay = np.random.uniform(3.8, 16.0, num_crash) * np.random.choice([-1, 1], num_crash)
    crash_az = np.random.uniform(2.8, 12.0, num_crash) * np.random.choice([-1, 1], num_crash)
    crash_gx = np.random.uniform(90.0, 480.0, num_crash) * np.random.choice([-1, 1], num_crash)
    crash_gy = np.random.uniform(90.0, 480.0, num_crash) * np.random.choice([-1, 1], num_crash)
    crash_gz = np.random.uniform(90.0, 480.0, num_crash) * np.random.choice([-1, 1], num_crash)
    crash_speed = np.random.uniform(35.0, 140.0, num_crash)
    crash_speed_drop = np.random.uniform(-105.0, -30.0, num_crash) # Severe deceleration
    crash_rollover = np.random.uniform(40.0, 180.0, num_crash)
    crash_jerk = np.random.uniform(12.0, 65.0, num_crash)
    crash_labels = np.ones(num_crash, dtype=int)
    
    X_normal = np.column_stack([norm_ax, norm_ay, norm_az, norm_gx, norm_gy, norm_gz, norm_speed, norm_speed_drop, norm_rollover, norm_jerk])
    X_crash = np.column_stack([crash_ax, crash_ay, crash_az, crash_gx, crash_gy, crash_gz, crash_speed, crash_speed_drop, crash_rollover, crash_jerk])
    
    X = np.vstack([X_normal, X_crash])
    y = np.concatenate([norm_labels, crash_labels])
    
    return X, y

def train_and_save_smartphone_model():
    print("[SAFAR SARTHI ML] Generating 10,000 synthetic smartphone sensor telemetry samples...")
    X, y = generate_smartphone_sensor_data(10000)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("[SAFAR SARTHI ML] Training Random Forest Smartphone Crash Classifier...")
    clf = RandomForestClassifier(n_estimators=150, max_depth=12, random_state=42)
    clf.fit(X_train, y_train)
    
    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    
    print("==========================================================================")
    print(f" Smartphone Sensor Accident Detection Model Accuracy: {acc * 100:.2f}%")
    print("==========================================================================")
    print(classification_report(y_test, preds))
    
    output_dir = os.path.dirname(__file__) or '.'
    model_path = os.path.join(output_dir, 'smartphone_accident_model.pkl')
    joblib.dump(clf, model_path)
    print(f"[SAFAR SARTHI ML] Saved trained smartphone crash model to: {model_path}")

if __name__ == '__main__':
    train_and_save_smartphone_model()
