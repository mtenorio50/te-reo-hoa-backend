from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import auth, crud, models, schemas
from app.database import get_db

import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Users"])


@router.get("/", response_model=list[schemas.UserOut],
            summary="List all users",
            description="Returns a list of all registered users. Admin access required.")
def list_users(db: Session = Depends(get_db), current_user=Depends(auth.require_admin)):
    """Get all registered users (admin only)."""
    return crud.get_users(db)


@router.post("/register", response_model=schemas.UserOut,
             summary="Register a new user",
             description="Creates a new user account with the specified email and password.")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    db_user = auth.get_user_by_email(db, user.email)
    if db_user:
        logger.warning("Email already registered for: %s", db_user)
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Admin-only: List all users
@router.post("/{user_id}/set_admin", response_model=schemas.UserOut,
             summary="Set user as admin",
             description="Promotes a user to admin privileges. Admin access required.")
def set_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_admin_user),
):
    """Promote a user to admin status (admin only)."""
    user = crud.set_user_role(db, user_id, "admin")
    if not user:
        logger.warning("User not found: %s", user)
        raise HTTPException(status_code=404, detail="User not found")
    return user
