from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.patient import PatientCreate, PatientUpdate, PatientResponse
from app.services.patient import create_patient, get_patient, get_all_patients, update_patient
from app.core.dependecies import get_current_user

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/", response_model=PatientResponse, status_code=201)
def register_patient(
    payload: PatientCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_patient(db, payload)

@router.get("/", response_model=list[PatientResponse])
def list_patients(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_all_patients(db, skip, limit)

@router.get("/{patient_id}", response_model=PatientResponse)
def get_one_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_patient(db, patient_id)

@router.patch("/{patient_id}", response_model=PatientResponse)
def update_one_patient(
    patient_id: int,
    payload: PatientUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return update_patient(db, patient_id, payload)