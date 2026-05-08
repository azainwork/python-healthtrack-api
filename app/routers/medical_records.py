from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.medical_record import MedicalRecordCreate, MedicalRecordResponse
from app.services.medical_record import create_record, get_patient_records, get_record
from app.core.dependecies import get_current_user, require_role
from app.models.user import User

router = APIRouter(prefix="/medical-records", tags=["Medical Records"])

@router.post("/", response_model=MedicalRecordResponse, status_code=201)
def add_record(
    payload: MedicalRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("doctor", "admin"))
):
    return create_record(db, payload, created_by=current_user.id)

@router.get("/patient/{patient_id}", response_model=list[MedicalRecordResponse])
def patient_history(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_patient_records(db, patient_id)

@router.get("/{record_id}", response_model=MedicalRecordResponse)
def get_one(
    record_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_record(db, record_id)