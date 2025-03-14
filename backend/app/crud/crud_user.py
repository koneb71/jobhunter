from typing import Any, Dict, Optional, Union, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.crud.base import CRUDBase
from app.models.user import User, UserType
from app.schemas.user import UserCreate, UserUpdate
from app.core.password import get_password_hash, verify_password
import uuid

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_type(
        self, db: Session, *, user_type: UserType, skip: int = 0, limit: int = 100
    ) -> List[User]:
        return (
            db.query(User)
            .filter(User.user_type == user_type)
            .order_by(desc(User.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        # Check if email already exists
        existing_user = self.get_by_email(db, email=obj_in.email)
        if existing_user:
            raise ValueError("Email already registered")
            
        db_obj = User(
            id=str(uuid.uuid4()),
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            display_name=obj_in.display_name,
            is_superuser=obj_in.is_superuser,
            user_type=obj_in.user_type,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

crud_user = CRUDUser(User) 