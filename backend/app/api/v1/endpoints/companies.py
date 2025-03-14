from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.api.deps import get_current_active_user
from app.crud import crud_company
from app.models.user import User
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate

router = APIRouter()

@router.get("/search", response_model=List[CompanyResponse])
def search_companies(
    db: Session = Depends(get_db),
    query: str = "",
    industry: str = "",
    location: str = "",
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Search companies by name, industry, and location.
    """
    return crud_company.search(
        db,
        query=query,
        industry=industry,
        location=location,
        skip=skip,
        limit=limit
    )

@router.get("/industry/{industry}", response_model=List[CompanyResponse])
def get_companies_by_industry(
    industry: str,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get companies by industry.
    """
    return crud_company.get_by_industry(db, industry=industry, skip=skip, limit=limit)

@router.get("/location/{location}", response_model=List[CompanyResponse])
def get_companies_by_location(
    location: str,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get companies by location.
    """
    return crud_company.get_by_location(db, location=location, skip=skip, limit=limit)

@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: str,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific company by id.
    """
    company = crud_company.get(db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )
    return company

@router.post("/", response_model=CompanyResponse)
def create_company(
    *,
    db: Session = Depends(get_db),
    company_in: CompanyCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new company.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return crud_company.create(db, obj_in=company_in, user_id=current_user.id)

@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(
    *,
    db: Session = Depends(get_db),
    company_id: str,
    company_in: CompanyUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a company.
    """
    company = crud_company.get(db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return crud_company.update(db, db_obj=company, obj_in=company_in)

@router.delete("/{company_id}")
def delete_company(
    *,
    db: Session = Depends(get_db),
    company_id: str,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete a company.
    """
    company = crud_company.get(db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return crud_company.remove(db, id=company_id) 