"""
Synthetic Patient Dataset Generator
Generates ~200 synthetic patients with realistic vitals, symptoms, and ESI labels.
"""

import json
import random
import os
from datetime import datetime, timedelta

random.seed(42)

# ─── ESI Level Templates ───

ESI_TEMPLATES = {
    1: {
        "complaints": [
            "Unresponsive, found on the floor, not breathing",
            "Cardiac arrest, bystander performing CPR",
            "Active seizure for the past 10 minutes, not stopping",
            "Severe difficulty breathing, turning blue, gasping for air",
            "Major trauma from vehicle accident, massive bleeding, unresponsive",
            "Found unconscious, no pulse detected by family",
            "Severe anaphylactic reaction, throat closing, unable to breathe",
            "Gunshot wound to chest, heavy bleeding, losing consciousness",
        ],
        "vitals_ranges": {
            "heart_rate": (20, 40, 170, 220),  # very low or very high
            "systolic_bp": (40, 70, None, None),
            "diastolic_bp": (20, 40, None, None),
            "respiratory_rate": (2, 8, 38, 50),
            "temperature": (35.0, 36.5, 39.5, 41.0),
            "spo2": (60, 84, None, None),
            "gcs_score": (3, 8, None, None),
        },
        "histories": [
            "History of cardiac disease, previous MI",
            "Known epileptic, non-compliant with medications",
            "No known medical history",
            "Previous anaphylaxis to penicillin",
            "COPD, end-stage, on home oxygen",
        ],
    },
    2: {
        "complaints": [
            "Severe chest pain radiating to left arm, shortness of breath, diaphoresis",
            "Sudden onset left-sided weakness, facial droop, slurred speech",
            "Severe abdominal pain with vomiting blood",
            "High fever with confusion and neck stiffness",
            "Diabetic patient found confused, blood sugar reportedly very high",
            "Severe allergic reaction with facial swelling and difficulty breathing",
            "Attempted overdose, ingested unknown quantity of pills 30 minutes ago",
            "Head injury after fall, brief loss of consciousness, now confused",
            "Severe asthma attack, unable to speak in full sentences",
            "Sudden severe headache, described as worst headache of life",
            "Chest pain, crushing sensation, nausea, shortness of breath",
            "Major laceration on forearm with significant bleeding, unable to stop",
        ],
        "vitals_ranges": {
            "heart_rate": (45, 60, 110, 150),
            "systolic_bp": (70, 95, 170, 210),
            "diastolic_bp": (40, 60, 100, 130),
            "respiratory_rate": (8, 12, 26, 36),
            "temperature": (36.0, 37.0, 39.0, 40.5),
            "spo2": (85, 92, None, None),
            "gcs_score": (9, 13, None, None),
        },
        "histories": [
            "History of hypertension, diabetes type 2, smoking 20 years",
            "Known asthmatic, multiple ER visits",
            "History of depression, previous suicide attempt",
            "Type 1 diabetic, insulin-dependent",
            "History of stroke, on blood thinners",
            "Known drug allergy to NSAIDs",
            "No significant past medical history",
            "History of peptic ulcer disease",
        ],
    },
    3: {
        "complaints": [
            "Abdominal pain, moderate severity, started 6 hours ago, nausea",
            "Difficulty breathing that has worsened over the past day",
            "High fever for 2 days with productive cough and body aches",
            "Moderate chest pain, dull and intermittent, no radiation",
            "Vomiting and diarrhea for 24 hours, feeling weak and dizzy",
            "Ankle injury from sports, significant swelling, unable to walk",
            "Worsening back pain with numbness in legs, started 2 days ago",
            "Urinary symptoms with flank pain, possible kidney stone",
            "Allergic reaction with widespread rash, mild breathing difficulty",
            "Persistent headache for 3 days, worse with movement, blurry vision",
            "Moderate asthma exacerbation, wheezing, using rescue inhaler frequently",
            "Deep cut on hand from kitchen knife, bleeding controlled with pressure",
        ],
        "vitals_ranges": {
            "heart_rate": (65, 80, 95, 115),
            "systolic_bp": (100, 120, 145, 165),
            "diastolic_bp": (60, 80, 90, 100),
            "respiratory_rate": (14, 18, 22, 28),
            "temperature": (36.8, 37.5, 38.0, 39.2),
            "spo2": (92, 95, None, None),
            "gcs_score": (14, 15, None, None),
        },
        "histories": [
            "History of asthma, well-controlled",
            "Previous kidney stones",
            "Hypertension, on medication",
            "No significant medical history",
            "History of migraines",
            "Type 2 diabetes, managed with metformin",
            "History of anxiety disorder",
        ],
    },
    4: {
        "complaints": [
            "Sore throat and mild fever for 2 days",
            "Twisted ankle while walking, mild swelling, can bear weight",
            "Earache and mild headache, started yesterday",
            "Mild abdominal discomfort after eating, no vomiting",
            "Small cut on finger, stopped bleeding, requesting stitches",
            "Mild rash on arms, itching for a few days",
            "Persistent cough for a week, no fever, no shortness of breath",
            "Lower back pain after lifting, mild, no numbness or weakness",
            "Eye redness and discharge for 2 days, mild discomfort",
            "Mild burn on hand from cooking, small area, no blistering",
            "Urinary burning and frequency for 2 days, no fever",
            "Knee pain after exercise, mild swelling, able to walk",
        ],
        "vitals_ranges": {
            "heart_rate": (65, 75, 85, 95),
            "systolic_bp": (110, 125, 135, 145),
            "diastolic_bp": (65, 78, 82, 90),
            "respiratory_rate": (14, 16, 18, 20),
            "temperature": (36.5, 37.0, 37.5, 38.3),
            "spo2": (96, 99, None, None),
            "gcs_score": (15, 15, None, None),
        },
        "histories": [
            "No significant medical history",
            "Seasonal allergies",
            "History of lower back strain",
            "No medications",
            "Takes over-the-counter allergy medication",
        ],
    },
    5: {
        "complaints": [
            "Requesting prescription refill, feeling fine",
            "Bug bite on leg, mild itching, no swelling",
            "Wants to get a mole checked, no changes noticed",
            "Cold symptoms for 5 days, runny nose, sneezing",
            "Mild headache, wants something stronger than OTC medication",
            "Ingrown toenail, mild discomfort",
            "Requesting clearance form for work",
            "Mild constipation for 3 days, no abdominal pain",
            "Small bruise on shin from bumping into furniture",
            "Dry skin and mild rash, wants cream recommendation",
        ],
        "vitals_ranges": {
            "heart_rate": (60, 72, 78, 88),
            "systolic_bp": (110, 120, 128, 135),
            "diastolic_bp": (65, 75, 80, 85),
            "respiratory_rate": (14, 16, 17, 18),
            "temperature": (36.4, 36.8, 37.1, 37.3),
            "spo2": (97, 99, None, None),
            "gcs_score": (15, 15, None, None),
        },
        "histories": [
            "No medical history",
            "No medications",
            "Healthy, no chronic conditions",
            "Takes daily multivitamin",
        ],
    },
}

