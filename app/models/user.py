from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from app.database import Base
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    doctor = "doctor"
    nurse = "nurse"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.nurse)
    created_at = Column(DateTime(timezone=True), server_default=func.now())