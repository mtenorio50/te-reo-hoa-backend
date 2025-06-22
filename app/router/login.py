from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import auth, schemas
from app.database import get_db

import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Login"])


@router.post("/", response_model=schemas.Token,
             summary="User login",
             description="Authenticate with email and password. Returns a JWT access token if successful.")
# @router.post("", response_model=schemas.Token,
#             summary="User login (alternative)",
#             description="Authenticate with email and password. Returns a JWT access token if successful.")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """Authenticate user and issue JWT token."""
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.error("Incorrect email or password: %s", user)
        raise HTTPException(
            status_code=400, detail="Incorrect email or password")
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}
