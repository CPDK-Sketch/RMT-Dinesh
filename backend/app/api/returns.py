from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db import models
from app.schemas.returns import ReturnCreate, ReturnUpdate, ReturnOut
from app.services.auth import require_role
from app.services.auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/returns/", response_model=ReturnOut)
def create_return(return_data: ReturnCreate, db: Session = Depends(get_db), user=Depends(require_role("returns"))):
    db_return = models.Return(**return_data.dict())
    db.add(db_return)
    db.commit()
    db.refresh(db_return)
    return db_return

@router.get("/returns/{return_id}", response_model=ReturnOut)
def get_return(return_id: int, db: Session = Depends(get_db), user=Depends(require_role("admin"))):
    return_obj = db.query(models.Return).filter(models.Return.id == return_id).first()
    if not return_obj:
        raise HTTPException(status_code=404, detail="Return not found")
    return return_obj

@router.put("/returns/{return_id}", response_model=ReturnOut)
def update_return(return_id: int, return_data: ReturnUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return_obj = db.query(models.Return).filter(models.Return.id == return_id).first()
    if not return_obj:
        raise HTTPException(status_code=404, detail="Return not found")
    for field, value in return_data.dict(exclude_unset=True).items():
        setattr(return_obj, field, value)
    db.commit()
    db.refresh(return_obj)
    return return_obj