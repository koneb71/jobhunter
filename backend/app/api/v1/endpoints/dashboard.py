from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, or_
from datetime import datetime, timedelta

from app.core.deps import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.job import Job
from app.models.job_application import JobApplication
from app.models.interview import Interview
from app.schemas.dashboard import (
    DashboardStats,
    DashboardJob,
    DashboardCandidate,
    ApplicationTrend,
    ApplicationStatusDistribution
)

router = APIRouter()

@router.get("/", response_model=Dict[str, Any])
async def get_employer_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get employer dashboard data.
    """
    if current_user.user_type != "employer":
        raise HTTPException(
            status_code=403,
            detail="Only employers can access this dashboard",
        )

    # Get basic stats
    total_jobs = db.query(func.count(Job.id)).filter(Job.employer_id == current_user.id).scalar()
    active_jobs = db.query(func.count(Job.id)).filter(
        and_(
            Job.employer_id == current_user.id,
            Job.is_active == True
        )
    ).scalar()
    
    total_applications = db.query(func.count(JobApplication.id)).join(Job).filter(
        Job.employer_id == current_user.id
    ).scalar()
    
    new_applications = db.query(func.count(JobApplication.id)).join(Job).filter(
        and_(
            Job.employer_id == current_user.id,
            JobApplication.created_at >= datetime.utcnow() - timedelta(days=7)
        )
    ).scalar()
    
    total_candidates = db.query(func.count(func.distinct(JobApplication.applicant_id))).join(Job).filter(
        Job.employer_id == current_user.id
    ).scalar()
    
    upcoming_interviews = db.query(func.count(Interview.id)).join(JobApplication).join(Job).filter(
        and_(
            Job.employer_id == current_user.id,
            Interview.scheduled_at >= datetime.utcnow(),
            Interview.status == "scheduled"
        )
    ).scalar()

    # Get active jobs
    active_jobs_list = db.query(Job).filter(
        and_(
            Job.employer_id == current_user.id,
            Job.is_active == True
        )
    ).order_by(desc(Job.created_at)).limit(5).all()

    # Get recent candidates
    recent_candidates = db.query(
        JobApplication.applicant_id,
        func.count(JobApplication.id).label('application_count')
    ).join(Job).filter(
        Job.employer_id == current_user.id
    ).group_by(JobApplication.applicant_id).order_by(desc('application_count')).limit(5).all()

    # Get application trends (last 30 days)
    trends = []
    for i in range(30):
        date = datetime.utcnow() - timedelta(days=i)
        applications = db.query(func.count(JobApplication.id)).join(Job).filter(
            and_(
                Job.employer_id == current_user.id,
                func.date(JobApplication.created_at) == date.date()
            )
        ).scalar()
        
        interviews = db.query(func.count(Interview.id)).join(JobApplication).join(Job).filter(
            and_(
                Job.employer_id == current_user.id,
                func.date(Interview.scheduled_at) == date.date()
            )
        ).scalar()
        
        offers = db.query(func.count(JobApplication.id)).join(Job).filter(
            and_(
                Job.employer_id == current_user.id,
                JobApplication.status == "accepted",
                func.date(JobApplication.updated_at) == date.date()
            )
        ).scalar()
        
        trends.append({
            "date": date.strftime("%Y-%m-%d"),
            "applications": applications,
            "interviews": interviews,
            "offers": offers
        })

    # Get application status distribution
    status_distribution = db.query(
        JobApplication.status,
        func.count(JobApplication.id).label('count')
    ).join(Job).filter(
        Job.employer_id == current_user.id
    ).group_by(JobApplication.status).all()

    return {
        "stats": {
            "total_jobs": total_jobs,
            "active_jobs": active_jobs,
            "total_applications": total_applications,
            "new_applications": new_applications,
            "total_candidates": total_candidates,
            "upcoming_interviews": upcoming_interviews
        },
        "active_jobs": [
            {
                "id": job.id,
                "title": job.title,
                "location": job.location,
                "type": job.job_type,
                "posted_date": job.created_at.isoformat(),
                "applications_count": len(job.applications),
                "status": "active" if job.is_active else "inactive"
            }
            for job in active_jobs_list
        ],
        "recent_candidates": [
            {
                "id": candidate.applicant_id,
                "name": candidate.applicant.display_name or f"{candidate.applicant.first_name} {candidate.applicant.last_name}",
                "position": candidate.job.title,
                "experience": "N/A",  # We'll need to add this to the user model if needed
                "applied_date": candidate.created_at.isoformat(),
                "status": candidate.status
            }
            for candidate in recent_candidates
        ],
        "application_trends": trends,
        "application_status": [
            {
                "name": status,
                "value": count
            }
            for status, count in status_distribution
        ]
    } 