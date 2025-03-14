from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.skill import Skill
from app.schemas.skill import SkillCreate, SkillUpdate


class CRUDSkill(CRUDBase[Skill, SkillCreate, SkillUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Skill]:
        return db.query(Skill).filter(Skill.name == name).first()

    def get_multi_by_category(
        self, db: Session, *, category: str, skip: int = 0, limit: int = 100
    ) -> List[Skill]:
        return (
            db.query(Skill)
            .filter(Skill.category == category)
            .offset(skip)
            .limit(limit)
            .all()
        )

skill = CRUDSkill(Skill) 