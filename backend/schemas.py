from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: str
    name: str
    password: str
    phone_no: Optional[str]
    role: str

class UserUpdate(BaseModel):
    name: Optional[str]
    phone_no: Optional[str]
    role: Optional[str]

class UserResponse(BaseModel):
    email: str
    name: str
    phone_no: Optional[str]
    role: str
    has_image: bool

    class Config:
        from_attributes = True


class SendOTP(BaseModel):
    email: EmailStr

class VerifyOTP(BaseModel):
    email: EmailStr
    otp: str