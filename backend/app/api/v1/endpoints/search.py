from typing import Any
from fastapi import APIRouter, Depends, Query
from supabase import Client

from app.core.deps import get_db
from app.schemas.search import (
    SearchParams, SearchResponse, JobType, ExperienceLevel,
    SortBy, SortOrder
)
from app.services.search import search_service

router = APIRouter()

@router.get("/", response_model=SearchResponse)
def search(
    query: str = Query(None, description="Search query for jobs and companies"),
    job_type: JobType = Query(None, description="Filter by job type"),
    experience_level: ExperienceLevel = Query(None, description="Filter by experience level"),
    location: str = Query(None, description="Filter by location"),
    industry: str = Query(None, description="Filter by industry"),
    salary_min: float = Query(None, description="Minimum salary"),
    salary_max: float = Query(None, description="Maximum salary"),
    remote_only: bool = Query(False, description="Show only remote jobs"),
    posted_within_days: int = Query(None, description="Jobs posted within X days"),
    company_size: str = Query(None, description="Filter by company size"),
    sort_by: SortBy = Query(SortBy.RELEVANCE, description="Sort by field"),
    sort_order: SortOrder = Query(SortOrder.DESC, description="Sort order"),
    page: int = Query(1, description="Page number", ge=1),
    page_size: int = Query(20, description="Items per page", ge=1, le=100),
    db: Client = Depends(get_db),
) -> Any:
    """
    Unified search endpoint for jobs and companies with advanced filtering and pagination.
    """
    search_params = SearchParams(
        query=query,
        job_type=job_type,
        experience_level=experience_level,
        location=location,
        industry=industry,
        salary_min=salary_min,
        salary_max=salary_max,
        remote_only=remote_only,
        posted_within_days=posted_within_days,
        company_size=company_size,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size
    )
    
    return search_service.search(db, search_params) 