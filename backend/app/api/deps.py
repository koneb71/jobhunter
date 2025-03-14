from typing import Generator

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.auth import ALGORITHM, oauth2_scheme
from app.core.config import settings
from app.crud.crud_user import crud_user
from app.db.session import SessionLocal
from app.models.user import User, UserType
from app.schemas.token import TokenPayload


def get_db() -> Generator[Session, None, None]:
    """
    Get database session.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Get current authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise credentials_exception

    user = crud_user.get(db, id=token_data.sub)
    if not user:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get current active user.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get current active superuser.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_current_employer(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get current employer user.
    """
    if current_user.user_type != UserType.EMPLOYER:
        raise HTTPException(status_code=400, detail="The user is not an employer")
    return current_user


def get_current_job_seeker(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get current job seeker user.
    """
    if current_user.user_type != UserType.JOB_SEEKER:
        raise HTTPException(status_code=400, detail="The user is not a job seeker")
    return current_user
