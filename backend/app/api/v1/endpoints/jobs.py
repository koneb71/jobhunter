from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from supabase import Client

from app.crud.crud_job import crud_job
from app.schemas.job import Job
from app.api import deps

router = APIRouter()

@router.get("/featured", response_model=List[Job])
async def get_featured_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Client = Depends(deps.get_db)
) -> List[Job]:
    """
    Get featured jobs.
    """
    return await crud_job.get_featured(db, skip=skip, limit=limit)

@router.get("/search", response_model=List[Job])
async def search_jobs(
    query: str = Query("", min_length=1),
    location: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Client = Depends(deps.get_db)
) -> List[Job]:
    """
    Search jobs by query and location.
    """
    return await crud_job.search_jobs(db, query=query, location=location, skip=skip, limit=limit)

@router.get("/{job_id}", response_model=Job)
async def get_job(
    job_id: str,
    db: Client = Depends(deps.get_db)
) -> Job:
    """
    Get a job by ID.
    """
    return await crud_job.get(db, job_id)

@router.post("/", response_model=Job)
async def create_job(
    job: Job,
    db: Client = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
) -> Job:
    """
    Create a new job.
    """
    return await crud_job.create(db, job=job, employer_id=current_user.id)

@router.put("/{job_id}", response_model=Job)
async def update_job(
    job_id: str,
    job: Job,
    db: Client = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
) -> Job:
    """
    Update a job.
    """
    return await crud_job.update(db, job_id=job_id, job=job)

@router.delete("/{job_id}")
async def delete_job(
    job_id: str,
    db: Client = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
) -> bool:
    """
    Delete a job.
    """
    return await crud_job.delete(db, job_id=job_id) 