NAMES_MALE = [
    "Rahim Ahmed", "Karim Hassan", "Tanvir Islam", "Fahim Rahman",
    "Shakil Hossain", "Nahid Akter", "Arif Khan", "Jabir Uddin",
    "Rafiq Miah", "Sohel Rana", "Md. Abdullah", "Tariq Hasan",
    "Imran Ali", "Nasir Uddin", "Farhan Iqbal", "Saiful Islam",
    "Rohan Das", "Amit Sharma", "Vikram Singh", "James Wilson",
    "Robert Chen", "David Kim", "Michael Park", "John Smith",
]

NAMES_FEMALE = [
    "Fatima Akhtar", "Nusrat Jahan", "Ayesha Begum", "Taslima Khatun",
    "Sabina Yasmin", "Rehana Parveen", "Marium Islam", "Salma Akter",
    "Nasreen Sultana", "Razia Begum", "Amina Khan", "Halima Khatun",
    "Priya Sharma", "Anjali Das", "Maria Garcia", "Sarah Johnson",
    "Emily Williams", "Jennifer Davis", "Lisa Anderson", "Rachel Brown",
]


def generate_vital(ranges: tuple) -> int | float:
    """Generate a vital sign from a range tuple (low_min, low_max, high_min, high_max)."""
    low_min, low_max, high_min, high_max = ranges
    
    if high_min is None:
        # Only low range (e.g., SpO2 for critical patients)
        return round(random.uniform(low_min, low_max))
    
    # Randomly pick low or normal-high range
    if random.random() < 0.5 and low_min != low_max:
        return round(random.uniform(low_min, low_max))
    else:
        return round(random.uniform(high_min, high_max))


