from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime

class RoleEnum(str, Enum):
    admin = "admin"
    doctor = "doctor"
    nurse = "nurse"

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.nurse

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: RoleEnum
    created_at: datetime

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: int | None = None
    role: str| None = None