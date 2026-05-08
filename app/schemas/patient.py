from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class PatientCreate(BaseModel):
    full_name: str
    nik: str
    date_of_birth: date
    gender: str
    phone: Optional[str] = None
    address: Optional[str] = None
    blood_type: Optional[str] = None
    allergies: Optional[str] = None

class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    allergies: Optional[str] = None

class PatientResponse(BaseModel):
    id: int
    full_name: str
    nik: str
    date_of_birth: date
    gender: str
    phone: Optional[str]
    address: Optional[str]
    blood_type: Optional[str]
    allergies: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}