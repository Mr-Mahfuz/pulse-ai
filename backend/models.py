from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


# ─── Patient Schemas ───

class PatientCreate(BaseModel):
    name: str
    age: int = Field(ge=0, le=150)
    gender: str
    chief_complaint: str = ""
    heart_rate: Optional[int] = Field(None, ge=0, le=300)
    systolic_bp: Optional[int] = Field(None, ge=0, le=350)
    diastolic_bp: Optional[int] = Field(None, ge=0, le=250)
    respiratory_rate: Optional[int] = Field(None, ge=0, le=80)
    temperature: Optional[float] = Field(None, ge=25.0, le=45.0)
    spo2: Optional[int] = Field(None, ge=0, le=100)
    gcs_score: Optional[int] = Field(15, ge=3, le=15)
    weight: Optional[float] = Field(None, ge=0.0, le=500.0)
    pain_scale: Optional[int] = Field(None, ge=0, le=10)
    medical_history: str = ""


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=150)
    gender: Optional[str] = None
    chief_complaint: Optional[str] = None
    heart_rate: Optional[int] = Field(None, ge=0, le=300)
    systolic_bp: Optional[int] = Field(None, ge=0, le=350)
    diastolic_bp: Optional[int] = Field(None, ge=0, le=250)
    respiratory_rate: Optional[int] = Field(None, ge=0, le=80)
    temperature: Optional[float] = Field(None, ge=25.0, le=45.0)
    spo2: Optional[int] = Field(None, ge=0, le=100)
    gcs_score: Optional[int] = Field(None, ge=3, le=15)
    weight: Optional[float] = Field(None, ge=0.0, le=500.0)
    pain_scale: Optional[int] = Field(None, ge=0, le=10)
    medical_history: Optional[str] = None
    status: Optional[str] = None


class PatientResponse(BaseModel):
    id: str
    name: str
    age: int
    gender: str
    chief_complaint: str
    heart_rate: Optional[int]
    systolic_bp: Optional[int]
    diastolic_bp: Optional[int]
    respiratory_rate: Optional[int]
    temperature: Optional[float]
    spo2: Optional[int]
    gcs_score: Optional[int]
    weight: Optional[float]
    pain_scale: Optional[int]
    medical_history: str
    arrival_time: Optional[datetime]
    triage_level: Optional[int]
    triage_confidence: Optional[float]
    triage_rationale: Optional[str]
    triage_source: Optional[str]
    triage_model_version: Optional[str]
    triage_timestamp: Optional[datetime]
    triage_red_flags: Optional[List[str]]
    triage_probabilities: Optional[Dict[str, float]]
    clinician_override: Optional[int]
    override_reason: Optional[str]
    status: str
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# ─── Triage Schemas ───

class TriageResult(BaseModel):
    patient_id: str
    level: int = Field(ge=1, le=5)
    level_name: str
    confidence: float = Field(ge=0.0, le=1.0)
    rationale: str
    source: str  # "red_flag_override" | "ml_classifier"
    model_version: str
    timestamp: datetime
    red_flags: List[str]
    probabilities: Dict[str, float]


class OverrideRequest(BaseModel):
    level: int = Field(ge=1, le=5)
    reason: str


# ─── Audit Log Schemas ───

class AuditLogResponse(BaseModel):
    id: str
    patient_id: str
    action: str
    old_value: Optional[dict]
    new_value: Optional[dict]
    actor: str
    timestamp: Optional[datetime]

    class Config:
        from_attributes = True


# ─── Utility ───

ESI_LEVEL_NAMES = {
    1: "Resuscitation",
    2: "Emergent",
    3: "Urgent",
    4: "Less Urgent",
    5: "Non-Urgent"
}

ESI_LEVEL_COLORS = {
    1: "#2563EB",  # Blue
    2: "#DC2626",  # Red
    3: "#F97316",  # Orange
    4: "#65A30D",  # Green
    5: "#4B5563",  # Grey
}
