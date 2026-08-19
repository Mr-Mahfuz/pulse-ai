"""
Train the ML Triage Classifier on synthetic patient data.
Trains a Random Forest classifier and saves as .pkl file.
"""

import json
import os
import sys
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib

# Add parent to path so we can import ml_model
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from backend.ml_model import TriageClassifier, SYMPTOM_GROUPS


def extract_features(patient: dict) -> list:
    """Extract features from a patient dict — mirrors TriageClassifier._extract_features."""
    hr = patient.get("heart_rate", 80)
    sbp = patient.get("systolic_bp", 120)
    dbp = patient.get("diastolic_bp", 80)
    rr = patient.get("respiratory_rate", 16)
    temp = patient.get("temperature", 37.0)
    spo2 = patient.get("spo2", 98)
    gcs = patient.get("gcs_score", 15)
    age = patient.get("age", 30)
    
    # Core vitals (8)
    vitals = [hr, sbp, dbp, rr, temp, spo2, gcs, age]
    
    # Derived features (6)
    derived = [
        sbp - dbp,                           # pulse pressure
        (sbp + 2 * dbp) / 3,                 # mean arterial pressure
        1 if hr > 100 else 0,                # tachycardic
        1 if spo2 < 94 else 0,               # hypoxic
        1 if temp > 38.5 else 0,             # febrile
        1 if gcs < 15 else 0,                # altered consciousness
    ]
    
    # Symptom keyword features (10)
    combined = f"{patient.get('chief_complaint', '')} {patient.get('medical_history', '')}".lower()
    symptoms = []
    for group_name, keywords in SYMPTOM_GROUPS.items():
        found = 1 if any(kw in combined for kw in keywords) else 0
        symptoms.append(found)
    
    return vitals + derived + symptoms


def train_model():
    """Train the triage classifier and save it."""
    
    # Load synthetic data
    data_path = os.path.join(os.path.dirname(__file__), "synthetic_patients.json")
    if not os.path.exists(data_path):
        print("❌ No synthetic data found. Run generate_synthetic.py first!")
        return
    
    with open(data_path, "r") as f:
        patients = json.load(f)
    
    print(f"📊 Loaded {len(patients)} patients")
    
    # Extract features and labels
    X = np.array([extract_features(p) for p in patients])
    y = np.array([p["esi_label"] for p in patients])
    
    feature_names = TriageClassifier.get_feature_names()
    print(f"📐 Feature vector size: {len(feature_names)} features")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"🔀 Train: {len(X_train)}, Test: {len(X_test)}")
    
    # Train Random Forest
    rf_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = rf_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n{'='*50}")
    print(f"🎯 Random Forest Accuracy: {accuracy:.2%}")
    print(f"{'='*50}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=[f"ESI-{i}" for i in sorted(set(y))]))
    
    print("Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    
    # Cross-validation
    cv_scores = cross_val_score(rf_model, X, y, cv=5, scoring="accuracy")
    print(f"\n📈 5-Fold CV Accuracy: {cv_scores.mean():.2%} (±{cv_scores.std():.2%})")
    
    # Feature importance
    importances = rf_model.feature_importances_
    sorted_idx = np.argsort(importances)[::-1]
    print("\n🔍 Top 10 Most Important Features:")
    for i in range(min(10, len(feature_names))):
        idx = sorted_idx[i]
        print(f"  {i+1}. {feature_names[idx]}: {importances[idx]:.4f}")
    
    # Save model
    model_path = os.path.join(os.path.dirname(__file__), "triage_model.pkl")
    joblib.dump(rf_model, model_path)
    print(f"\n💾 Model saved to {model_path}")
    print(f"📦 Model classes: {rf_model.classes_}")
    
    return rf_model


if __name__ == "__main__":
    train_model()
