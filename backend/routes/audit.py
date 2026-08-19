"""
Audit Log API routes.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db, AuditLogDB
from backend.models import AuditLogResponse

router = APIRouter(prefix="/api/audit", tags=["audit"])


@router.get("/{patient_id}", response_model=List[AuditLogResponse])
def get_patient_audit_log(patient_id: str, db: Session = Depends(get_db)):
    """Get all audit log entries for a specific patient, newest first."""
    logs = (
        db.query(AuditLogDB)
        .filter(AuditLogDB.patient_id == patient_id)
        .order_by(AuditLogDB.timestamp.desc())
        .all()
    )
    return logs


@router.get("", response_model=List[AuditLogResponse])
def get_all_audit_logs(limit: int = 100, db: Session = Depends(get_db)):
    """Get all audit log entries, newest first."""
    logs = (
        db.query(AuditLogDB)
        .order_by(AuditLogDB.timestamp.desc())
        .limit(limit)
        .all()
    )
    return logs
