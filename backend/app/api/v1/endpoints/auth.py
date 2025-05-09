from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.core.config import settings
from app.core.security import create_access_token
from app.crud import crud_user
from app.schemas.auth import Token, LoginRequest
from app.schemas.user import UserCreate

router = APIRouter()


@router.post("/register", response_model=Token)
async def register(*, db: Session = Depends(deps.get_db), user_in: UserCreate) -> Any:
    """
    Register new user.
    """
    try:
        user = crud_user.create(db, obj_in=user_in)
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(user.id, expires_delta=access_token_expires)

        return {"access_token": access_token, "token_type": "bearer", "user": user}
    except ValueError as e:
        if "Email already registered" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This email is already registered. Please use a different email or try logging in.",
            )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=Token)
async def login(
    *,
    db: Session = Depends(deps.get_db),
    login_data: LoginRequest,
) -> Any:
    """
    Login endpoint to get an access token for future requests.
    """
    user = crud_user.authenticate(
        db, email=login_data.email, password=login_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.id, expires_delta=access_token_expires)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "display_name": user.display_name,
            "user_type": user.user_type,
        }
    }


@router.post("/refresh-token", response_model=Token)
async def refresh_token(
    current_user=Depends(deps.get_current_user),
) -> Any:
    """
    Refresh access token.
    """
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        current_user.id, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer", "user": current_user}
