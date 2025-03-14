from typing import Any, Dict, List, Optional, Union
from supabase import Client

from app.crud.base import CRUDBase
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate

class CRUDCompany(CRUDBase[Company, CompanyCreate, CompanyUpdate]):
    def get_by_industry(
        self, db: Client, *, industry: str, skip: int = 0, limit: int = 100
    ) -> List[Company]:
        response = (
            db.table("companies")
            .select("*")
            .eq("industry", industry)
            .eq("is_active", True)
            .range(skip, skip + limit - 1)
            .execute()
        )
        return [Company(**item) for item in response.data]

    def get_by_location(
        self, db: Client, *, location: str, skip: int = 0, limit: int = 100
    ) -> List[Company]:
        response = (
            db.table("companies")
            .select("*")
            .ilike("location", f"%{location}%")
            .eq("is_active", True)
            .range(skip, skip + limit - 1)
            .execute()
        )
        return [Company(**item) for item in response.data]

    def search(
        self,
        db: Client,
        *,
        query: str = "",
        industry: str = "",
        location: str = "",
        skip: int = 0,
        limit: int = 100
    ) -> List[Company]:
        query_builder = db.table("companies").select("*")
        
        if query:
            query_builder = query_builder.ilike("name", f"%{query}%")
        if industry:
            query_builder = query_builder.eq("industry", industry)
        if location:
            query_builder = query_builder.ilike("location", f"%{location}%")
            
        query_builder = query_builder.eq("is_active", True)
        response = query_builder.range(skip, skip + limit - 1).execute()
        
        return [Company(**item) for item in response.data]

    def create(
        self, db: Client, *, obj_in: CompanyCreate, user_id: str
    ) -> Company:
        db_obj = obj_in.model_dump()
        db_obj["created_by"] = user_id
        response = db.table("companies").insert(db_obj).execute()
        return Company(**response.data[0])

    def update(
        self,
        db: Client,
        *,
        db_obj: Company,
        obj_in: Union[CompanyUpdate, Dict[str, Any]]
    ) -> Company:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        response = (
            db.table("companies")
            .update(update_data)
            .eq("id", db_obj.id)
            .execute()
        )
        return Company(**response.data[0])

crud_company = CRUDCompany(Company) 