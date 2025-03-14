from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from sqlalchemy import and_, desc, or_
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.crud.base import CRUDBase
from app.models.job import ExperienceLevel, Job, JobType
from app.schemas.job import JobCreate, JobUpdate


class CRUDJob(CRUDBase[Job, JobCreate, JobUpdate]):
    def get_by_employer(
        self, db: Session, *, employer_id: int, skip: int = 0, limit: int = 100
    ) -> List[Job]:
        return (
            db.query(Job)
            .filter(Job.employer_id == employer_id)
            .order_by(desc(Job.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_featured(self, db: Session, *, skip: int = 0, limit: int = 10) -> List[Job]:
        """
        Get featured jobs that are active and not expired.
        """
        now = datetime.utcnow()
        return (
            db.query(Job)
            .filter(
                Job.is_featured == True,
                Job.is_active == True,
                or_(Job.expires_at.is_(None), Job.expires_at > now),
            )
            .order_by(desc(Job.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search(
        self,
        db: Session,
        *,
        query: Optional[str] = None,
        location: Optional[str] = None,
        job_type: Optional[JobType] = None,
        experience_level: Optional[ExperienceLevel] = None,
        salary_min: Optional[float] = None,
        salary_max: Optional[float] = None,
        remote_work: Optional[bool] = None,
        visa_sponsorship: Optional[bool] = None,
        employer_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[Job]:
        """
        Search jobs with multiple filters.
        """
        now = datetime.utcnow()
        filters = [
            Job.is_active == True,
            or_(Job.expires_at.is_(None), Job.expires_at > now),
        ]

        if query:
            filters.append(
                or_(Job.title.ilike(f"%{query}%"), Job.description.ilike(f"%{query}%"))
            )
        if location:
            filters.append(Job.location.ilike(f"%{location}%"))
        if job_type:
            filters.append(Job.job_type == job_type)
        if experience_level:
            filters.append(Job.experience_level == experience_level)
        if salary_min is not None:
            filters.append(Job.salary_min >= salary_min)
        if salary_max is not None:
            filters.append(Job.salary_max <= salary_max)
        if remote_work is not None:
            filters.append(Job.remote_work == remote_work)
        if visa_sponsorship is not None:
            filters.append(Job.visa_sponsorship == visa_sponsorship)
        if employer_id:
            filters.append(Job.employer_id == employer_id)

        return (
            db.query(Job)
            .filter(and_(*filters))
            .order_by(desc(Job.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: JobCreate, employer_id: int) -> Job:
        """Create a new job."""
        db_obj = Job(
            title=obj_in.title,
            description=obj_in.description,
            location=obj_in.location,
            salary_min=obj_in.salary_min,
            salary_max=obj_in.salary_max,
            job_type=obj_in.job_type,
            experience_level=obj_in.experience_level,
            required_skills=obj_in.required_skills,
            preferred_skills=obj_in.preferred_skills,
            benefits=obj_in.benefits,
            is_featured=obj_in.is_featured,
            is_active=True,
            expires_at=obj_in.expires_at,
            employer_id=employer_id,
            department=obj_in.department,
            remote_work=obj_in.remote_work,
            visa_sponsorship=obj_in.visa_sponsorship,
            relocation_assistance=obj_in.relocation_assistance,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Job, obj_in: Union[JobUpdate, Dict[str, Any]]
    ) -> Job:
        """Update a job."""
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def delete(self, db: Session, *, id: int) -> Optional[Job]:
        """Delete a job."""
        obj = db.query(Job).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


crud_job = CRUDJob(Job)
