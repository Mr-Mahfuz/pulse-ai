"""
Seed demo data — 10 curated patients for live demo scenarios.
Run this to populate the database with interesting test cases.
"""

import sys
import os
import json
import requests

API_URL = "http://localhost:8000"

DEMO_PATIENTS = [
    {
        "name": "Rahim Ahmed",
        "age": 58,
        "gender": "M",
        "chief_complaint": "Severe crushing chest pain radiating to left arm and jaw, shortness of breath, profuse sweating, nausea. Pain started 20 minutes ago while resting.",
        "heart_rate": 135,
        "systolic_bp": 85,
        "diastolic_bp": 50,
        "respiratory_rate": 28,
        "temperature": 37.2,
        "spo2": 87,
        "gcs_score": 15,
        "medical_history": "History of hypertension for 15 years, type 2 diabetes, smoking 20 pack-years. Father had MI at age 55."
    },
    {
        "name": "Fatima Khatun",
        "age": 72,
        "gender": "F",
        "chief_complaint": "Sudden onset left-sided weakness, facial droop on the right side, slurred speech. Family noticed symptoms 45 minutes ago. Unable to lift left arm.",
        "heart_rate": 92,
        "systolic_bp": 185,
        "diastolic_bp": 105,
        "respiratory_rate": 18,
        "temperature": 37.0,
        "spo2": 96,
        "gcs_score": 13,
        "medical_history": "Atrial fibrillation, hypertension, previous TIA 2 years ago. On warfarin."
    },
    {
        "name": "Karim Hassan",
        "age": 34,
        "gender": "M",
        "chief_complaint": "Severe difficulty breathing, wheezing, unable to speak in full sentences. Used rescue inhaler 4 times with no relief. Getting worse over the past hour.",
        "heart_rate": 118,
        "systolic_bp": 130,
        "diastolic_bp": 82,
        "respiratory_rate": 32,
        "temperature": 37.1,
        "spo2": 89,
        "gcs_score": 15,
        "medical_history": "Severe persistent asthma, multiple ER visits and one ICU admission. Allergic to aspirin."
    },
    {
        "name": "Ayesha Begum",
        "age": 45,
        "gender": "F",
        "chief_complaint": "Severe abdominal pain in the right lower quadrant, started 8 hours ago, now constant and worsening. Nausea, one episode of vomiting, low-grade fever.",
        "heart_rate": 102,
        "systolic_bp": 128,
        "diastolic_bp": 78,
        "respiratory_rate": 20,
        "temperature": 38.4,
        "spo2": 97,
        "gcs_score": 15,
        "medical_history": "No significant past medical history. No prior surgeries."
    },
    {
        "name": "Tanvir Islam",
        "age": 19,
        "gender": "M",
        "chief_complaint": "Twisted right ankle playing football 2 hours ago. Moderate swelling, can bear weight with pain. No numbness or tingling.",
        "heart_rate": 78,
        "systolic_bp": 122,
        "diastolic_bp": 76,
        "respiratory_rate": 16,
        "temperature": 36.8,
        "spo2": 99,
        "gcs_score": 15,
        "medical_history": "No medical history. No medications. No allergies."
    },
    {
        "name": "Nusrat Jahan",
        "age": 28,
        "gender": "F",
        "chief_complaint": "Sore throat and mild fever for 3 days. Runny nose, mild cough. No difficulty swallowing or breathing. Able to eat and drink.",
        "heart_rate": 82,
        "systolic_bp": 118,
        "diastolic_bp": 74,
        "respiratory_rate": 16,
        "temperature": 37.8,
        "spo2": 99,
        "gcs_score": 15,
        "medical_history": "Seasonal allergies. No chronic conditions."
    },
    {
        "name": "Md. Abdullah",
        "age": 65,
        "gender": "M",
        "chief_complaint": "Found confused by family, blood sugar reportedly very high on home monitor (reading 'HI'). Increased thirst and urination for 2 days. Becoming increasingly drowsy.",
        "heart_rate": 108,
        "systolic_bp": 100,
        "diastolic_bp": 62,
        "respiratory_rate": 26,
        "temperature": 37.4,
        "spo2": 95,
        "gcs_score": 12,
        "medical_history": "Type 2 diabetes for 20 years, non-compliant with insulin. Hypertension. Chronic kidney disease stage 3."
    },
    {
        "name": "Sabina Yasmin",
        "age": 55,
        "gender": "F",
        "chief_complaint": "Sudden severe headache, described as the worst headache of her life. Started 1 hour ago. Mild neck stiffness. No trauma. Photophobia.",
        "heart_rate": 95,
        "systolic_bp": 165,
        "diastolic_bp": 95,
        "respiratory_rate": 18,
        "temperature": 37.3,
        "spo2": 97,
        "gcs_score": 14,
        "medical_history": "Hypertension, managed with amlodipine. No previous headache history of this severity."
    },
    {
        "name": "Imran Ali",
        "age": 40,
        "gender": "M",
        "chief_complaint": "Severe allergic reaction after eating shrimp. Widespread hives, facial swelling, mild throat tightness. Took diphenhydramine at home with partial relief.",
        "heart_rate": 105,
        "systolic_bp": 115,
        "diastolic_bp": 70,
        "respiratory_rate": 22,
        "temperature": 37.0,
        "spo2": 95,
        "gcs_score": 15,
        "medical_history": "Known shellfish allergy. Carries EpiPen but did not use it. Previous mild allergic reactions."
    },
    {
        "name": "Rehana Parveen",
        "age": 32,
        "gender": "F",
        "chief_complaint": "Requesting prescription refill for blood pressure medication. Ran out 3 days ago. Feeling fine, no symptoms. No headache, no chest pain.",
        "heart_rate": 74,
        "systolic_bp": 132,
        "diastolic_bp": 84,
        "respiratory_rate": 15,
        "temperature": 36.6,
        "spo2": 99,
        "gcs_score": 15,
        "medical_history": "Hypertension diagnosed 2 years ago. On amlodipine 5mg daily. No other conditions."
    }
]


def seed_demo_data():
    """Seed the database with demo patients and run triage on each."""
    print("🌱 Seeding demo patients...")
    
    for i, patient in enumerate(DEMO_PATIENTS, 1):
        # Create patient
        resp = requests.post(f"{API_URL}/api/patients", json=patient)
        if resp.status_code != 201:
            print(f"  ❌ Failed to create patient {i}: {resp.text}")
            continue
        
        patient_data = resp.json()
        patient_id = patient_data["id"]
        print(f"  ✅ {i}. Created: {patient['name']} (ID: {patient_id[:8]}...)")
        
        # Run triage
        triage_resp = requests.post(f"{API_URL}/api/triage/{patient_id}")
        if triage_resp.status_code == 200:
            result = triage_resp.json()
            level = result.get("triage_level", "?")
            conf = result.get("triage_confidence", 0)
            source = result.get("triage_source", "?")
            print(f"     → ESI-{level} ({conf:.0%} confidence, {source})")
        else:
            print(f"     ❌ Triage failed: {triage_resp.text}")
    
    print("\n✅ Demo data seeded successfully!")


if __name__ == "__main__":
    seed_demo_data()
