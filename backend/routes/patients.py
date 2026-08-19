"""
Patient CRUD API routes.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from backend.database import get_db, PatientDB, AuditLogDB, generate_uuid
from backend.models import PatientCreate, PatientUpdate, PatientResponse

router = APIRouter(prefix="/api/patients", tags=["patients"])


@router.post("", response_model=PatientResponse, status_code=201)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    """Create a new patient record."""
    db_patient = PatientDB(
        id=generate_uuid(),
        name=patient.name,
        age=patient.age,
        gender=patient.gender,
        chief_complaint=patient.chief_complaint,
        heart_rate=patient.heart_rate,
        systolic_bp=patient.systolic_bp,
        diastolic_bp=patient.diastolic_bp,
        respiratory_rate=patient.respiratory_rate,
        temperature=patient.temperature,
        spo2=patient.spo2,
        gcs_score=patient.gcs_score,
        medical_history=patient.medical_history,
        arrival_time=datetime.utcnow(),
        status="waiting",
        created_at=datetime.utcnow()
    )
    db.add(db_patient)
    
    # Audit log
    audit = AuditLogDB(
        id=generate_uuid(),
        patient_id=db_patient.id,
        action="patient_registered",
        new_value={"name": patient.name, "chief_complaint": patient.chief_complaint},
        actor="system",
        timestamp=datetime.utcnow()
    )
    db.add(audit)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@router.get("", response_model=List[PatientResponse])
def list_patients(
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all patients, sorted by triage priority (ESI-1 first), then arrival time."""
    query = db.query(PatientDB)
    
    if status:
        query = query.filter(PatientDB.status == status)
    
    # Sort: clinician_override first (if exists), then triage_level, then arrival_time
    patients = query.all()
    
    def sort_key(p):
        effective_level = p.clinician_override if p.clinician_override else (p.triage_level or 99)
        arrival = p.arrival_time or datetime.min
        return (effective_level, arrival)
    
    patients.sort(key=sort_key)
    return patients


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    """Get a single patient by ID."""
    patient = db.query(PatientDB).filter(PatientDB.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: str, update: PatientUpdate, db: Session = Depends(get_db)):
    """Update a patient's information (e.g., change vitals)."""
    patient = db.query(PatientDB).filter(PatientDB.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    old_values = {}
    new_values = {}
    
    update_data = update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        old_val = getattr(patient, field, None)
        if old_val != value:
            old_values[field] = old_val
            new_values[field] = value
        setattr(patient, field, value)
    
    # Audit log for changes
    if new_values:
        audit = AuditLogDB(
            id=generate_uuid(),
            patient_id=patient_id,
            action="patient_updated",
            old_value=old_values,
            new_value=new_values,
            actor="clinician",
            timestamp=datetime.utcnow()
        )
        db.add(audit)
    
    db.commit()
    db.refresh(patient)
    return patient


@router.delete("/{patient_id}", status_code=204)
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    """Delete a patient record."""
    patient = db.query(PatientDB).filter(PatientDB.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(patient)
    db.commit()


@router.patch("/{patient_id}/status")
def update_status(patient_id: str, status: str, db: Session = Depends(get_db)):
    """Update patient status (waiting / in-treatment / discharged)."""
    valid_statuses = ["waiting", "in-treatment", "discharged"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Status must be one of: {valid_statuses}")
    
    patient = db.query(PatientDB).filter(PatientDB.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    old_status = patient.status
    patient.status = status
    
    audit = AuditLogDB(
        id=generate_uuid(),
        patient_id=patient_id,
        action="status_changed",
        old_value={"status": old_status},
        new_value={"status": status},
        actor="clinician",
        timestamp=datetime.utcnow()
    )
    db.add(audit)
    db.commit()
    
    return {"message": f"Status updated to {status}"}
