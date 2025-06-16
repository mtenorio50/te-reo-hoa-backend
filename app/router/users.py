from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, auth, models, crud
from app.database import get_db

router = APIRouter(tags=["Users"])

@router.get("/", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db), current_user=Depends(auth.require_admin)):
    return crud.get_users(db)

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = auth.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
# Admin-only: List all users

@router.post("/{user_id}/set_admin", response_model=schemas.UserOut)
def set_admin(user_id: int, db: Session = Depends(get_db), current_user=Depends(auth.get_admin_user)):
    user = crud.set_user_role(db, user_id, "admin")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user