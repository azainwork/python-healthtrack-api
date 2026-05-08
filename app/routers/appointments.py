from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from app.services.appointment import create_appointment, get_appointment, update_appointment, get_doctor_appointments
from app.core.dependecies import get_current_user, require_role

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("/", response_model=AppointmentResponse, status_code=201)
def book_appointment(
    payload: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_appointment(db, payload)

@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_one(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_appointment(db, appointment_id)

@router.patch("/{appointment_id}", response_model=AppointmentResponse)
def update_one(
    appointment_id: int,
    payload: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("doctor", "admin"))
):
    return update_appointment(db, appointment_id, payload)

@router.get("/doctor/{doctor_id}", response_model=list[AppointmentResponse])
def doctor_schedule(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_doctor_appointments(db, doctor_id)