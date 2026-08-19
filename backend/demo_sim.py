import time
import requests
import random
import json
from datetime import datetime

API_URL = "http://localhost:8000/api/patients/"

# A pool of synthetic diverse patient profiles for hackathon demo
DEMO_PATIENTS = [
    {
        "name": "Arif Rahman",
        "age": 55,
        "gender": "M",
        "chief_complaint": "Sudden onset of crushing chest pain radiating to left arm. Sweating profusely.",
        "heart_rate": 115,
        "systolic_bp": 165,
        "diastolic_bp": 95,
        "respiratory_rate": 24,
        "temperature": 37.1,
        "spo2": 93,
        "gcs_score": 15,
        "medical_history": "Hypertension, smoker"
    },
    {
        "name": "Tariq Hasan",
        "age": 28,
        "gender": "M",
        "chief_complaint": "Twisted ankle while playing football. Swollen and painful.",
        "heart_rate": 88,
        "systolic_bp": 120,
        "diastolic_bp": 80,
        "respiratory_rate": 16,
        "temperature": 36.8,
        "spo2": 99,
        "gcs_score": 15,
        "medical_history": "None"
    },
    {
        "name": "Sumaiya Islam",
        "age": 68,
        "gender": "F",
        "chief_complaint": "Right-sided weakness and slurred speech starting 30 minutes ago.",
        "heart_rate": 95,
        "systolic_bp": 180,
        "diastolic_bp": 100,
        "respiratory_rate": 18,
        "temperature": 37.0,
        "spo2": 96,
        "gcs_score": 13,
        "medical_history": "Type 2 Diabetes, Atrial Fibrillation"
    },
    {
        "name": "Kabir Hossain",
        "age": 42,
        "gender": "M",
        "chief_complaint": "Severe abdominal pain for 2 days. Vomiting and fever.",
        "heart_rate": 110,
        "systolic_bp": 105,
        "diastolic_bp": 65,
        "respiratory_rate": 20,
        "temperature": 39.2,
        "spo2": 97,
        "gcs_score": 15,
        "medical_history": "Previous appendectomy"
    },
    {
        "name": "Farhana Begum",
        "age": 35,
        "gender": "F",
        "chief_complaint": "Difficulty breathing, wheezing. Used inhaler 4 times with no relief.",
        "heart_rate": 125,
        "systolic_bp": 140,
        "diastolic_bp": 85,
        "respiratory_rate": 32,
        "temperature": 37.3,
        "spo2": 88,
        "gcs_score": 15,
        "medical_history": "Asthma"
    },
    {
        "name": "Nafis Iqbal",
        "age": 7,
        "gender": "M",
        "chief_complaint": "Fell off bicycle, large laceration on forehead. Bleeding controlled.",
        "heart_rate": 105,
        "systolic_bp": 110,
        "diastolic_bp": 70,
        "respiratory_rate": 22,
        "temperature": 37.0,
        "spo2": 99,
        "gcs_score": 15,
        "medical_history": "None"
    },
    {
        "name": "Ayesha Akter",
        "age": 22,
        "gender": "F",
        "chief_complaint": "Allergic reaction after eating peanuts. Swollen lips, hives.",
        "heart_rate": 118,
        "systolic_bp": 115,
        "diastolic_bp": 75,
        "respiratory_rate": 26,
        "temperature": 37.0,
        "spo2": 94,
        "gcs_score": 15,
        "medical_history": "Peanut allergy"
    },
    {
        "name": "Unknown Male",
        "age": 50,
        "gender": "M",
        "chief_complaint": "Found unresponsive on the street. Brought in by bystanders.",
        "heart_rate": 45,
        "systolic_bp": 70,
        "diastolic_bp": 40,
        "respiratory_rate": 8,
        "temperature": 35.5,
        "spo2": 82,
        "gcs_score": 6,
        "medical_history": "Unknown"
    }
]

def print_banner():
    print("""
    ==================================================
      SMART TRIAGE: LIVE CHAOS SIMULATION ENGINE
    ==================================================
    Injecting synthetic patients into the API queue...
    Press Ctrl+C to stop the simulation.
    """)

def run_simulation(interval_seconds=15):
    print_banner()
    
    # Shuffle the patients so the order is random
    random.shuffle(DEMO_PATIENTS)
    
    for i, patient in enumerate(DEMO_PATIENTS):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚨 Injecting patient: {patient['name']} (Age: {patient['age']})")
        print(f"    Complaint: {patient['chief_complaint']}")
        
        try:
            response = requests.post(API_URL, json=patient)
            if response.status_code == 200:
                print(f"    ✅ Successfully added to queue!")
            else:
                print(f"    ❌ API Error: {response.status_code}")
                print(f"    {response.text}")
        except requests.exceptions.ConnectionError:
            print(f"    ❌ Connection Error: Is the backend server running on port 8000?")
            break
            
        if i < len(DEMO_PATIENTS) - 1:
            print(f"    ⏳ Waiting {interval_seconds} seconds before next patient...\n")
            time.sleep(interval_seconds)
            
    print("\n🏁 Simulation complete. All patients injected.")

if __name__ == "__main__":
    run_simulation(interval_seconds=15)
