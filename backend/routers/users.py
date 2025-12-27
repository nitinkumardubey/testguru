from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import User, UserRole, EmailOTP
from schemas import UserCreate, UserUpdate, UserResponse, SendOTP, VerifyOTP
from fastapi.responses import Response
import random
from datetime import datetime, timedelta
from email_service import send_email

router = APIRouter(prefix="/users", tags=["Users"])

# CREATE
@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        email=user.email,
        name=user.name,
        password=user.password,  # hash in real apps
        phone_no=user.phone_no,
        role=UserRole(user.role),
        image=None
    )

    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

# READ ALL
@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# READ ONE
@router.get("/{email}", response_model=UserResponse)
def get_user(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "email": user.email,
        "name": user.name,
        "phone_no": user.phone_no,
        "role": user.role.value,
        "has_image": user.image is not None
    }

# UPDATE
@router.put("/{email}")
def update_user(email: str, data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.name is not None:
        user.name = data.name
    if data.phone_no is not None:
        user.phone_no = data.phone_no
    if data.role is not None:
        user.role = UserRole(data.role)

    db.commit()
    return {"message": "User updated successfully"}

# DELETE
@router.delete("/{email}")
def delete_user(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

# UPLOAD IMAGE
@router.post("/{email}/image")
def upload_image(email: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.image = file.file.read()
    db.commit()
    return {"message": "Image uploaded successfully"}

# GET IMAGE
@router.get("/{email}/image")
def get_image(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.image:
        raise HTTPException(status_code=404, detail="Image not found")

    return Response(content=user.image, media_type="image/jpeg")

# UTILITY FUNCTIONS
def generate_otp():
    return str(random.randint(100000, 999999))

def get_expiry_time(minutes: int = 5):
    return datetime.utcnow() + timedelta(minutes=minutes)

@router.post("/send-otp")
def send_otp(data: SendOTP, db: Session = Depends(get_db)):
    otp = generate_otp()
    expiry = get_expiry_time()

    otp_entry = EmailOTP(
        email=data.email,
        otp=otp,
        expiry_time=expiry
    )

    db.add(otp_entry)
    db.commit()

    send_email(data.email, otp)

    return {"message": "OTP sent successfully"}

# ---------------- VERIFY OTP ----------------
@router.post("/verify-otp")
def verify_otp(data: VerifyOTP, db: Session = Depends(get_db)):
    otp_record = db.query(EmailOTP).filter(
        EmailOTP.email == data.email,
        EmailOTP.otp == data.otp,
        EmailOTP.is_verified == False
    ).first()

    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if datetime.utcnow() > otp_record.expiry_time:
        raise HTTPException(
            status_code=400,
            detail="Verification failed due to OTP expiry"
        )

    otp_record.is_verified = True
    db.commit()

    return {"message": "OTP verified successfully"}
