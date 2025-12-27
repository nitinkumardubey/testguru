from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserCreate(BaseModel):
    email: str
    name: str
    phone_no: Optional[str]
    role: str

class AdminCreate(BaseModel):
    email: str
    name: str
    password: str
    phone_no: Optional[str]
    role: str

class UserUpdate(BaseModel):
    name: Optional[str]
    phone_no: Optional[str]
    role: Optional[str]
    image: Optional[bytes]

class AdminUpdate(BaseModel):
    name: Optional[str]
    password: Optional[str]
    phone_no: Optional[str]
    role: Optional[str]
    image: Optional[bytes]

class UserResponse(BaseModel):
    email: str
    name: str
    phone_no: Optional[str]
    role: str
    has_image: bool

    class Config:
        from_attributes = True

class AdminResponse(BaseModel):
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

class RoleRequest(BaseModel):
    role: str

class ApiPermissions(BaseModel):
    mapped: List[str]
    unmapped: List[str]