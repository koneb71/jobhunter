from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from supabase import Client

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        """
        self.model = model

    def get(self, db: Client, id: str) -> Optional[ModelType]:
        response = db.table(self.model.__tablename__).select("*").eq("id", id).execute()
        if response.data:
            return self.model(**response.data[0])
        return None

    def get_multi(
        self, db: Client, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        response = (
            db.table(self.model.__tablename__)
            .select("*")
            .range(skip, skip + limit - 1)
            .execute()
        )
        return [self.model(**item) for item in response.data]

    def create(self, db: Client, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = obj_in.model_dump()
        response = db.table(self.model.__tablename__).insert(db_obj).execute()
        return self.model(**response.data[0])

    def update(
        self,
        db: Client,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        response = (
            db.table(self.model.__tablename__)
            .update(update_data)
            .eq("id", db_obj.id)
            .execute()
        )
        return self.model(**response.data[0])

    def remove(self, db: Client, *, id: str) -> ModelType:
        response = (
            db.table(self.model.__tablename__)
            .delete()
            .eq("id", id)
            .execute()
        )
        return self.model(**response.data[0]) 