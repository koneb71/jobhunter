from typing import Any, List, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, Query
from supabase import Client

from app.core.deps import get_db
from app.core.security import get_current_active_user
from app.crud import crud_user
from app.models.user import User
from app.schemas.user import (
    UserCreate, UserUpdate, User as UserSchema,
    UserRole, AvailabilityStatus, EmploymentType,
    WorkSchedule, EmploymentPreferences, CompanySize,
    BenefitType
)
from app.schemas.profile import (
    ProfileScore, SkillRating, SkillEndorsement,
    ProfileVerification, ProfileAnalytics, SearchCriteria,
    SearchResult
)
from app.services.profile import ProfileService
from app.services.search import SearchService

router = APIRouter()

@router.get("/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.get("/", response_model=List[UserSchema])
def read_users(
    db: Client = Depends(get_db),
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

@router.get("/role/{role}", response_model=List[UserSchema])
def read_users_by_role(
    role: UserRole,
    db: Client = Depends(get_db),
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

@router.get("/skills", response_model=List[UserSchema])
def read_users_by_skills(
    skills: List[str] = Query(...),
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users by skills.
    """
    return crud_user.get_by_skills(db, skills=skills, skip=skip, limit=limit)

@router.get("/availability/{status}", response_model=List[UserSchema])
def read_users_by_availability(
    status: AvailabilityStatus,
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users by availability status.
    """
    return crud_user.get_by_availability(db, status=status, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserSchema)
def read_user_by_id(
    user_id: str,
    db: Client = Depends(get_db),
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

@router.post("/", response_model=UserSchema)
def create_user(
    *,
    db: Client = Depends(get_db),
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

@router.put("/me", response_model=UserSchema)
def update_user_me(
    *,
    db: Client = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    return crud_user.update(db, db_obj=current_user, obj_in=user_in)

@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    *,
    db: Client = Depends(get_db),
    user_id: str,
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a user.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return crud_user.update(db, db_obj=user, obj_in=user_in)

@router.delete("/{user_id}")
def delete_user(
    *,
    db: Client = Depends(get_db),
    user_id: str,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete a user.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return crud_user.remove(db, id=user_id)

@router.get("/employment-types", response_model=List[str])
def get_employment_types() -> Any:
    """
    Get all available employment types.
    """
    return [e.value for e in EmploymentType]

@router.get("/work-schedules", response_model=List[str])
def get_work_schedules() -> Any:
    """
    Get all available work schedules.
    """
    return [w.value for w in WorkSchedule]

@router.get("/preferred-employment", response_model=List[UserSchema])
def get_users_by_employment_preference(
    employment_type: EmploymentType,
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get users who prefer a specific employment type.
    """
    response = (
        db.table("users")
        .select("*")
        .contains("employment_preferences->preferred_employment_types", [employment_type])
        .order("created_at", desc=True)
        .range(skip, skip + limit - 1)
        .execute()
    )
    return [User(**item) for item in response.data]

@router.get("/preferred-schedule", response_model=List[UserSchema])
def get_users_by_work_schedule(
    work_schedule: WorkSchedule,
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get users who prefer a specific work schedule.
    """
    response = (
        db.table("users")
        .select("*")
        .contains("employment_preferences->preferred_work_schedule", [work_schedule])
        .order("created_at", desc=True)
        .range(skip, skip + limit - 1)
        .execute()
    )
    return [User(**item) for item in response.data]

@router.put("/me/employment-preferences", response_model=UserSchema)
def update_employment_preferences(
    *,
    db: Client = Depends(get_db),
    preferences: EmploymentPreferences,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update user's employment preferences.
    """
    update_data = {"employment_preferences": preferences.model_dump()}
    return crud_user.update(db, db_obj=current_user, obj_in=update_data)

@router.get("/me/employment-preferences", response_model=EmploymentPreferences)
def get_employment_preferences(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user's employment preferences.
    """
    return current_user.employment_preferences

@router.get("/search/employment", response_model=List[UserSchema])
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
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Search users by employment criteria.
    """
    query = db.table("users").select("*")
    
    if employment_type:
        query = query.contains("employment_preferences->preferred_employment_types", [employment_type])
    
    if work_schedule:
        query = query.contains("employment_preferences->preferred_work_schedule", [work_schedule])
    
    if company_size:
        query = query.contains("employment_preferences->preferred_company_size", [company_size])
    
    if min_salary is not None:
        query = query.gte("employment_preferences->preferred_salary_range->min", min_salary)
    
    if max_salary is not None:
        query = query.lte("employment_preferences->preferred_salary_range->max", max_salary)
    
    if currency:
        query = query.eq("employment_preferences->preferred_currency", currency)
    
    if remote_percentage is not None:
        query = query.eq("employment_preferences->preferred_remote_percentage", remote_percentage)
    
    if benefits:
        query = query.contains("employment_preferences->preferred_benefits", benefits)
    
    if location:
        query = query.ilike("location", f"%{location}%")
    
    response = query.order("created_at", desc=True).range(skip, skip + limit - 1).execute()
    return [User(**item) for item in response.data]

@router.get("/search/salary-range", response_model=List[UserSchema])
def search_users_by_salary_range(
    min_salary: float,
    max_salary: float,
    currency: str = Query(..., pattern="^[A-Z]{3}$"),
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Search users by salary range.
    """
    response = (
        db.table("users")
        .select("*")
        .gte("employment_preferences->preferred_salary_range->min", min_salary)
        .lte("employment_preferences->preferred_salary_range->max", max_salary)
        .eq("employment_preferences->preferred_currency", currency)
        .order("created_at", desc=True)
        .range(skip, skip + limit - 1)
        .execute()
    )
    return [User(**item) for item in response.data]

@router.get("/search/benefits", response_model=List[UserSchema])
def search_users_by_benefits(
    benefits: List[BenefitType],
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Search users by preferred benefits.
    """
    response = (
        db.table("users")
        .select("*")
        .contains("employment_preferences->preferred_benefits", benefits)
        .order("created_at", desc=True)
        .range(skip, skip + limit - 1)
        .execute()
    )
    return [User(**item) for item in response.data]

@router.get("/search/location", response_model=List[UserSchema])
def search_users_by_location(
    location: str,
    max_distance: Optional[int] = Query(None, ge=0, le=500),
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Search users by location and optional maximum distance.
    """
    query = (
        db.table("users")
        .select("*")
        .ilike("location", f"%{location}%")
    )
    
    if max_distance is not None:
        query = query.lte("employment_preferences->preferred_commute_distance", max_distance)
    
    response = query.order("created_at", desc=True).range(skip, skip + limit - 1).execute()
    return [User(**item) for item in response.data]

@router.get("/search/work-environment", response_model=List[UserSchema])
def search_users_by_work_environment(
    environment: str,
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Search users by preferred work environment.
    """
    response = (
        db.table("users")
        .select("*")
        .contains("employment_preferences->preferred_work_environment", [environment])
        .order("created_at", desc=True)
        .range(skip, skip + limit - 1)
        .execute()
    )
    return [User(**item) for item in response.data]

@router.get("/analytics/employment-preferences", response_model=Dict[str, Any])
def get_employment_preferences_analytics(
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get analytics about employment preferences.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions",
        )
    
    # Get all users
    response = db.table("users").select("employment_preferences").execute()
    users = response.data
    
    # Initialize counters
    employment_types = {}
    work_schedules = {}
    company_sizes = {}
    benefits = {}
    remote_percentages = {}
    salary_ranges = {}
    
    # Count preferences
    for user in users:
        prefs = user.get("employment_preferences", {})
        
        # Employment types
        for emp_type in prefs.get("preferred_employment_types", []):
            employment_types[emp_type] = employment_types.get(emp_type, 0) + 1
        
        # Work schedules
        for schedule in prefs.get("preferred_work_schedule", []):
            work_schedules[schedule] = work_schedules.get(schedule, 0) + 1
        
        # Company sizes
        for size in prefs.get("preferred_company_size", []):
            company_sizes[size] = company_sizes.get(size, 0) + 1
        
        # Benefits
        for benefit in prefs.get("preferred_benefits", []):
            benefits[benefit] = benefits.get(benefit, 0) + 1
        
        # Remote percentages
        remote_pct = prefs.get("preferred_remote_percentage")
        if remote_pct is not None:
            remote_percentages[remote_pct] = remote_percentages.get(remote_pct, 0) + 1
        
        # Salary ranges
        salary_range = prefs.get("preferred_salary_range")
        if salary_range:
            min_salary = salary_range.get("min")
            max_salary = salary_range.get("max")
            if min_salary is not None and max_salary is not None:
                range_key = f"{min_salary}-{max_salary}"
                salary_ranges[range_key] = salary_ranges.get(range_key, 0) + 1
    
    return {
        "employment_types": employment_types,
        "work_schedules": work_schedules,
        "company_sizes": company_sizes,
        "benefits": benefits,
        "remote_percentages": remote_percentages,
        "salary_ranges": salary_ranges,
        "total_users": len(users)
    }

@router.get("/me/profile-score", response_model=ProfileScore)
def get_profile_score(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user's profile completion score and recommendations.
    """
    return ProfileService.calculate_profile_score(current_user)

@router.get("/me/skill-ratings", response_model=List[SkillRating])
def get_skill_ratings(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user's skill ratings based on work experience.
    """
    return [
        ProfileService.calculate_skill_rating(skill, current_user.work_experience)
        for skill in current_user.skills
    ]

@router.post("/me/skills/{skill}/endorse", response_model=SkillEndorsement)
def endorse_skill(
    skill: str,
    comment: Optional[str] = None,
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    endorser: User = Depends(get_current_active_user),
) -> Any:
    """
    Endorse a user's skill.
    """
    if skill not in current_user.skills:
        raise HTTPException(
            status_code=400,
            detail="Skill not found in user's profile",
        )
    
    endorsement = ProfileService.create_skill_endorsement(
        skill=skill,
        endorser_id=endorser.id,
        endorser_name=f"{endorser.first_name} {endorser.last_name}",
        comment=comment
    )
    
    # Update user's skill endorsements in database
    # Implementation depends on your database structure
    
    return endorsement

@router.get("/me/verification", response_model=ProfileVerification)
def get_profile_verification(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user's profile verification status.
    """
    # Implementation depends on your database structure
    return ProfileVerification()

@router.get("/me/analytics", response_model=ProfileAnalytics)
def get_profile_analytics(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user's profile analytics.
    """
    # Implementation depends on your database structure
    return ProfileAnalytics()

@router.post("/search", response_model=SearchResult)
def search_users(
    criteria: SearchCriteria,
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Advanced search for users with multiple criteria.
    """
    # Build and execute search query
    query = SearchService.build_search_query(db, criteria)
    response = query.range(
        (criteria.page - 1) * criteria.per_page,
        criteria.page * criteria.per_page - 1
    ).execute()
    
    # Get total count
    count_response = db.table("users").select("id", count="exact").execute()
    total_count = count_response.count
    
    # Calculate match scores
    results = []
    for user_data in response.data:
        user = User(**user_data)
        match_score = SearchService.calculate_match_score(user, criteria)
        results.append({
            **user_data,
            "match_score": match_score
        })
    
    # Sort by match score if no specific sort criteria
    if not criteria.sort_by:
        results.sort(key=lambda x: x["match_score"], reverse=True)
    
    return SearchResult(
        total_count=total_count,
        page=criteria.page,
        per_page=criteria.per_page,
        total_pages=(total_count + criteria.per_page - 1) // criteria.per_page,
        results=results,
        facets=SearchService.get_search_facets(db)
    )

@router.get("/search/suggestions", response_model=List[str])
def get_search_suggestions(
    query: str = Query(..., min_length=2),
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get search suggestions based on partial query.
    """
    return SearchService.get_search_suggestions(db, query)

@router.get("/search/facets", response_model=Dict[str, Any])
def get_search_facets(
    db: Client = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get search facets for filtering.
    """
    return SearchService.get_search_facets(db) 