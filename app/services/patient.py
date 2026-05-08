from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate

def create_patient(db: Session, payload: PatientCreate) -> Patient:
    existing = db.query(Patient).filter(Patient.nik == payload.nik).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="NIK already registered."
        )
    
    patient = Patient(**payload.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

def get_patient(db: Session, patient_id: int) -> Patient:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )
    return patient

def get_all_patients(db: Session, skip: int = 0, limit: int = 20) -> list[Patient]:
    return db.query(Patient).offset(skip).limit(limit).all()

def update_patient(db: Session, patient_id: int, payload: PatientUpdate) -> Patient:
    patient = get_patient(db, patient_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)
    return patient

