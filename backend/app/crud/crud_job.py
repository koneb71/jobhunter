from typing import Any, Dict, List, Optional, Union
from supabase import Client
from datetime import datetime
from app.core.logger import logger

from app.crud.base import CRUDBase
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate

class CRUDJob(CRUDBase[Job, JobCreate, JobUpdate]):
    async def get_by_company(
        self, db: Client, *, company_id: str, skip: int = 0, limit: int = 100
    ) -> List[Job]:
        try:
            response = await db.table("jobs").select("*").eq("company_id", company_id).range(skip, skip + limit - 1).execute()
            return [Job(**item) for item in response.data]
        except Exception as e:
            logger.error(f"Error fetching company jobs: {str(e)}")
            return []

    async def get_featured(
        self, db: Client, *, skip: int = 0, limit: int = 10
    ) -> List[Job]:
        """
        Get featured jobs that are active and not expired.
        """
        try:
            now = datetime.utcnow().isoformat()
            response = await (
                db.table("jobs")
                .select("*")
                .eq("is_featured", True)
                .eq("is_active", True)
                .is_("expires_at", None)
                .or_(f"expires_at.gt.{now}")
                .order("created_at", desc=True)
                .range(skip, skip + limit - 1)
                .execute()
            )
            return [Job(**job) for job in response.data]
        except Exception as e:
            logger.error(f"Error fetching featured jobs: {str(e)}")
            return []

    async def search(
        self,
        db: Client,
        *,
        query: Optional[str] = None,
        location: Optional[str] = None,
        job_type: Optional[str] = None,
        experience_level: Optional[str] = None,
        salary_min: Optional[float] = None,
        salary_max: Optional[float] = None,
        remote_work: Optional[bool] = None,
        visa_sponsorship: Optional[bool] = None,
        company_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 10
    ) -> List[Job]:
        """
        Search jobs with multiple filters.
        """
        try:
            now = datetime.utcnow().isoformat()
            query_builder = (
                db.table("jobs")
                .select("*")
                .eq("is_active", True)
                .is_("expires_at", None)
                .or_(f"expires_at.gt.{now}")
            )

            if query:
                query_builder = query_builder.ilike("title", f"%{query}%")
            if location:
                query_builder = query_builder.ilike("location", f"%{location}%")
            if job_type:
                query_builder = query_builder.eq("job_type", job_type)
            if experience_level:
                query_builder = query_builder.eq("experience_level", experience_level)
            if salary_min is not None:
                query_builder = query_builder.gte("salary_min", salary_min)
            if salary_max is not None:
                query_builder = query_builder.lte("salary_max", salary_max)
            if remote_work is not None:
                query_builder = query_builder.eq("remote_work", remote_work)
            if visa_sponsorship is not None:
                query_builder = query_builder.eq("visa_sponsorship", visa_sponsorship)
            if company_id:
                query_builder = query_builder.eq("company_id", company_id)

            response = await (
                query_builder
                .order("created_at", desc=True)
                .range(skip, skip + limit - 1)
                .execute()
            )
            return [Job(**job) for job in response.data]
        except Exception as e:
            logger.error(f"Error searching jobs: {str(e)}")
            return []

    async def create(
        self,
        db: Client,
        job: JobCreate,
        employer_id: str
    ) -> Optional[Job]:
        """Create a new job."""
        try:
            job_data = job.model_dump()
            job_data["employer_id"] = employer_id
            job_data["created_at"] = datetime.utcnow().isoformat()
            job_data["status"] = "active"
            
            response = await db.table("jobs").insert(job_data).execute()
            if not response.data:
                return None
            return Job(**response.data[0])
        except Exception as e:
            logger.error(f"Error creating job: {str(e)}")
            return None

    async def update(
        self,
        db: Client,
        job_id: str,
        job: JobUpdate
    ) -> Optional[Job]:
        """Update a job."""
        try:
            update_data = job.model_dump(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow().isoformat()
            
            response = await db.table("jobs").update(update_data).eq("id", job_id).execute()
            if not response.data:
                return None
            return Job(**response.data[0])
        except Exception as e:
            logger.error(f"Error updating job {job_id}: {str(e)}")
            return None

    async def delete(
        self,
        db: Client,
        job_id: str
    ) -> bool:
        """Delete a job."""
        try:
            response = await db.table("jobs").delete().eq("id", job_id).execute()
            return bool(response.data)
        except Exception as e:
            logger.error(f"Error deleting job {job_id}: {str(e)}")
            return False

    async def get_employer_jobs(
        self,
        db: Client,
        employer_id: str,
        skip: int = 0,
        limit: int = 10
    ) -> List[Job]:
        """Get all jobs for an employer."""
        try:
            response = await db.table("jobs").select("*").eq("employer_id", employer_id).order("created_at", desc=True).range(skip, skip + limit - 1).execute()
            return [Job(**job) for job in response.data]
        except Exception as e:
            logger.error(f"Error fetching employer jobs: {str(e)}")
            return []

    async def search_jobs(
        self,
        db: Client,
        query: str,
        location: Optional[str] = None,
        skip: int = 0,
        limit: int = 10
    ) -> List[Job]:
        """Search jobs by query and location."""
        try:
            # Build the query
            db_query = db.table("jobs").select("*").eq("status", "active").gte("expires_at", datetime.utcnow().isoformat())
            
            # Add search conditions
            if query:
                db_query = db_query.or_(f"title.ilike.%{query}%,description.ilike.%{query}%")
            if location:
                db_query = db_query.ilike("location", f"%{location}%")
            
            # Execute the query
            response = await db_query.order("created_at", desc=True).range(skip, skip + limit - 1).execute()
            return [Job(**job) for job in response.data]
        except Exception as e:
            logger.error(f"Error searching jobs: {str(e)}")
            return []

crud_job = CRUDJob(Job) 