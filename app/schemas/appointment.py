from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class AppointmentStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    scheduled_at: datetime
    complaint: Optional[str] = None

class AppointmentUpdate(BaseModel):
    status: Optional[AppointmentStatus] = None
    notes: Optional[str] = None
    scheduled_at: Optional[datetime] = None

class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    scheduled_at: datetime
    status: AppointmentStatus
    complaint: Optional[str]
    notes: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}