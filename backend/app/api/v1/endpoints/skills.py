from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Skill])
def read_skills(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    category: str = None,
) -> Any:
    """
    Retrieve skills.
    """
    if category:
        skills = crud.skill.get_multi_by_category(
            db, category=category, skip=skip, limit=limit
        )
    else:
        skills = crud.skill.get_multi(db, skip=skip, limit=limit)
    return skills

@router.post("/", response_model=schemas.Skill)
def create_skill(
    *,
    db: Session = Depends(deps.get_db),
    skill_in: schemas.SkillCreate,
) -> Any:
    """
    Create new skill.
    """
    skill = crud.skill.get_by_name(db, name=skill_in.name)
    if skill:
        raise HTTPException(
            status_code=400,
            detail="A skill with this name already exists.",
        )
    skill = crud.skill.create(db, obj_in=skill_in)
    return skill

@router.put("/{skill_id}", response_model=schemas.Skill)
def update_skill(
    *,
    db: Session = Depends(deps.get_db),
    skill_id: int,
    skill_in: schemas.SkillUpdate,
) -> Any:
    """
    Update a skill.
    """
    skill = crud.skill.get(db, id=skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    skill = crud.skill.update(db, db_obj=skill, obj_in=skill_in)
    return skill

@router.get("/{skill_id}", response_model=schemas.Skill)
def read_skill(
    *,
    db: Session = Depends(deps.get_db),
    skill_id: int,
) -> Any:
    """
    Get skill by ID.
    """
    skill = crud.skill.get(db, id=skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@router.delete("/{skill_id}")
def delete_skill(
    *,
    db: Session = Depends(deps.get_db),
    skill_id: int,
) -> Any:
    """
    Delete a skill.
    """
    skill = crud.skill.get(db, id=skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    skill = crud.skill.remove(db, id=skill_id)
    return {"success": True} 