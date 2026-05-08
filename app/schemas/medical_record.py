from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MedicalRecordCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_id: Optional[int] = None
    diagnosis: str
    prescription: Optional[str] = None
    notes: Optional[str] = None

class MedicalRecordResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_id: Optional[int]
    diagnosis: str
    prescription: Optional[str]
    notes: Optional[str]
    created_by: int
    created_at: datetime

    model_config = {"from_attributes": True}