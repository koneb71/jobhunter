from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Benefit])
def read_benefits(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    category: str = None,
) -> Any:
    """
    Retrieve benefits.
    """
    if category:
        benefits = crud.benefit.get_multi_by_category(
            db, category=category, skip=skip, limit=limit
        )
    else:
        benefits = crud.benefit.get_multi(db, skip=skip, limit=limit)
    return benefits

@router.post("/", response_model=schemas.Benefit)
def create_benefit(
    *,
    db: Session = Depends(deps.get_db),
    benefit_in: schemas.BenefitCreate,
) -> Any:
    """
    Create new benefit.
    """
    benefit = crud.benefit.get_by_name(db, name=benefit_in.name)
    if benefit:
        raise HTTPException(
            status_code=400,
            detail="A benefit with this name already exists.",
        )
    benefit = crud.benefit.create(db, obj_in=benefit_in)
    return benefit

@router.put("/{benefit_id}", response_model=schemas.Benefit)
def update_benefit(
    *,
    db: Session = Depends(deps.get_db),
    benefit_id: int,
    benefit_in: schemas.BenefitUpdate,
) -> Any:
    """
    Update a benefit.
    """
    benefit = crud.benefit.get(db, id=benefit_id)
    if not benefit:
        raise HTTPException(status_code=404, detail="Benefit not found")
    benefit = crud.benefit.update(db, db_obj=benefit, obj_in=benefit_in)
    return benefit

@router.get("/{benefit_id}", response_model=schemas.Benefit)
def read_benefit(
    *,
    db: Session = Depends(deps.get_db),
    benefit_id: int,
) -> Any:
    """
    Get benefit by ID.
    """
    benefit = crud.benefit.get(db, id=benefit_id)
    if not benefit:
        raise HTTPException(status_code=404, detail="Benefit not found")
    return benefit

@router.delete("/{benefit_id}")
def delete_benefit(
    *,
    db: Session = Depends(deps.get_db),
    benefit_id: int,
) -> Any:
    """
    Delete a benefit.
    """
    benefit = crud.benefit.get(db, id=benefit_id)
    if not benefit:
        raise HTTPException(status_code=404, detail="Benefit not found")
    benefit = crud.benefit.remove(db, id=benefit_id)
    return {"success": True} 