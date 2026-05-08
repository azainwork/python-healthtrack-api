from fastapi import FastAPI
from app.database import Base, engine

# Wajib import semua models di sini sebelum create_all!
from app.models import user, patient, doctor, appointment, medical_record

from app.routers import auth, patients, appointments, medical_records

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HealthTrack API",
    description="Patient Management & Medical Record API for clinics",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(medical_records.router)

@app.get("/", tags=["Health Check"])
def root():
    return {"status": "ok", "message": "HealthTrack API is running"}