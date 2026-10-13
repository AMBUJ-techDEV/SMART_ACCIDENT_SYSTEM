import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

def generate_synthetic_data(num_samples=5000):
    np.random.seed(42)
    
    # 70% Normal driving, 30% Accidents / Sudden impacts
    num_normal = int(num_samples * 0.7)
    num_accident = num_samples - num_normal
    
    # Normal driving features:
    # accel_x, accel_y ~ N(0, 0.3g), accel_z ~ N(1.0, 0.1g)
    # gyro_x, gyro_y, gyro_z ~ N(0, 15 deg/s)
    # speed ~ Uniform(10, 120 km/h)
    # speed_change ~ N(0, 3 km/h)
    # orientation_change ~ N(0, 5 deg)
    normal_ax = np.random.normal(0.0, 0.3, num_normal)
    normal_ay = np.random.normal(0.0, 0.3, num_normal)
    normal_az = np.random.normal(1.0, 0.1, num_normal)
    normal_gx = np.random.normal(0.0, 15.0, num_normal)
    normal_gy = np.random.normal(0.0, 15.0, num_normal)
    normal_gz = np.random.normal(0.0, 15.0, num_normal)
    normal_speed = np.random.uniform(10.0, 120.0, num_normal)
    normal_speed_change = np.random.normal(0.0, 3.0, num_normal)
    normal_orientation = np.random.normal(0.0, 5.0, num_normal)
    normal_labels = np.zeros(num_normal, dtype=int)
    
    # Accident features:
    # High impact acceleration: spike up to 4g - 15g
    # Sudden angular velocity change: gyro up to 180-500 deg/s
    # Sudden speed drop: speed_change ~ -20 to -90 km/h
    accident_ax = np.random.uniform(3.5, 14.0, num_accident) * np.random.choice([-1, 1], num_accident)
    accident_ay = np.random.uniform(3.5, 14.0, num_accident) * np.random.choice([-1, 1], num_accident)
    accident_az = np.random.uniform(2.5, 12.0, num_accident) * np.random.choice([-1, 1], num_accident)
    accident_gx = np.random.uniform(80.0, 450.0, num_accident) * np.random.choice([-1, 1], num_accident)
    accident_gy = np.random.uniform(80.0, 450.0, num_accident) * np.random.choice([-1, 1], num_accident)
    accident_gz = np.random.uniform(80.0, 450.0, num_accident) * np.random.choice([-1, 1], num_accident)
    accident_speed = np.random.uniform(30.0, 130.0, num_accident)
    accident_speed_change = np.random.uniform(-90.0, -25.0, num_accident)
    accident_orientation = np.random.uniform(35.0, 180.0, num_accident)
    accident_labels = np.ones(num_accident, dtype=int)
    
    X_normal = np.column_stack([normal_ax, normal_ay, normal_az, normal_gx, normal_gy, normal_gz, normal_speed, normal_speed_change, normal_orientation])
    X_accident = np.column_stack([accident_ax, accident_ay, accident_az, accident_gx, accident_gy, accident_gz, accident_speed, accident_speed_change, accident_orientation])
    
    X = np.vstack([X_normal, X_accident])
    y = np.concatenate([normal_labels, accident_labels])
    
    return X, y

def train_and_save_model():
    print("[AI/ML Service] Generating synthetic crash & sensor telemetry dataset...")
    X, y = generate_synthetic_data(6000)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("[AI/ML Service] Training RandomForest Classifier...")
    clf = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42)
    clf.fit(X_train, y_train)
    
    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"[AI/ML Service] Model Accuracy: {acc * 100:.2f}%")
    print(classification_report(y_test, preds))
    
    os.makedirs(os.path.dirname(__file__) or '.', exist_ok=True)
    model_path = os.path.join(os.path.dirname(__file__), 'accident_rf_model.pkl')
    joblib.dump(clf, model_path)
    print(f"[AI/ML Service] Saved trained model artifact to {model_path}")

if __name__ == '__main__':
    train_and_save_model()
