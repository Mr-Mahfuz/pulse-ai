"""
Red-flag rules engine + triage orchestrator.
Combines three layers: deterministic rules → ML classifier → LLM explanation.
"""

from datetime import datetime
from typing import List, Dict, Optional
import re

from backend.models import ESI_LEVEL_NAMES


# ─── Layer 1: Deterministic Red-Flag Rules ───

RED_FLAG_KEYWORDS_ESI1 = [
    "unresponsive", "not breathing", "cardiac arrest", "pulseless",
    "apneic", "code blue", "active seizure", "seizure active",
    "no pulse", "agonal breathing"
]

RED_FLAG_KEYWORDS_ESI2 = [
    "chest pain", "crushing chest", "stroke", "facial droop",
    "slurred speech", "sudden weakness", "hematemesis",
    "suicidal", "overdose", "anaphylaxis", "severe allergic",
    "gunshot", "stab wound", "major trauma", "severe bleeding",
    "altered mental status", "confusion", "disoriented"
]


def check_red_flags(
    heart_rate: Optional[int],
    systolic_bp: Optional[int],
    diastolic_bp: Optional[int],
    respiratory_rate: Optional[int],
    temperature: Optional[float],
    spo2: Optional[int],
    gcs_score: Optional[int],
    chief_complaint: str,
    age: int,
    medical_history: str = ""
) -> dict:
    """
    Layer 1: Deterministic red-flag rules.
    Returns {triggered: bool, level: int, matched_rules: list}
    """
    matched_rules = []
    complaint_lower = chief_complaint.lower()
    history_lower = medical_history.lower()
    combined_text = f"{complaint_lower} {history_lower}"
    
    # Dynamic thresholds based on age (Age-Agnostic Vitals)
    is_pediatric = age < 12
    hr_critical_low = 60 if is_pediatric else 30
    hr_critical_high = 200 if is_pediatric else 180
    rr_critical_low = 15 if is_pediatric else 6
    rr_critical_high = 60 if is_pediatric else 40

    # Vitals-based ESI-1
    if heart_rate is not None and heart_rate < hr_critical_low:
        matched_rules.append(f"Severe bradycardia for age {age} (HR={heart_rate}, <{hr_critical_low})")
    if heart_rate is not None and heart_rate > hr_critical_high:
        matched_rules.append(f"Severe tachycardia for age {age} (HR={heart_rate}, >{hr_critical_high})")
    if spo2 is not None and spo2 < 85:
        matched_rules.append(f"Critical hypoxia (SpO2={spo2}%, <85%)")
    if respiratory_rate is not None and respiratory_rate > rr_critical_high:
        matched_rules.append(f"Severe tachypnea for age {age} (RR={respiratory_rate}, >{rr_critical_high})")
    if respiratory_rate is not None and respiratory_rate < rr_critical_low:
        matched_rules.append(f"Respiratory depression for age {age} (RR={respiratory_rate}, <{rr_critical_low})")
    if systolic_bp is not None and systolic_bp < 60:
        matched_rules.append(f"Severe hypotension / shock (SBP={systolic_bp}, <60 mmHg)")
    if gcs_score is not None and gcs_score <= 8:
        matched_rules.append(f"Severely altered consciousness (GCS={gcs_score}, ≤8)")
    
    # Keyword-based ESI-1
    for keyword in RED_FLAG_KEYWORDS_ESI1:
        if keyword in combined_text:
            matched_rules.append(f"Critical keyword detected: '{keyword}'")
    
    if matched_rules:
        return {
            "triggered": True,
            "level": 1,
            "matched_rules": matched_rules
        }
    
    # ── ESI-2 (Emergent) checks ──
    
    esi2_rules = []
    
    # Chest pain + risk factors
    if "chest pain" in complaint_lower:
        if age > 40:
            esi2_rules.append(f"Chest pain in patient age {age} (>40)")
        if heart_rate is not None and heart_rate > 100:
            esi2_rules.append(f"Chest pain with tachycardia (HR={heart_rate})")
        if spo2 is not None and spo2 < 94:
            esi2_rules.append(f"Chest pain with hypoxia (SpO2={spo2}%)")
    
    # Stroke symptoms
    stroke_keywords = ["sudden weakness", "slurred speech", "facial droop", "sudden numbness"]
    for kw in stroke_keywords:
        if kw in combined_text:
            esi2_rules.append(f"Possible stroke symptom: '{kw}'")
    
    # Severe hypotension (not critical but concerning)
    if systolic_bp is not None and systolic_bp < 80:
        esi2_rules.append(f"Hypotension (SBP={systolic_bp}, <80 mmHg)")
    
    # High fever + altered mental status
    if temperature is not None and temperature > 39.5:
        if gcs_score is not None and gcs_score < 14:
            esi2_rules.append(f"High fever ({temperature}°C) with altered consciousness (GCS={gcs_score})")
        else:
            esi2_rules.append(f"High-grade fever ({temperature}°C)")
    
    # Severe pain + hemodynamic instability
    if "severe pain" in complaint_lower:
        hr_warning = 150 if is_pediatric else 120
        if heart_rate is not None and heart_rate > hr_warning:
            esi2_rules.append(f"Severe pain with significant tachycardia for age {age} (HR={heart_rate})")
        if systolic_bp is not None and systolic_bp > 180:
            esi2_rules.append(f"Severe pain with hypertensive crisis (SBP={systolic_bp})")
    
    # SpO2 concerning range
    if spo2 is not None and 85 <= spo2 < 90:
        esi2_rules.append(f"Significant hypoxia (SpO2={spo2}%, 85-89%)")
    
    # GCS concerning
    if gcs_score is not None and 9 <= gcs_score <= 12:
        esi2_rules.append(f"Moderately altered consciousness (GCS={gcs_score})")
    
    # Keyword-based ESI-2
    for keyword in RED_FLAG_KEYWORDS_ESI2:
        if keyword in combined_text and keyword not in ["chest pain"]:  # avoid double-counting
            esi2_rules.append(f"Emergent keyword: '{keyword}'")
    
    if esi2_rules:
        return {
            "triggered": True,
            "level": 2,
            "matched_rules": esi2_rules
        }
    
    # No red flags triggered
    return {
        "triggered": False,
        "level": 0,
        "matched_rules": []
    }


