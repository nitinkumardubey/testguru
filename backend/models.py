from sqlalchemy import Integer, Boolean, DateTime, Column, String, Enum, LargeBinary, BigInteger, Text, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
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

class Admin(Base):
    __tablename__ = "admins"

    email = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone_no = Column(String)
    image = Column(LargeBinary, nullable=True)
    role = Column(Enum(UserRole), nullable=False)


class ApiManage(Base):
    __tablename__ = "api_manage"

    role = Column(String, primary_key=True, index=True)
    permissions = Column(JSONB, nullable=False)


class ApiLog(Base):
    __tablename__ = "api_logs"

    id = Column(BigInteger, primary_key=True, index=True)
    path = Column(Text, nullable=False)
    method = Column(Text, nullable=False)
    status_code = Column(Integer)
    response_time_ms = Column(Integer)
    ip_address = Column(Text)
    request_body = Column(JSONB)
    created_at = Column(TIMESTAMP, server_default=func.now())