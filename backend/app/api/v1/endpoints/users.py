from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, desc, func, or_
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user
from app.core.deps import get_db
from app.crud import crud_user
from app.models.user import User
from app.schemas.profile import (
    ProfileAnalytics,
    ProfileScore,
    ProfileVerification,
    SearchCriteria,
    SearchResult,
    SkillEndorsement,
    SkillRating,
)
from app.schemas.user import (
    AvailabilityStatus,
    BenefitType,
    CompanySize,
    EmploymentPreferences,
    EmploymentType,
    UserCreate,
    UserResponse,
    UserRole,
    UserUpdate,
    WorkSchedule,
)
from app.services.profile import ProfileService
from app.services.search import SearchService

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.get("/", response_model=List[UserResponse])
def read_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return crud_user.get_multi(db, skip=skip, limit=limit)


@router.get("/role/{role}", response_model=List[UserResponse])
def read_users_by_role(
    role: UserRole,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users by role.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return crud_user.get_by_role(db, role=role, skip=skip, limit=limit)


@router.get("/skills", response_model=List[UserResponse])
def read_users_by_skills(
    skills: List[str] = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users by skills.
    """
    return crud_user.get_by_skills(db, skills=skills, skip=skip, limit=limit)


@router.get("/availability/{status}", response_model=List[UserResponse])
def read_users_by_availability(
    status: AvailabilityStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users by availability status.
    """
    return crud_user.get_by_availability(db, status=status, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
def read_user_by_id(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    if not current_user.is_superuser and user.id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return user


@router.post("/", response_model=UserResponse)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new user.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    return crud_user.create(db, obj_in=user_in)


@router.put("/me", response_model=UserResponse)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    return crud_user.update(db, db_obj=current_user, obj_in=user_in)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: str,
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a user.
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    if not current_user.is_superuser and user.id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    return crud_user.update(db, db_obj=user, obj_in=user_in)


@router.delete("/{user_id}")
def delete_user(
    *,
    db: Session = Depends(get_db),
    user_id: str,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete a user.
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    if not current_user.is_superuser and user.id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    crud_user.remove(db, id=user_id)
    return {"status": "success"}


@router.get("/employment-types", response_model=List[str])
def get_employment_types() -> Any:
    """
    Get list of employment types.
    """
    return [e.value for e in EmploymentType]


@router.get("/work-schedules", response_model=List[str])
def get_work_schedules() -> Any:
    """
    Get list of work schedules.
    """
    return [s.value for s in WorkSchedule]


@router.get("/preferred-employment", response_model=List[UserResponse])
def get_users_by_employment_preference(
    employment_type: EmploymentType,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get users by employment preference.
    """
    return crud_user.get_by_employment_preference(
        db, employment_type=employment_type, skip=skip, limit=limit
    )


@router.get("/preferred-schedule", response_model=List[UserResponse])
def get_users_by_work_schedule(
    work_schedule: WorkSchedule,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get users by work schedule preference.
    """
    return crud_user.get_by_work_schedule(
        db, work_schedule=work_schedule, skip=skip, limit=limit
    )


@router.put("/me/employment-preferences", response_model=UserResponse)
def update_employment_preferences(
    *,
    db: Session = Depends(get_db),
    preferences: EmploymentPreferences,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update current user's employment preferences.
    """
    return crud_user.update_employment_preferences(
        db, user=current_user, preferences=preferences
    )


@router.get("/me/employment-preferences", response_model=EmploymentPreferences)
def get_employment_preferences(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user's employment preferences.
    """
    return current_user.employment_preferences


@router.get("/search/employment", response_model=List[UserResponse])
def search_users_by_employment_criteria(
    employment_type: Optional[EmploymentType] = None,
    work_schedule: Optional[WorkSchedule] = None,
    company_size: Optional[CompanySize] = None,
    min_salary: Optional[float] = None,
    max_salary: Optional[float] = None,
    currency: Optional[str] = Query(None, pattern="^[A-Z]{3}$"),
    remote_percentage: Optional[int] = Query(None, ge=0, le=100),
    benefits: Optional[List[BenefitType]] = None,
    location: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Search users by employment criteria.
    """
    return crud_user.search_by_employment_criteria(
        db,
        employment_type=employment_type,
        work_schedule=work_schedule,
        company_size=company_size,
        min_salary=min_salary,
        max_salary=max_salary,
        currency=currency,
        remote_percentage=remote_percentage,
        benefits=benefits,
        location=location,
        skip=skip,
        limit=limit,
    )


@router.get("/search/salary-range", response_model=List[UserResponse])
def search_users_by_salary_range(
    min_salary: float,
    max_salary: float,
    currency: str = Query(..., pattern="^[A-Z]{3}$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Search users by salary range.
    """
    return crud_user.search_by_salary_range(
        db,
        min_salary=min_salary,
        max_salary=max_salary,
        currency=currency,
        skip=skip,
        limit=limit,
    )


@router.get("/search/benefits", response_model=List[UserResponse])
def search_users_by_benefits(
    benefits: List[BenefitType],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Search users by benefits preferences.
    """
    return crud_user.search_by_benefits(db, benefits=benefits, skip=skip, limit=limit)


@router.get("/search/location", response_model=List[UserResponse])
def search_users_by_location(
    location: str,
    max_distance: Optional[int] = Query(None, ge=0, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Search users by location.
    """
    return crud_user.search_by_location(
        db, location=location, max_distance=max_distance, skip=skip, limit=limit
    )


@router.get("/search/work-environment", response_model=List[UserResponse])
def search_users_by_work_environment(
    environment: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Search users by work environment preferences.
    """
    return crud_user.search_by_work_environment(
        db, environment=environment, skip=skip, limit=limit
    )


@router.get("/analytics/employment-preferences", response_model=Dict[str, Any])
def get_employment_preferences_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get analytics about users' employment preferences.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )

    total_users = db.query(func.count(User.id)).scalar()

    # Employment type distribution
    employment_type_dist = (
        db.query(
            User.employment_preferences["employment_type"].label("type"),
            func.count(User.id).label("count"),
        )
        .group_by("type")
        .all()
    )

    # Work schedule distribution
    work_schedule_dist = (
        db.query(
            User.employment_preferences["work_schedule"].label("schedule"),
            func.count(User.id).label("count"),
        )
        .group_by("schedule")
        .all()
    )

    # Salary range distribution
    salary_ranges = [
        (0, 50000),
        (50000, 100000),
        (100000, 150000),
        (150000, float("inf")),
    ]

    salary_dist = []
    for min_sal, max_sal in salary_ranges:
        count = (
            db.query(func.count(User.id))
            .filter(
                User.employment_preferences["min_salary"].astext.cast(float) >= min_sal,
                or_(
                    User.employment_preferences["max_salary"].astext.cast(float)
                    <= max_sal,
                    max_sal == float("inf"),
                ),
            )
            .scalar()
        )
        salary_dist.append(
            {
                "range": f"${min_sal:,} - {'∞' if max_sal == float('inf') else f'${max_sal:,}'}",
                "count": count,
            }
        )

    # Remote work preference distribution
    remote_dist = (
        db.query(
            User.employment_preferences["remote_percentage"].label("percentage"),
            func.count(User.id).label("count"),
        )
        .group_by("percentage")
        .all()
    )

    # Benefits preferences
    benefits_dist = (
        db.query(
            func.jsonb_array_elements_text(
                User.employment_preferences["benefits"]
            ).label("benefit"),
            func.count(User.id).label("count"),
        )
        .group_by("benefit")
        .all()
    )

    return {
        "total_users": total_users,
        "employment_type_distribution": [
            {"type": type_, "count": count, "percentage": (count / total_users) * 100}
            for type_, count in employment_type_dist
        ],
        "work_schedule_distribution": [
            {
                "schedule": schedule,
                "count": count,
                "percentage": (count / total_users) * 100,
            }
            for schedule, count in work_schedule_dist
        ],
        "salary_distribution": [
            {**range_, "percentage": (range_["count"] / total_users) * 100}
            for range_ in salary_dist
        ],
        "remote_work_distribution": [
            {"percentage": pct, "count": count, "ratio": (count / total_users) * 100}
            for pct, count in remote_dist
        ],
        "benefits_preferences": [
            {
                "benefit": benefit,
                "count": count,
                "percentage": (count / total_users) * 100,
            }
            for benefit, count in benefits_dist
        ],
    }


@router.get("/me/profile-score", response_model=ProfileScore)
def get_profile_score(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user's profile score.
    """
    return ProfileService.calculate_profile_score(current_user)


@router.get("/me/skill-ratings", response_model=List[SkillRating])
def get_skill_ratings(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user's skill ratings.
    """
    return ProfileService.get_skill_ratings(current_user)


@router.post("/me/skills/{skill}/endorse", response_model=SkillEndorsement)
def endorse_skill(
    skill: str,
    comment: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    endorser: User = Depends(get_current_active_user),
) -> Any:
    """
    Endorse a user's skill.
    """
    if not current_user.skills or skill not in current_user.skills:
        raise HTTPException(
            status_code=400,
            detail=f"User does not have the skill: {skill}",
        )

    if current_user.id == endorser.id:
        raise HTTPException(
            status_code=400,
            detail="Cannot endorse your own skills",
        )

    return ProfileService.endorse_skill(
        db, user=current_user, endorser=endorser, skill=skill, comment=comment
    )


@router.get("/me/verification", response_model=ProfileVerification)
def get_profile_verification(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user's profile verification status.
    """
    return current_user.profile_verification


@router.get("/me/analytics", response_model=ProfileAnalytics)
def get_profile_analytics(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user's profile analytics.
    """
    return ProfileService.get_profile_analytics(current_user)


@router.post("/search", response_model=SearchResult)
def search_users(
    criteria: SearchCriteria,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Search users based on criteria.
    """
    search_service = SearchService()
    return search_service.search_users(db, criteria)


@router.get("/search/suggestions", response_model=List[str])
def get_search_suggestions(
    query: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get search suggestions based on query.
    """
    search_service = SearchService()
    return search_service.get_user_search_suggestions(db, query)


@router.get("/search/facets", response_model=Dict[str, Any])
def get_search_facets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get search facets for user search.
    """
    search_service = SearchService()
    return search_service.get_user_search_facets(db)