# ─── Layer 2 + 3 Orchestration ───

async def compute_triage(
    patient_data: dict,
    ml_classifier,
    llm_explainer,
    language: str = "en"
) -> dict:
    """
    Full triage pipeline: red-flags → ML → LLM explanation.
    Returns complete triage result dict.
    """
    
    # Layer 1: Red-flag rules
    red_flag_result = check_red_flags(
        heart_rate=patient_data.get("heart_rate"),
        systolic_bp=patient_data.get("systolic_bp"),
        diastolic_bp=patient_data.get("diastolic_bp"),
        respiratory_rate=patient_data.get("respiratory_rate"),
        temperature=patient_data.get("temperature"),
        spo2=patient_data.get("spo2"),
        gcs_score=patient_data.get("gcs_score"),
        chief_complaint=patient_data.get("chief_complaint", ""),
        age=patient_data.get("age", 30),
        medical_history=patient_data.get("medical_history", "")
    )
    
    # Layer 2: ML classifier prediction
    ml_result = ml_classifier.predict(patient_data)
    
    # Determine final level
    if red_flag_result["triggered"]:
        final_level = red_flag_result["level"]
        source = "red_flag_override"
    else:
        final_level = ml_result["level"]
        source = "ml_classifier"
    
    level_name = ESI_LEVEL_NAMES.get(final_level, "Unknown")
    
    # Layer 3: LLM explanation
    if llm_explainer:
        rationale = await llm_explainer.generate_explanation(
            patient_data=patient_data,
            level=final_level,
            level_name=level_name,
            confidence=ml_result["confidence"],
            red_flags=red_flag_result["matched_rules"],
            ml_probabilities=ml_result["probabilities"],
            source=source,
            language=language
        )
    else:
        rationale = None
    
    return {
        "level": final_level,
        "level_name": level_name,
        "confidence": ml_result["confidence"],
        "rationale": rationale,
        "source": source,
        "model_version": ml_result["model_version"],
        "timestamp": datetime.utcnow(),
        "red_flags": red_flag_result["matched_rules"],
        "probabilities": ml_result["probabilities"]
    }
