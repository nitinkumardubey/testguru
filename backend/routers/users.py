from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from database import get_db
from models import User, UserRole
from schemas import UserCreate, UserUpdate, UserResponse
from fastapi.responses import Response

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