def generate_patient(esi_level: int, patient_id: int) -> dict:
    """Generate a single synthetic patient for a given ESI level."""
    template = ESI_TEMPLATES[esi_level]
    
    gender = random.choice(["M", "F"])
    if gender == "M":
        name = random.choice(NAMES_MALE)
    else:
        name = random.choice(NAMES_FEMALE)
    
    # Age distribution varies by ESI level
    if esi_level <= 2:
        age = random.choice([
            random.randint(45, 85),  # Older patients more likely critical
            random.randint(20, 70),
        ])
    else:
        age = random.randint(18, 75)
    
    # Generate vitals
    vitals = {}
    for vital_name, ranges in template["vitals_ranges"].items():
        val = generate_vital(ranges)
        if vital_name == "temperature":
            vitals[vital_name] = round(random.uniform(ranges[0], ranges[1]) if random.random() < 0.5 else random.uniform(ranges[2] or ranges[0], ranges[3] or ranges[1]), 1)
        elif vital_name == "gcs_score":
            vitals[vital_name] = min(15, max(3, int(val)))
        else:
            vitals[vital_name] = int(val)
    
    # Ensure SpO2 is bounded
    vitals["spo2"] = min(100, max(0, vitals.get("spo2", 98)))
    
    arrival_offset = random.randint(0, 180)  # 0-180 minutes ago
    
    return {
        "name": name,
        "age": age,
        "gender": gender,
        "chief_complaint": random.choice(template["complaints"]),
        "heart_rate": vitals.get("heart_rate", 80),
        "systolic_bp": vitals.get("systolic_bp", 120),
        "diastolic_bp": vitals.get("diastolic_bp", 80),
        "respiratory_rate": vitals.get("respiratory_rate", 16),
        "temperature": vitals.get("temperature", 37.0),
        "spo2": vitals.get("spo2", 98),
        "gcs_score": vitals.get("gcs_score", 15),
        "medical_history": random.choice(template["histories"]),
        "esi_label": esi_level,  # Ground truth for training
    }


def generate_dataset(n: int = 200) -> list:
    """Generate a full synthetic dataset with specified ESI distribution."""
    # Distribution: ESI-1 (5%), ESI-2 (15%), ESI-3 (35%), ESI-4 (30%), ESI-5 (15%)
    distribution = {
        1: int(n * 0.05),
        2: int(n * 0.15),
        3: int(n * 0.35),
        4: int(n * 0.30),
        5: int(n * 0.15),
    }
    
    # Adjust for rounding
    total = sum(distribution.values())
    distribution[3] += n - total
    
    patients = []
    pid = 1
    for level, count in distribution.items():
        for _ in range(count):
            patient = generate_patient(level, pid)
            patients.append(patient)
            pid += 1
    
    random.shuffle(patients)
    return patients


if __name__ == "__main__":
    dataset = generate_dataset(250)
    
    output_path = os.path.join(os.path.dirname(__file__), "synthetic_patients.json")
    with open(output_path, "w") as f:
        json.dump(dataset, f, indent=2)
    
    # Print distribution
    from collections import Counter
    dist = Counter(p["esi_label"] for p in dataset)
    print(f"Generated {len(dataset)} synthetic patients:")
    for level in sorted(dist.keys()):
        print(f"  ESI-{level}: {dist[level]} patients")
    print(f"Saved to {output_path}")
