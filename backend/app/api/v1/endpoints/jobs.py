from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.crud_job import crud_job
from app.models.job import ExperienceLevel, Job, JobType
from app.schemas.job import JobCreate, JobResponse, JobUpdate, PaginatedJobResponse

router = APIRouter()


@router.get("/featured", response_model=List[JobResponse])
def get_featured_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(deps.get_db),
) -> List[Job]:
    """
    Get featured jobs.
    """
    return crud_job.get_featured(db, skip=skip, limit=limit)


@router.get("/search", response_model=List[JobResponse])
def search_jobs(
    query: Optional[str] = None,
    location: Optional[str] = None,
    job_type: Optional[JobType] = None,
    experience_level: Optional[ExperienceLevel] = None,
    salary_min: Optional[float] = None,
    salary_max: Optional[float] = None,
    remote_work: Optional[bool] = None,
    visa_sponsorship: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(deps.get_db),
) -> List[Job]:
    """
    Search jobs with multiple filters.
    """
    return crud_job.search(
        db,
        query=query,
        location=location,
        job_type=job_type,
        experience_level=experience_level,
        salary_min=salary_min,
        salary_max=salary_max,
        remote_work=remote_work,
        visa_sponsorship=visa_sponsorship,
        skip=skip,
        limit=limit,
    )


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(deps.get_db)) -> Job:
    """
    Get a job by ID.
    """
    job = crud_job.get(db, id=job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )
    return job


@router.post("/", response_model=JobResponse)
def create_job(
    job_in: JobCreate,
    db: Session = Depends(deps.get_db),
    current_user=Depends(deps.get_current_user),
) -> Job:
    """
    Create a new job.
    """
    return crud_job.create(db, obj_in=job_in, employer_id=current_user.id)


@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_in: JobUpdate,
    db: Session = Depends(deps.get_db),
    current_user=Depends(deps.get_current_user),
) -> Job:
    """
    Update a job.
    """
    job = crud_job.get(db, id=job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )
    if job.employer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return crud_job.update(db, db_obj=job, obj_in=job_in)


@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(deps.get_db),
    current_user=Depends(deps.get_current_user),
) -> dict:
    """
    Delete a job.
    """
    job = crud_job.get(db, id=job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )
    if job.employer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    crud_job.remove(db, id=job_id)
    return {"message": "Job deleted successfully"}


@router.get("/", response_model=PaginatedJobResponse)
def get_jobs(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Get paginated list of jobs.
    """
    skip = (page - 1) * size
    total = crud_job.count(db)
    jobs = crud_job.get_multi(db, skip=skip, limit=size)
    
    return {
        "items": jobs,
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size
    }
