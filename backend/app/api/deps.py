from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from supabase import Client, create_client

from app.core.config import settings
from app.core.security import ALGORITHM
from app.models.user import User
from app.schemas.token import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_db() -> Generator[Client, None, None]:
    """
    Get database client.
    """
    try:
        client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        yield client
    finally:
        # Clean up if needed
        pass

async def get_current_user(
    db: Client = Depends(get_db),
    token: str = Depends(oauth2_scheme)
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
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise credentials_exception

    # Get user from database
    response = await db.table("users").select("*").eq("id", token_data.sub).execute()
    if not response.data:
        raise credentials_exception

    user = User(**response.data[0])
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

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
    if current_user.role != "employer":
        raise HTTPException(
            status_code=400, detail="The user is not an employer"
        )
    return current_user

def get_current_job_seeker(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get current job seeker user.
    """
    if current_user.role != "job_seeker":
        raise HTTPException(
            status_code=400, detail="The user is not a job seeker"
        )
    return current_user 