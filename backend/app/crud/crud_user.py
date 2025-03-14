from typing import Any, Dict, Optional, Union, List
from datetime import datetime
from supabase import Client
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserRole

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Client, *, email: str) -> Optional[User]:
        response = db.table("users").select("*").eq("email", email).execute()
        if not response.data:
            return None
        return User(**response.data[0])

    def get_by_role(
        self, db: Client, *, role: UserRole, skip: int = 0, limit: int = 100
    ) -> List[User]:
        response = (
            db.table("users")
            .select("*")
            .eq("role", role)
            .order("created_at", desc=True)
            .range(skip, skip + limit - 1)
            .execute()
        )
        return [User(**item) for item in response.data]

    def get_by_skills(
        self, db: Client, *, skills: List[str], skip: int = 0, limit: int = 100
    ) -> List[User]:
        # Using Postgres array overlap operator
        response = (
            db.table("users")
            .select("*")
            .contains("skills", skills)
            .order("created_at", desc=True)
            .range(skip, skip + limit - 1)
            .execute()
        )
        return [User(**item) for item in response.data]

    def get_by_availability(
        self, db: Client, *, status: str, skip: int = 0, limit: int = 100
    ) -> List[User]:
        response = (
            db.table("users")
            .select("*")
            .eq("availability_status", status)
            .order("created_at", desc=True)
            .range(skip, skip + limit - 1)
            .execute()
        )
        return [User(**item) for item in response.data]

    def create(self, db: Client, *, obj_in: UserCreate) -> User:
        db_obj = obj_in.model_dump()
        db_obj["hashed_password"] = get_password_hash(obj_in.password)
        del db_obj["password"]
        
        # Handle nested objects
        for field in ["education", "work_experience", "portfolio"]:
            if field in db_obj:
                db_obj[field] = [item.model_dump() for item in db_obj[field]]
        
        response = db.table("users").insert(db_obj).execute()
        return User(**response.data[0])

    def update(
        self,
        db: Client,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        
        # Handle nested objects
        for field in ["education", "work_experience", "portfolio"]:
            if field in update_data:
                update_data[field] = [item.model_dump() for item in update_data[field]]
        
        response = (
            db.table("users")
            .update(update_data)
            .eq("id", db_obj.id)
            .execute()
        )
        return User(**response.data[0])

    def authenticate(
        self, db: Client, *, email: str, password: str
    ) -> Optional[User]:
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