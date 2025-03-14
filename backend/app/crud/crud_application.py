from typing import Any, Dict, List, Optional, Union
from supabase import Client

from app.crud.base import CRUDBase
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationUpdate

class CRUDApplication(CRUDBase[Application, ApplicationCreate, ApplicationUpdate]):
    def get_by_user(
        self, db: Client, *, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[Application]:
        response = (
            db.table("applications")
            .select("*, jobs(title, companies(name))")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .range(skip, skip + limit - 1)
            .execute()
        )
        applications = []
        for item in response.data:
            app_data = item.copy()
            app_data["job_title"] = app_data.pop("jobs")["title"]
            app_data["company_name"] = app_data["jobs"]["companies"]["name"]
            applications.append(Application(**app_data))
        return applications

    def get_by_job(
        self, db: Client, *, job_id: str, skip: int = 0, limit: int = 100
    ) -> List[Application]:
        response = (
            db.table("applications")
            .select("*, users(full_name)")
            .eq("job_id", job_id)
            .order("created_at", desc=True)
            .range(skip, skip + limit - 1)
            .execute()
        )
        applications = []
        for item in response.data:
            app_data = item.copy()
            app_data["user_name"] = app_data.pop("users")["full_name"]
            applications.append(Application(**app_data))
        return applications

    def get_by_status(
        self, db: Client, *, status: str, skip: int = 0, limit: int = 100
    ) -> List[Application]:
        response = (
            db.table("applications")
            .select("*, jobs(title, companies(name)), users(full_name)")
            .eq("status", status)
            .order("created_at", desc=True)
            .range(skip, skip + limit - 1)
            .execute()
        )
        applications = []
        for item in response.data:
            app_data = item.copy()
            app_data["job_title"] = app_data.pop("jobs")["title"]
            app_data["company_name"] = app_data["jobs"]["companies"]["name"]
            app_data["user_name"] = app_data.pop("users")["full_name"]
            applications.append(Application(**app_data))
        return applications

    def create(
        self, db: Client, *, obj_in: ApplicationCreate, user_id: str
    ) -> Application:
        db_obj = obj_in.model_dump()
        db_obj["user_id"] = user_id
        response = db.table("applications").insert(db_obj).execute()
        return Application(**response.data[0])

    def update(
        self,
        db: Client,
        *,
        db_obj: Application,
        obj_in: Union[ApplicationUpdate, Dict[str, Any]]
    ) -> Application:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        response = (
            db.table("applications")
            .update(update_data)
            .eq("id", db_obj.id)
            .execute()
        )
        return Application(**response.data[0])

crud_application = CRUDApplication(Application) 