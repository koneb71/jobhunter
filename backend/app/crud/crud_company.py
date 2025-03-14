from typing import Any, Dict, List, Union

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate


class CRUDCompany(CRUDBase[Company, CompanyCreate, CompanyUpdate]):
    def get_by_industry(
        self, db: Session, *, industry: str, skip: int = 0, limit: int = 100
    ) -> List[Company]:
        return (
            db.query(Company)
            .filter(Company.industry == industry)
            .filter(Company.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_location(
        self, db: Session, *, location: str, skip: int = 0, limit: int = 100
    ) -> List[Company]:
        return (
            db.query(Company)
            .filter(Company.location.ilike(f"%{location}%"))
            .filter(Company.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search(
        self,
        db: Session,
        *,
        query: str = "",
        industry: str = "",
        location: str = "",
        skip: int = 0,
        limit: int = 100,
    ) -> List[Company]:
        filters = [Company.is_active == True]

        if query:
            filters.append(Company.name.ilike(f"%{query}%"))
        if industry:
            filters.append(Company.industry == industry)
        if location:
            filters.append(Company.location.ilike(f"%{location}%"))

        return db.query(Company).filter(and_(*filters)).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CompanyCreate, user_id: str) -> Company:
        db_obj = Company(**obj_in.model_dump(), created_by=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Company,
        obj_in: Union[CompanyUpdate, Dict[str, Any]],
    ) -> Company:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field in update_data:
            setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


crud_company = CRUDCompany(Company)
