from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_job_application, crud_job
from app.models.user import User
from app.schemas.job_application import JobApplicationCreate, JobApplicationResponse, JobApplicationUpdate

router = APIRouter()

@router.get("/my-applications", response_model=List[JobApplicationResponse])
def get_my_applications(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get current user's applications.
    """
    return crud_job_application.get_by_applicant(db, applicant_id=current_user.id, skip=skip, limit=limit)

@router.get("/job/{job_id}", response_model=List[JobApplicationResponse])
def get_job_applications(
    job_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
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
    return crud_job_application.get_by_job(db, job_id=job_id, skip=skip, limit=limit)

@router.get("/status/{status}", response_model=List[JobApplicationResponse])
def get_applications_by_status(
    status: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
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
    return crud_job_application.get_by_status(db, status=status, skip=skip, limit=limit)

@router.get("/{application_id}", response_model=JobApplicationResponse)
def get_application(
    application_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific application by id.
    """
    application = crud_job_application.get(db, id=application_id)
    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )
    if not current_user.is_superuser and application.applicant_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return application

@router.post("/", response_model=JobApplicationResponse)
def create_application(
    *,
    db: Session = Depends(deps.get_db),
    application_in: JobApplicationCreate,
    current_user: User = Depends(deps.get_current_active_user),
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
    existing_applications = crud_job_application.get_by_applicant(db, applicant_id=current_user.id)
    for app in existing_applications:
        if app.job_id == application_in.job_id:
            raise HTTPException(
                status_code=400,
                detail="You have already applied for this job",
            )
    
    return crud_job_application.create(db, obj_in=application_in, applicant_id=current_user.id)

@router.put("/{application_id}", response_model=JobApplicationResponse)
def update_application(
    *,
    db: Session = Depends(deps.get_db),
    application_id: str,
    application_in: JobApplicationUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an application.
    """
    application = crud_job_application.get(db, id=application_id)
    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )
    if not current_user.is_superuser and application.applicant_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return crud_job_application.update(db, db_obj=application, obj_in=application_in)

@router.delete("/{application_id}")
def delete_application(
    *,
    db: Session = Depends(deps.get_db),
    application_id: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an application.
    """
    application = crud_job_application.get(db, id=application_id)
    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )
    if not current_user.is_superuser and application.applicant_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return crud_job_application.remove(db, id=application_id) 