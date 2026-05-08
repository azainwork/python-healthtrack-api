# HealthTrack API 🏥

A production-ready REST API for patient management and medical records, built for small clinics and independent healthcare providers. Designed with security and data integrity as first-class concerns.

## Tech Stack

- **Runtime**: Python 3.11
- **Framework**: FastAPI
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Auth**: JWT (python-jose) + bcrypt
- **Containerization**: Docker + Docker Compose
- **Docs**: Auto-generated OpenAPI / Swagger UI

---

## Features

- **Role-Based Access Control (RBAC)** — Admin, Doctor, Nurse with enforced permission scopes
- **Patient Registration & Management** — Full CRUD with NIK validation
- **Appointment Scheduling** — With conflict detection (30-minute window per doctor)
- **Medical Records** — Doctor-only write access with full audit trail (`created_by`)
- **JWT Authentication** — Stateless, per-request token validation
- **Dockerized** — One command to run the entire stack

---

## Entity Relationship Diagram

```
users
  id, full_name, email, hashed_password, role (admin|doctor|nurse), created_at

doctors
  id, user_id (FK → users), specialization, license_number, created_at

patients
  id, full_name, nik (unique), date_of_birth, gender, phone, address, blood_type, allergies, created_at

appointments
  id, patient_id (FK → patients), doctor_id (FK → doctors),
  scheduled_at, status (pending|confirmed|completed|cancelled),
  complaint, notes, created_at, updated_at

medical_records
  id, patient_id (FK → patients), doctor_id (FK → doctors),
  appointment_id (FK → appointments, nullable),
  diagnosis, prescription, notes,
  created_by (FK → users),  ← audit trail
  created_at
```

---

## Getting Started

### Prerequisites
- Docker
- Docker Compose

### Run

```bash
git clone https://github.com/devzainn/healthtrack-api.git
cd healthtrack-api
cp .env.example .env
docker compose up --build
```

API will be available at: `http://localhost:8000`  
Swagger UI: `http://localhost:8000/docs`

---

## API Endpoints

### Auth
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/auth/register` | Register new user | Public |
| POST | `/auth/login` | Login, get JWT token | Public |

### Doctors
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/doctors/` | Register doctor profile | Admin only |

### Patients
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/patients/` | Register new patient | All roles |
| GET | `/patients/` | List all patients (paginated) | All roles |
| GET | `/patients/{id}` | Get patient detail | All roles |
| PATCH | `/patients/{id}` | Update patient info | All roles |

### Appointments
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/appointments/` | Book appointment | All roles |
| GET | `/appointments/{id}` | Get appointment detail | All roles |
| PATCH | `/appointments/{id}` | Update status / notes | Doctor, Admin |
| GET | `/appointments/doctor/{id}` | Get doctor's schedule | All roles |

### Medical Records
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/medical-records/` | Create medical record | Doctor, Admin |
| GET | `/medical-records/patient/{id}` | Patient's medical history | All roles |
| GET | `/medical-records/{id}` | Get record detail | All roles |

---

## Example Requests & Responses

### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "full_name": "Dr. Budi Santoso",
  "email": "budi@healthtrack.com",
  "password": "doctor123",
  "role": "doctor"
}
```
```json
{
  "id": 2,
  "full_name": "Dr. Budi Santoso",
  "email": "budi@healthtrack.com",
  "role": "doctor",
  "created_at": "2026-05-06T10:00:00Z"
}
```

### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=budi@healthtrack.com&password=doctor123
```
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Book Appointment
```http
POST /appointments/
Authorization: Bearer <token>
Content-Type: application/json

{
  "patient_id": 1,
  "doctor_id": 1,
  "scheduled_at": "2026-05-10T09:00:00",
  "complaint": "Demam 3 hari, batuk kering"
}
```
```json
{
  "id": 1,
  "patient_id": 1,
  "doctor_id": 1,
  "scheduled_at": "2026-05-10T09:00:00",
  "status": "pending",
  "complaint": "Demam 3 hari, batuk kering",
  "notes": null,
  "created_at": "2026-05-06T10:05:00Z"
}
```

### Conflict Detection (409)
```http
POST /appointments/
Authorization: Bearer <token>
Content-Type: application/json

{
  "patient_id": 1,
  "doctor_id": 1,
  "scheduled_at": "2026-05-10T09:20:00",
  "complaint": "Test conflict"
}
```
```json
{
  "detail": "Doctor already has an appointment around that time (ID: 1)"
}
```

### RBAC Enforcement (403)
```http
PATCH /appointments/1
Authorization: Bearer <nurse_token>
Content-Type: application/json

{ "status": "completed" }
```
```json
{
  "detail": "Access denied. Required roles: ['doctor', 'admin']"
}
```

### Create Medical Record
```http
POST /medical-records/
Authorization: Bearer <doctor_token>
Content-Type: application/json

{
  "patient_id": 1,
  "doctor_id": 1,
  "appointment_id": 1,
  "diagnosis": "Infeksi Saluran Pernapasan Atas (ISPA)",
  "prescription": "Paracetamol 500mg 3x1, Ambroxol 30mg 3x1",
  "notes": "Istirahat cukup, minum air putih minimal 2L per hari"
}
```
```json
{
  "id": 1,
  "patient_id": 1,
  "doctor_id": 1,
  "appointment_id": 1,
  "diagnosis": "Infeksi Saluran Pernapasan Atas (ISPA)",
  "prescription": "Paracetamol 500mg 3x1, Ambroxol 30mg 3x1",
  "notes": "Istirahat cukup, minum air putih minimal 2L per hari",
  "created_by": 2,
  "created_at": "2026-05-06T10:10:00Z"
}
```

---

## Project Structure

```
healthtrack-api/
├── app/
│   ├── main.py              # App entrypoint, router registration
│   ├── config.py            # Environment config (pydantic-settings)
│   ├── database.py          # SQLAlchemy engine, session, Base
│   ├── models/              # SQLAlchemy ORM models (DB tables)
│   │   ├── user.py
│   │   ├── patient.py
│   │   ├── doctor.py
│   │   ├── appointment.py
│   │   └── medical_record.py
│   ├── schemas/             # Pydantic schemas (request/response validation)
│   │   ├── user.py
│   │   ├── patient.py
│   │   ├── appointment.py
│   │   └── medical_record.py
│   ├── routers/             # FastAPI route handlers
│   │   ├── auth.py
│   │   ├── patients.py
│   │   ├── doctors.py
│   │   ├── appointments.py
│   │   └── medical_records.py
│   ├── services/            # Business logic layer
│   │   ├── auth.py
│   │   ├── patient.py
│   │   ├── appointment.py
│   │   └── medical_record.py
│   └── core/
│       ├── security.py      # JWT encode/decode, bcrypt hashing
│       └── dependencies.py  # get_current_user, require_role factory
├── .env.example
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/healthtrack_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## Architecture Notes

**Layered architecture** is used to separate concerns:
- **Routers** — handle HTTP request/response only, no business logic
- **Services** — contain all business logic (conflict detection, RBAC enforcement, audit trail)
- **Models** — define database schema via SQLAlchemy ORM
- **Schemas** — validate and serialize data via Pydantic v2

**RBAC** is implemented via a `require_role()` factory in `dependencies.py` that returns a FastAPI dependency — keeping role enforcement declarative at the router level.

**Audit trail** on `medical_records.created_by` ensures every record mutation is traceable to the authenticated user who made it.

---

## License

MIT
