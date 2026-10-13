import os
import joblib
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'accident_rf_model.pkl')
model = None

def load_ml_model():
    global model
    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            print("[AI/ML Service] Loaded Random Forest model successfully.")
        except Exception as e:
            print(f"[AI/ML Service] Could not load model file: {e}")
    else:
        print("[AI/ML Service] Model file not found. Running training on startup...")
        try:
            from train_model import train_and_save_model
            train_and_save_model()
            if os.path.exists(MODEL_PATH):
                model = joblib.load(MODEL_PATH)
        except Exception as ex:
            print(f"[AI/ML Service] Training error: {ex}")

load_ml_model()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "service": "SADERS AI/ML Prediction Engine",
        "status": "UP",
        "model_loaded": model is not None,
        "disclaimer": "Academic Prototype ML Service - Not certified for critical medical/legal use."
    })

@app.route('/predict', methods=['POST'])
def predict_accident():
    try:
        data = request.get_json(force=True)
        ax = float(data.get('acceleration_x', 0.0))
        ay = float(data.get('acceleration_y', 0.0))
        az = float(data.get('acceleration_z', 1.0))
        gx = float(data.get('gyro_x', 0.0))
        gy = float(data.get('gyro_y', 0.0))
        gz = float(data.get('gyro_z', 0.0))
        speed = float(data.get('speed', 0.0))
        speed_change = float(data.get('speed_change', 0.0))
        orientation = float(data.get('orientation', 0.0))

        # Build feature vector
        features = np.array([[ax, ay, az, gx, gy, gz, speed, speed_change, orientation]])

        if model is not None:
            proba = model.predict_proba(features)[0]
            accident_score = float(proba[1])
        else:
            # Rule-based fallback if ML model is missing
            accel_mag = np.sqrt(ax**2 + ay**2 + az**2)
            gyro_mag = np.sqrt(gx**2 + gy**2 + gz**2)
            score = 0.1
            if accel_mag > 3.0: score += 0.4
            if abs(speed_change) > 25.0: score += 0.3
            if gyro_mag > 90.0: score += 0.2
            accident_score = min(1.0, score)

        confidence_pct = int(round(accident_score * 100))

        # Severity categorization
        if accident_score >= 0.85:
            severity = "CRITICAL" if abs(speed_change) > 60 or np.sqrt(ax**2+ay**2+az**2) > 8 else "HIGH"
        elif accident_score >= 0.60:
            severity = "MEDIUM"
        elif accident_score >= 0.35:
            severity = "LOW"
        else:
            severity = "NONE"

        # AI Explainability features
        reasons = []
        accel_total = np.sqrt(ax**2 + ay**2 + az**2)
        gyro_total = np.sqrt(gx**2 + gy**2 + gz**2)

        if accel_total > 3.0:
            reasons.append(f"High impact acceleration spike detected ({accel_total:.2f}g)")
        if abs(speed_change) > 20.0:
            reasons.append(f"Sudden speed change detected ({speed_change:.1f} km/h)")
        if gyro_total > 80.0:
            reasons.append(f"Abnormal rotational movement ({gyro_total:.1f} deg/s)")
        if abs(orientation) > 40.0:
            reasons.append(f"Significant vehicle orientation tilt ({orientation:.1f}°)")

        if not reasons:
            reasons.append("Telemetry parameters within normal driving baseline thresholds")

        response = {
            "accident_score": round(accident_score, 4),
            "confidence_percentage": confidence_pct,
            "severity": severity,
            "is_accident": accident_score >= 0.60,
            "explainability_reasons": reasons,
            "model_version": "RandomForest_v1.0_AcademicPrototype"
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    print(f"[AI/ML Service] Starting Flask server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)
