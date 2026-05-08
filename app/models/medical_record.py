from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from app.database import Base

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=True)
    diagnosis = Column(Text, nullable=False)
    prescription = Column(Text)
    notes = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)  # audit trail
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient")
    doctor = relationship("Doctor")
    creator = relationship("User")