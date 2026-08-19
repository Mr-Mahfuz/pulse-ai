# Phase 2 — Triage Engine & AI Pipeline

> **Goal:** Build the core intelligence — red-flag rules, ML classifier integration, and LLM explanation layer. This is the heart of the project and where we score on "AI Implementation & Technical Excellence" (20 marks).
> **Time Budget:** ~90 minutes (of 5 hours)

---

## Pre-Hackathon Prep (During 3-Day Window)

These can be prepared ahead of time per the rules ("pre-trained AI models encouraged", "open-source libraries encouraged"):

- [x] Synthetic patient dataset generated and validated
- [x] ML model trained on synthetic data and saved as `.pkl`
- [x] Red-flag rule set researched and documented
- [x] Gemini API key obtained and tested
- [x] Prompt templates for LLM explanation layer drafted

---

## Tasks (Ordered)

### 2.1 — Red-Flag Rules Engine (Deterministic Layer)

The first layer is a hardcoded rule set that catches life-threatening conditions regardless of what the ML model says. This is both clinically responsible and impressive to judges.

**Rules (ESI Level 1 — Immediate/Resuscitation):**
| Condition | Rule |
|---|---|
| Cardiac arrest indicators | HR < 30 OR HR > 180 |
| Respiratory failure | SpO2 < 85% OR RR > 35 |
| Severe hypotension (shock) | Systolic BP < 70 |
| Unconscious / unresponsive | GCS ≤ 8 |
| Keyword triggers | chief_complaint contains: "unresponsive", "not breathing", "cardiac arrest", "seizure active" |

**Rules (ESI Level 2 — Emergent, auto-escalate):**
| Condition | Rule |
|---|---|
| Chest pain + risk factors | "chest pain" in complaint AND (age > 40 OR HR > 100) |
| Stroke symptoms | complaint contains: "sudden weakness", "slurred speech", "facial droop" |
| Severe pain + abnormal vitals | "severe pain" AND (HR > 110 OR BP systolic > 180) |
| High fever + altered mental | temp > 39.5°C AND GCS < 14 |

**Implementation:** Pure Python functions, no ML needed. Returns `{ triggered: bool, level: int, matched_rules: string[] }`.

### 2.2 — ML Risk Classifier Integration

Load the pre-trained model and run predictions:

```python
# ml_model.py
import joblib
import numpy as np

class TriageClassifier:
    def __init__(self):
        self.model = joblib.load("data/triage_model.pkl")
        self.version = "smarttriage-rf-v1.0"
    
    def predict(self, vitals: dict) -> dict:
        features = self._extract_features(vitals)
        prediction = self.model.predict([features])[0]
        probabilities = self.model.predict_proba([features])[0]
        confidence = float(max(probabilities))
        
        return {
            "level": int(prediction),
            "confidence": confidence,
            "probabilities": {f"ESI-{i+1}": float(p) for i, p in enumerate(probabilities)},
            "model_version": self.version
        }
    
    def _extract_features(self, vitals):
        # Numeric vitals + derived features
        return [
            vitals["heart_rate"],
            vitals["systolic_bp"],
            vitals["diastolic_bp"],
            vitals["respiratory_rate"],
            vitals["temperature"],
            vitals["spo2"],
            vitals["gcs_score"],
            vitals["age"],
            # Derived
            vitals["systolic_bp"] - vitals["diastolic_bp"],  # pulse pressure
            1 if vitals["heart_rate"] > 100 else 0,           # tachycardic
            1 if vitals["spo2"] < 94 else 0,                  # hypoxic
            1 if vitals["temperature"] > 38.5 else 0,         # febrile
            # Symptom keyword indicators (from chief_complaint)
            ...keyword_features
        ]
```

### 2.3 — LLM Explanation Layer (Gemini API)

The LLM **explains** the triage decision — it does NOT make it. This is the key architectural principle.

```python
# Prompt template
EXPLANATION_PROMPT = """
You are a clinical decision-support assistant. A triage AI system has assessed 
a patient and assigned them a priority level. Your job is to explain WHY in 
plain language that a clinician would find useful.

PATIENT DATA:
- Age: {age}, Gender: {gender}
- Chief Complaint: {chief_complaint}
- Vitals: HR {hr}, BP {sbp}/{dbp}, RR {rr}, Temp {temp}°C, SpO2 {spo2}%, GCS {gcs}
- Medical History: {medical_history}

AI TRIAGE RESULT:
- Assigned Level: ESI-{level} ({level_name})
- Confidence: {confidence:.0%}
- Red-flag rules triggered: {triggered_rules}

Generate a 2-3 sentence clinical rationale explaining this priority assignment.
Focus on which specific findings drove the decision. Be concise and professional.
"""
```

**Key design:** 
- Call is async (non-blocking)
- Falls back to a template-based explanation if the API call fails or times out
- Response is cached per triage computation (no re-calling for the same data)

### 2.4 — Triage Engine Orchestrator

Combines all three layers:

```python
async def compute_triage(patient: Patient) -> TriageResult:
    # Layer 1: Red flags (instant, deterministic)
    red_flag_result = check_red_flags(patient)
    
    # Layer 2: ML prediction
    ml_result = classifier.predict(patient.to_vitals_dict())
    
    # Combine: red flags override ML if triggered
    if red_flag_result.triggered:
        final_level = red_flag_result.level
        source = "red_flag_override"
    else:
        final_level = ml_result["level"]
        source = "ml_classifier"
    
    # Layer 3: LLM explanation (async, non-blocking)
    rationale = await generate_explanation(
        patient, final_level, ml_result, red_flag_result
    )
    
    result = TriageResult(
        level=final_level,
        confidence=ml_result["confidence"],
        rationale=rationale,
        source=source,
        model_version=ml_result["model_version"],
        timestamp=datetime.utcnow(),
        red_flags=red_flag_result.matched_rules,
        ml_probabilities=ml_result["probabilities"]
    )
    
    # Write to audit log
    log_triage_decision(patient.id, result)
    
    return result
```

### 2.5 — Triage API Endpoints

```
POST /api/triage/{patient_id}     → Run triage on a patient
POST /api/triage/batch            → Run triage on all un-triaged patients
PUT  /api/triage/{patient_id}/override  → Clinician overrides AI decision
GET  /api/triage/{patient_id}/history   → Get triage history for patient
```

### 2.6 — Verify Phase 2

- [ ] Red-flag rules correctly catch critical cases (test with edge cases)
- [ ] ML model returns level + confidence for any valid input
- [ ] LLM explanation generates readable rationale in <3 seconds
- [ ] Fallback explanation works when LLM is unavailable
- [ ] Changing vitals via PUT → re-triage → produces updated result
- [ ] Audit log captures every triage computation

---

## 🔴 USER ACTION REQUIRED

1. **Gemini API Key** — must be set in `backend/.env` as `GEMINI_API_KEY=your_key_here`
   - Get it free at [Google AI Studio](https://aistudio.google.com/apikey)
   - Confirm when done so I can test the LLM layer
