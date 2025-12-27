from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert


from database import get_db
from models import ApiManage
from schemas import RoleRequest, ApiPermissions

router = APIRouter(prefix="/api_management", tags=["API Management"])

@router.post("/api_manage")
def upsert_api_manage(
    role: str,
    payload: ApiPermissions,
    db: Session = Depends(get_db)
):
    stmt = insert(ApiManage).values(
        role=role,
        permissions={
            "mapped": payload.mapped,
            "unmapped": payload.unmapped
        }
    ).on_conflict_do_update(
        index_elements=["role"],
        set_={
            "permissions": {
                "mapped": payload.mapped,
                "unmapped": payload.unmapped
            }
        }
    )

    db.execute(stmt)
    db.commit()

    return {"message": f"Permissions saved for role '{role}'"}

@router.post("/api_manage/get")
def get_api_manage(payload: RoleRequest, db: Session = Depends(get_db)):
    record = db.query(ApiManage).filter(ApiManage.role == payload.role).first()

    if not record:
        return {"mapped": [], "unmapped": []}

    return record.permissions
