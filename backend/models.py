from sqlalchemy import Integer, Boolean, DateTime, Column, String, Enum, LargeBinary
from database import Base
from datetime import datetime
import enum

class UserRole(enum.Enum):
    admin = "admin"
    user = "user"
    creator = "creator"

class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone_no = Column(String)
    image = Column(LargeBinary, nullable=True)
    role = Column(Enum(UserRole), nullable=False)

class EmailOTP(Base):
    __tablename__ = "email_otps"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    otp = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    expiry_time = Column(DateTime, nullable=False)