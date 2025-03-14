from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.benefit import Benefit
from app.schemas.benefit import BenefitCreate, BenefitUpdate

class CRUDBenefit(CRUDBase[Benefit, BenefitCreate, BenefitUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Benefit]:
        return db.query(Benefit).filter(Benefit.name == name).first()

    def get_multi_by_category(
        self, db: Session, *, category: str, skip: int = 0, limit: int = 100
    ) -> List[Benefit]:
        return (
            db.query(Benefit)
            .filter(Benefit.category == category)
            .offset(skip)
            .limit(limit)
            .all()
        )

benefit = CRUDBenefit(Benefit) 