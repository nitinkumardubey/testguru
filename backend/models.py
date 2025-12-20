from sqlalchemy import Column, String, Enum, LargeBinary
from database import Base
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
