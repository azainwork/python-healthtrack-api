from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.medical_record import MedicalRecord
from app.schemas.medical_record import MedicalRecordCreate

def create_record(db: Session, payload: MedicalRecordCreate, created_by: int) -> MedicalRecord:
    record = MedicalRecord(**payload.model_dump(), created_by=created_by)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_patient_records(db: Session, patient_id: int) -> list[MedicalRecord]:
    return db.query(MedicalRecord).filter(MedicalRecord.patient_id == patient_id).all()

def get_record(db: Session, record_id: int) -> MedicalRecord:
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    return record