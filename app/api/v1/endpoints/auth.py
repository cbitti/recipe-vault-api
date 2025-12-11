from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import User, UserCreate
from app.db import crud_user
from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.core import security
from app.core.config import settings
from app.schemas.token import Token

router = APIRouter()


@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    # 1. Check if user already exists
    user = crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    # 2. Create new user
    user = crud_user.create_user(db, user=user_in)
    return user


@router.post("/token", response_model=Token)
def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    # 1. Authenticate the user
    user = crud_user.get_user_by_email(db, email=form_data.username)

    if not user or not security.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    # 2. Check if user is active
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    # 3. Create Access Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            subject=user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
