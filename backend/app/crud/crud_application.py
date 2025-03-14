from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.crud.base import CRUDBase
from app.models.job_application import JobApplication
from app.schemas.job_application import JobApplicationCreate, JobApplicationUpdate, ApplicationStatus

class CRUDJobApplication(CRUDBase[JobApplication, JobApplicationCreate, JobApplicationUpdate]):
    def get_by_applicant(
        self, db: Session, *, applicant_id: str, skip: int = 0, limit: int = 100
    ) -> List[JobApplication]:
        return (
            db.query(JobApplication)
            .filter(JobApplication.applicant_id == applicant_id)
            .order_by(desc(JobApplication.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_job(
        self, db: Session, *, job_id: str, skip: int = 0, limit: int = 100
    ) -> List[JobApplication]:
        return (
            db.query(JobApplication)
            .filter(JobApplication.job_id == job_id)
            .order_by(desc(JobApplication.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self, db: Session, *, status: str, skip: int = 0, limit: int = 100
    ) -> List[JobApplication]:
        return (
            db.query(JobApplication)
            .filter(JobApplication.status == status)
            .order_by(desc(JobApplication.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(
        self, db: Session, *, obj_in: JobApplicationCreate, applicant_id: str
    ) -> JobApplication:
        db_obj = JobApplication(
            job_id=obj_in.job_id,
            applicant_id=applicant_id,
            cover_letter=obj_in.cover_letter,
            resume_url=obj_in.resume_url,
            status=ApplicationStatus.PENDING,
            expected_salary=obj_in.expected_salary,
            availability_date=obj_in.availability_date,
            additional_info=obj_in.additional_info
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: JobApplication,
        obj_in: Union[JobApplicationUpdate, Dict[str, Any]]
    ) -> JobApplication:
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

crud_job_application = CRUDJobApplication(JobApplication) 