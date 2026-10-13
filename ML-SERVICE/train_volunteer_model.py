"""
============================================================================
SAFAR SARTHI - Government-Certified Volunteer Dispatch ML Model Trainer
Trains a Scikit-Learn Random Forest Classifier on Synthetic Volunteer Data
Targeting Optimal First Responder Matching & Rapid CPR Dispatch
============================================================================
"""

import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

def generate_volunteer_dataset(num_samples=8000):
    np.random.seed(42)
    
    # Feature 1: Distance to incident (0.1 km to 10.0 km)
    distance_km = np.random.uniform(0.1, 10.0, num_samples)
    
    # Feature 2: Certification Level (1: Basic, 2: CPR/AED, 3: Advanced First Aid, 4: Govt Paramedic/Doctor)
    cert_level = np.random.choice([1, 2, 3, 4], size=num_samples, p=[0.3, 0.4, 0.2, 0.1])
    
    # Feature 3: Past Response Time in Minutes (1 to 20 mins)
    historical_response_mins = np.random.uniform(1.0, 20.0, num_samples)
    
    # Feature 4: Volunteer Reliability Rating (1.0 to 5.0 Stars)
    reliability_rating = np.random.uniform(1.0, 5.0, num_samples)
    
    # Feature 5: Availability Status (1: Available, 0: Off Duty)
    is_active_duty = np.random.choice([0, 1], size=num_samples, p=[0.25, 0.75])
    
    # Feature 6: Victim Crash Severity Score (0.70 to 1.00)
    victim_severity_score = np.random.uniform(0.70, 1.00, num_samples)
    
    # Calculate Dispatch Suitability Index to create realistic ground truth labels
    # High suitability = Close distance (< 3.0 km), Active Duty (1), High Cert Level (>=2), Good Rating (>= 3.5)
    suitability_score = (
        (10.0 - distance_km) * 2.5 +
        cert_level * 3.0 +
        (20.0 - historical_response_mins) * 1.5 +
        reliability_rating * 4.0 +
        is_active_duty * 15.0 +
        victim_severity_score * 5.0
    )
    
    # Target label: 1 if suitability is in top 40%, else 0
    threshold = np.percentile(suitability_score, 60)
    y = (suitability_score >= threshold).astype(int)
    
    X = np.column_stack([
        distance_km,
        cert_level,
        historical_response_mins,
        reliability_rating,
        is_active_duty,
        victim_severity_score
    ])
    
    return X, y

def train_and_save_volunteer_model():
    print("[SAFAR SARTHI ML] Generating 8,000 synthetic volunteer responder records...")
    X, y = generate_volunteer_dataset(8000)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("[SAFAR SARTHI ML] Training Random Forest Volunteer Dispatch Model...")
    clf = RandomForestClassifier(n_estimators=120, max_depth=10, random_state=42)
    clf.fit(X_train, y_train)
    
    predictions = clf.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    
    print("==========================================================================")
    print(f" Volunteer Dispatch ML Model Accuracy: {acc * 100:.2f}%")
    print("==========================================================================")
    print(classification_report(y_test, predictions))
    
    output_dir = os.path.dirname(__file__) or '.'
    model_path = os.path.join(output_dir, 'volunteer_dispatch_model.pkl')
    joblib.dump(clf, model_path)
    print(f"[SAFAR SARTHI ML] Successfully trained and saved model artifact to: {model_path}")

if __name__ == '__main__':
    train_and_save_volunteer_model()
