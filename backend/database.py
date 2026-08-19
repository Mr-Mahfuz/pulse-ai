import os
from sqlalchemy import create_engine, Column, String, Integer, Float, Text, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import uuid

DATABASE_URL = "sqlite:///./smarttriage.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class PatientDB(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    chief_complaint = Column(Text, nullable=False, default="")
    
    # Vitals
    heart_rate = Column(Integer)
    systolic_bp = Column(Integer)
    diastolic_bp = Column(Integer)
    respiratory_rate = Column(Integer)
    temperature = Column(Float)
    spo2 = Column(Integer)
    gcs_score = Column(Integer, default=15)
    
    medical_history = Column(Text, default="")
    arrival_time = Column(DateTime, default=datetime.utcnow)
    
    # Triage results
    triage_level = Column(Integer, nullable=True)
    triage_confidence = Column(Float, nullable=True)
    triage_rationale = Column(Text, nullable=True)
    triage_source = Column(String, nullable=True)
    triage_model_version = Column(String, nullable=True)
    triage_timestamp = Column(DateTime, nullable=True)
    triage_red_flags = Column(JSON, nullable=True)
    triage_probabilities = Column(JSON, nullable=True)
    
    # Clinician override
    clinician_override = Column(Integer, nullable=True)
    override_reason = Column(Text, nullable=True)
    
    status = Column(String, default="waiting")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    audit_logs = relationship("AuditLogDB", back_populates="patient", cascade="all, delete-orphan")


class AuditLogDB(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=generate_uuid)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    action = Column(String, nullable=False)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    actor = Column(String, default="system")
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("PatientDB", back_populates="audit_logs")


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
