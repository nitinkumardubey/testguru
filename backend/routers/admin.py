from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from database import get_db
from models import Admin
from schemas import AdminCreate, AdminUpdate, AdminResponse
router = APIRouter(prefix="/admin", tags=["Admin"])

# CREATE
@router.post("/create")
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    if db.query(Admin).filter(Admin.email == admin.email).first():
        raise HTTPException(status_code=400, detail="Admin already exists")

    new_admin = Admin(
        email=admin.email,
        name=admin.name,
        password=admin.password,  # hash in real apps
        phone_no=admin.phone_no,
        role=admin.role,
        image=None
    )

    db.add(new_admin)
    db.commit()
    return {"message": "Admin created successfully"}

# READ ALL
@router.get("/list_all")
def get_admins(db: Session = Depends(get_db)):
    return db.query(Admin).all()

# READ ONE
@router.get("/{email}", response_model=AdminResponse)
def get_admin(email: str, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.email == email).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    return {
        "email": admin.email,
        "name": admin.name,
        "phone_no": admin.phone_no,
        "role": admin.role,
        "has_image": admin.image is not None
    }

# UPDATE
@router.put("/{email}")
def update_admin(email: str, data: AdminUpdate, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.email == email).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    if data.name is not None:
        admin.name = data.name
    if data.password is not None:
        admin.password = data.password
    if data.phone_no is not None:
        admin.phone_no = data.phone_no
    if data.role is not None:
        admin.role = data.role
    if data.image is not None:
        admin.image = data.image

    db.commit()
    return {"message": "Admin updated successfully"}

# DELETE
@router.delete("/{email}")
def delete_admin(email: str, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.email == email).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    db.delete(admin)
    db.commit()
    return {"message": "Admin deleted successfully"}

