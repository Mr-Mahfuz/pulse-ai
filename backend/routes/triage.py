"""
Triage API routes — run triage, batch triage, clinician override.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from pydantic import BaseModel
from backend.database import get_db, PatientDB, AuditLogDB, generate_uuid
from backend.models import TriageResult, OverrideRequest, PatientResponse, ESI_LEVEL_NAMES
from backend.triage_engine import compute_triage

router = APIRouter(prefix="/api/triage", tags=["triage"])

class TranslateRequest(BaseModel):
    language: str

# These will be set by main.py on startup
ml_classifier = None
llm_explainer = None


def set_dependencies(classifier, explainer):
    global ml_classifier, llm_explainer
    ml_classifier = classifier
    llm_explainer = explainer


@router.post("/batch", response_model=List[PatientResponse])
async def batch_triage(db: Session = Depends(get_db)):
    """Run triage on all patients that haven't been triaged yet."""
    untriaged = db.query(PatientDB).filter(PatientDB.triage_level == None).all()
    
    results = []
    for patient in untriaged:
        patient_data = {
            "name": patient.name,
            "age": patient.age,
            "gender": patient.gender,
            "chief_complaint": patient.chief_complaint,
            "heart_rate": patient.heart_rate,
            "systolic_bp": patient.systolic_bp,
            "diastolic_bp": patient.diastolic_bp,
            "respiratory_rate": patient.respiratory_rate,
            "temperature": patient.temperature,
            "spo2": patient.spo2,
            "gcs_score": patient.gcs_score,
            "medical_history": patient.medical_history,
        }
        
        result = await compute_triage(patient_data, ml_classifier, llm_explainer)
        
        patient.triage_level = result["level"]
        patient.triage_confidence = result["confidence"]
        patient.triage_rationale = result["rationale"]
        patient.triage_source = result["source"]
        patient.triage_model_version = result["model_version"]
        patient.triage_timestamp = result["timestamp"]
        patient.triage_red_flags = result["red_flags"]
        patient.triage_probabilities = result["probabilities"]
        
        audit = AuditLogDB(
            id=generate_uuid(),
            patient_id=patient.id,
            action="triage_computed",
            old_value=None,
            new_value={
                "level": result["level"],
                "confidence": round(result["confidence"], 4),
                "source": result["source"],
            },
            actor="system",
            timestamp=datetime.utcnow()
        )
        db.add(audit)
        results.append(patient)
    
    db.commit()
    for p in results:
        db.refresh(p)
    
    return results


@router.post("/{patient_id}", response_model=PatientResponse)
async def run_triage(patient_id: str, language: str = "en", db: Session = Depends(get_db)):
    """Run the full triage pipeline on a patient."""
    patient = db.query(PatientDB).filter(PatientDB.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    if ml_classifier is None:
        raise HTTPException(status_code=503, detail="ML classifier not initialized")
    
    # Build patient data dict
    patient_data = {
        "name": patient.name,
        "age": patient.age,
        "gender": patient.gender,
        "chief_complaint": patient.chief_complaint,
        "heart_rate": patient.heart_rate,
        "systolic_bp": patient.systolic_bp,
        "diastolic_bp": patient.diastolic_bp,
        "respiratory_rate": patient.respiratory_rate,
        "temperature": patient.temperature,
        "spo2": patient.spo2,
        "gcs_score": patient.gcs_score,
        "medical_history": patient.medical_history,
    }
    
    # Store old triage values for audit
    old_triage = {
        "level": patient.triage_level,
        "confidence": patient.triage_confidence,
        "source": patient.triage_source,
    }
    
    # Run triage pipeline
    result = await compute_triage(patient_data, ml_classifier, llm_explainer, language)
    
    # Update patient record
    patient.triage_level = result["level"]
    patient.triage_confidence = result["confidence"]
    patient.triage_rationale = result["rationale"]
    patient.triage_source = result["source"]
    patient.triage_model_version = result["model_version"]
    patient.triage_timestamp = result["timestamp"]
    patient.triage_red_flags = result["red_flags"]
    patient.triage_probabilities = result["probabilities"]
    
    # Audit log
    audit = AuditLogDB(
        id=generate_uuid(),
        patient_id=patient_id,
        action="triage_computed",
        old_value=old_triage,
        new_value={
            "level": result["level"],
            "level_name": result["level_name"],
            "confidence": round(result["confidence"], 4),
            "source": result["source"],
            "red_flags": result["red_flags"],
            "model_version": result["model_version"],
        },
        actor="system",
        timestamp=datetime.utcnow()
    )
    db.add(audit)
    db.commit()
    db.refresh(patient)
    
    return patient


@router.put("/{patient_id}/override", response_model=PatientResponse)
def override_triage(patient_id: str, override: OverrideRequest, db: Session = Depends(get_db)):
    """Clinician overrides the AI triage decision."""
    patient = db.query(PatientDB).filter(PatientDB.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    old_values = {
        "triage_level": patient.triage_level,
        "clinician_override": patient.clinician_override,
    }
    
    patient.clinician_override = override.level
    patient.override_reason = override.reason
    
    audit = AuditLogDB(
        id=generate_uuid(),
        patient_id=patient_id,
        action="clinician_override",
        old_value=old_values,
        new_value={
            "clinician_override": override.level,
            "override_level_name": ESI_LEVEL_NAMES.get(override.level, "Unknown"),
            "reason": override.reason,
        },
        actor="clinician",
        timestamp=datetime.utcnow()
    )
    db.add(audit)
    db.commit()
    db.refresh(patient)
    
    return patient


@router.post("/{patient_id}/translate")
async def translate_rationale(patient_id: str, req: TranslateRequest, db: Session = Depends(get_db)):
    """Translate the triage rationale to a specific language without re-running triage."""
    patient = db.query(PatientDB).filter(PatientDB.id == patient_id).first()
    if not patient or not patient.triage_rationale:
        raise HTTPException(status_code=404, detail="Patient or rationale not found")
        
    target_lang = "English" if req.language == "en" else "Bengali"
    
    # Fast path for English
    if req.language == "en":
        return {"rationale": patient.triage_rationale}
        
    import os
    import asyncio
    try:
        from google import genai
    except ImportError:
        genai = None

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_keys = os.getenv("GEMINI_API_KEYS")
        if api_keys:
            api_key = api_keys.split(',')[0].strip()
            
    if api_key and genai:
        client = genai.Client(api_key=api_key)
        prompt = f"Translate the following medical triage rationale to {target_lang}. Respond ONLY with the translation, no extra text. Do not use markdown.\n\nRationale:\n{patient.triage_rationale}"
        
        try:
            response = await asyncio.to_thread(
                client.models.generate_content,
                model="gemini-2.5-flash",
                contents=prompt
            )
            patient.triage_rationale = response.text.strip()
            db.commit()
            db.refresh(patient)
            return {"rationale": patient.triage_rationale}
        except Exception as e:
            print(f"Translation API failed: {e}")
            # Fall through to fallback
            
    # Fallback to hardcoded translation
    if req.language == "bn":
        patient.triage_rationale = "রেড ফ্ল্যাগ নিয়মের কারণে অথবা এআই মডেলটির মূল্যায়নের ভিত্তিতে রোগীকে এই অগ্রাধিকার স্তর দেওয়া হয়েছে। অবিলম্বে মনোযোগ বা আরও মূল্যায়নের প্রয়োজন হতে পারে।"
        db.commit()
        db.refresh(patient)
        return {"rationale": patient.triage_rationale}
    
    raise HTTPException(status_code=500, detail="Translation failed and no fallback available.")
