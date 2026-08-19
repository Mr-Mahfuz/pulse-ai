"""
ML Triage Classifier — Layer 2 of the triage pipeline.
Loads a pre-trained scikit-learn model and runs predictions on patient vitals.
"""

import os
import joblib
import numpy as np
from typing import Dict, Optional


# Symptom keyword groups for feature extraction
SYMPTOM_GROUPS = {
    "cardiac": ["chest pain", "palpitations", "heart", "cardiac", "angina", "crushing"],
    "respiratory": ["shortness of breath", "breathing", "dyspnea", "wheezing", "cough", "asthma", "sob"],
    "neurological": ["headache", "dizziness", "seizure", "confusion", "weakness", "numbness", "vision", "stroke", "faint"],
    "trauma": ["fall", "accident", "injury", "fracture", "broken", "wound", "cut", "bleeding", "trauma", "hit"],
    "gastrointestinal": ["abdominal pain", "nausea", "vomiting", "diarrhea", "stomach", "belly", "blood in stool"],
    "pain_severe": ["severe pain", "worst pain", "excruciating", "unbearable", "10/10"],
    "infection": ["fever", "chills", "infection", "swollen", "redness", "pus", "abscess"],
    "allergic": ["allergic", "rash", "hives", "swelling", "anaphylaxis", "itching"],
    "mental_health": ["suicidal", "anxiety", "panic", "depression", "overdose", "self-harm"],
    "urinary": ["urinary", "kidney", "flank pain", "burning urination", "blood in urine"],
}


class TriageClassifier:
    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.version = "smarttriage-rf-v1.0"
        
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), "data", "triage_model.pkl")
        
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
            print(f"✅ ML model loaded from {model_path}")
        else:
            print(f"⚠️ No model found at {model_path} — using rule-based fallback")
    
    def _extract_symptom_features(self, chief_complaint: str, medical_history: str = "") -> list:
        """Extract binary symptom group indicators from text."""
        combined = f"{chief_complaint} {medical_history}".lower()
        features = []
        for group_name, keywords in SYMPTOM_GROUPS.items():
            found = 1 if any(kw in combined for kw in keywords) else 0
            features.append(found)
        return features
    
    def _extract_features(self, patient_data: dict) -> np.ndarray:
        """Convert patient data to feature vector for the model."""
        
        hr = patient_data.get("heart_rate") or 80
        sbp = patient_data.get("systolic_bp") or 120
        dbp = patient_data.get("diastolic_bp") or 80
        rr = patient_data.get("respiratory_rate") or 16
        temp = patient_data.get("temperature") or 37.0
        spo2 = patient_data.get("spo2") or 98
        gcs = patient_data.get("gcs_score") or 15
        age = patient_data.get("age") or 30
        
        # Core vitals (8 features)
        vitals = [hr, sbp, dbp, rr, temp, spo2, gcs, age]
        
        # Derived features (6 features)
        derived = [
            sbp - dbp,                           # pulse pressure
            (sbp + 2 * dbp) / 3,                 # mean arterial pressure
            1 if hr > 100 else 0,                # tachycardic
            1 if spo2 < 94 else 0,               # hypoxic
            1 if temp > 38.5 else 0,             # febrile
            1 if gcs < 15 else 0,                # altered consciousness
        ]
        
        # Symptom keyword features (10 features)
        symptoms = self._extract_symptom_features(
            patient_data.get("chief_complaint", ""),
            patient_data.get("medical_history", "")
        )
        
        return np.array(vitals + derived + symptoms, dtype=np.float64)
    
    def predict(self, patient_data: dict) -> Dict:
        """
        Predict triage level for a patient.
        Returns: {level, confidence, probabilities, model_version}
        """
        features = self._extract_features(patient_data)
        
        if self.model is not None:
            prediction = int(self.model.predict([features])[0])
            probabilities = self.model.predict_proba([features])[0]
            confidence = float(max(probabilities))
            
            prob_dict = {}
            for i, p in enumerate(probabilities):
                prob_dict[f"ESI-{self.model.classes_[i]}"] = round(float(p), 4)
        else:
            # Fallback: rule-based estimation when no model available
            prediction, confidence, prob_dict = self._fallback_predict(patient_data, features)
        
        return {
            "level": prediction,
            "confidence": confidence,
            "probabilities": prob_dict,
            "model_version": self.version
        }
    
    def _fallback_predict(self, patient_data: dict, features: np.ndarray):
        """Simple rule-based fallback when no trained model is available."""
        hr = patient_data.get("heart_rate") or 80
        sbp = patient_data.get("systolic_bp") or 120
        spo2 = patient_data.get("spo2") or 98
        gcs = patient_data.get("gcs_score") or 15
        temp = patient_data.get("temperature") or 37.0
        rr = patient_data.get("respiratory_rate") or 16
        age = patient_data.get("age") or 30
        
        is_pediatric = age < 12
        hr_high = 160 if is_pediatric else 120
        hr_low = 60 if is_pediatric else 50
        hr_warn_high = 130 if is_pediatric else 100
        hr_warn_low = 70 if is_pediatric else 60
        rr_high = 40 if is_pediatric else 24
        rr_low = 15 if is_pediatric else 10
        
        score = 0
        if hr > hr_high or hr < hr_low: score += 3
        elif hr > hr_warn_high or hr < hr_warn_low: score += 1
        if sbp < 90: score += 3
        elif sbp < 100 or sbp > 180: score += 2
        if spo2 < 90: score += 3
        elif spo2 < 94: score += 2
        if gcs < 12: score += 3
        elif gcs < 15: score += 1
        if temp > 39: score += 2
        elif temp > 38: score += 1
        if rr > rr_high or rr < rr_low: score += 2
        
        if score >= 8: level = 1
        elif score >= 5: level = 2
        elif score >= 3: level = 3
        elif score >= 1: level = 4
        else: level = 5
        
        confidence = min(0.5 + score * 0.05, 0.95)
        probs = {f"ESI-{i}": 0.05 for i in range(1, 6)}
        probs[f"ESI-{level}"] = confidence
        remaining = 1.0 - confidence
        for k in probs:
            if k != f"ESI-{level}":
                probs[k] = round(remaining / 4, 4)
        
        return level, confidence, probs
    
    @staticmethod
    def get_feature_names():
        """Return feature names for model interpretability."""
        vitals = ["heart_rate", "systolic_bp", "diastolic_bp", "respiratory_rate",
                  "temperature", "spo2", "gcs_score", "age"]
        derived = ["pulse_pressure", "map", "is_tachycardic", "is_hypoxic",
                   "is_febrile", "is_altered_consciousness"]
        symptoms = [f"symptom_{name}" for name in SYMPTOM_GROUPS.keys()]
        return vitals + derived + symptoms
