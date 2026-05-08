from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import timedelta
from app.models.appointment import Appointment, AppointmentStatus
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate

def check_conflict(db: Session, doctor_id: int, scheduled_at, exclude_id: int = None):
    windows_start = scheduled_at - timedelta(minutes=30)
    windows_end = scheduled_at + timedelta(minutes=30)

    query = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.scheduled_at >= windows_start,
        Appointment.scheduled_at <= windows_end,
        Appointment.status != AppointmentStatus.cancelled
    )

    if exclude_id:
        query = query.filter(Appointment.id != exclude_id)

    return query.first()

def create_appointment(db: Session, payload: AppointmentCreate) -> Appointment:
    conflict = check_conflict(db, payload.doctor_id, payload.scheduled_at)
    if conflict:
        raise HTTPException(
            status_code=409,
            detail=f"Doctor already has an appointment around that time (ID: {conflict.id})"
        )
    
    appointment = Appointment(**payload.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

def get_appointment(db: Session, appointment_id: int) -> Appointment:
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )
    return appointment

def update_appointment(db: Session, appointment_id: int, payload: AppointmentUpdate) -> Appointment:
    appointment = get_appointment(db, appointment_id)
    if payload.scheduled_at:
        conflict = check_conflict(db, appointment.doctor_id, payload.scheduled_at, exclude_id=appointment_id)
        if conflict:
            raise HTTPException(
                status_code=409,
                detail="Schedule conflict detected"
            )
    
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(appointment, field, value)

    db.commit()
    db.refresh(appointment)
    return appointment

def get_doctor_appointments(db: Session, doctor_id: int) -> list[Appointment]:
    return db.query(Appointment).filter(Appointment.doctor_id == doctor_id).all()