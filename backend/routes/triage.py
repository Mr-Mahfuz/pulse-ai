"""
Triage API routes — run triage, batch triage, clinician override.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from backend.database import get_db, PatientDB, AuditLogDB, generate_uuid
from backend.models import TriageResult, OverrideRequest, PatientResponse, ESI_LEVEL_NAMES
from backend.triage_engine import compute_triage

router = APIRouter(prefix="/api/triage", tags=["triage"])

# These will be set by main.py on startup
ml_classifier = None
llm_explainer = None


def set_dependencies(classifier, explainer):
    global ml_classifier, llm_explainer
    ml_classifier = classifier
    llm_explainer = explainer


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
