from sqlalchemy import Column, Integer, String, Date, Text, DateTime, func
from app.database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    nik = Column(String(16), unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(10), nullable=False)
    phone = Column(String(20))
    address = Column(Text)
    blood_type = Column(String(5))
    allergies = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default = func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())