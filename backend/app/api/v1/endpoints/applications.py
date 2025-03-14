from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from supabase import Client

from app.core.deps import get_db
from app.core.security import get_current_active_user
from app.crud import crud_application, crud_job
from app.models.user import User
from app.schemas.application import ApplicationCreate, ApplicationResponse, ApplicationUpdate

router = APIRouter()

@router.get("/my-applications", response_model=List[ApplicationResponse])
def get_my_applications(
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get current user's applications.
    """
    return crud_application.get_by_user(db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/job/{job_id}", response_model=List[ApplicationResponse])
def get_job_applications(
    job_id: str,
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get applications for a specific job.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return crud_application.get_by_job(db, job_id=job_id, skip=skip, limit=limit)

@router.get("/status/{status}", response_model=List[ApplicationResponse])
def get_applications_by_status(
    status: str,
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get applications by status.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return crud_application.get_by_status(db, status=status, skip=skip, limit=limit)

@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(
    application_id: str,
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific application by id.
    """
    application = crud_application.get(db, id=application_id)
    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )
    if not current_user.is_superuser and application.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return application

@router.post("/", response_model=ApplicationResponse)
def create_application(
    *,
    db: Client = Depends(get_db),
    application_in: ApplicationCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new application.
    """
    # Check if job exists and is active
    job = crud_job.get(db, id=application_in.job_id)
    if not job or not job.is_active:
        raise HTTPException(
            status_code=404,
            detail="Job not found or not active",
        )
    
    # Check if user has already applied
    existing_applications = crud_application.get_by_user(db, user_id=current_user.id)
    for app in existing_applications:
        if app.job_id == application_in.job_id:
            raise HTTPException(
                status_code=400,
                detail="You have already applied for this job",
            )
    
    return crud_application.create(db, obj_in=application_in, user_id=current_user.id)

@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application(
    *,
    db: Client = Depends(get_db),
    application_id: str,
    application_in: ApplicationUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update an application.
    """
    application = crud_application.get(db, id=application_id)
    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )
    if not current_user.is_superuser and application.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return crud_application.update(db, db_obj=application, obj_in=application_in)

@router.delete("/{application_id}")
def delete_application(
    *,
    db: Client = Depends(get_db),
    application_id: str,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete an application.
    """
    application = crud_application.get(db, id=application_id)
    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )
    if not current_user.is_superuser and application.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return crud_application.remove(db, id=application_id) 