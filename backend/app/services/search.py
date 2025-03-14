from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc, func, text

from app.crud import crud_job, crud_company
from app.models.job import Job
from app.models.company import Company
from app.models.user import User
from app.schemas.search import (
    SearchParams, SearchResponse, PaginationInfo,
    JobType, ExperienceLevel, SortBy, SortOrder
)
from app.schemas.profile import SearchCriteria, SearchResult

class SearchService:
    def __init__(self):
        self.start_time = None

    def _start_timer(self):
        self.start_time = datetime.now()

    def _get_elapsed_time(self) -> float:
        if not self.start_time:
            return 0.0
        return (datetime.now() - self.start_time).total_seconds() * 1000

    def _apply_job_filters(self, query, params: SearchParams):
        """Apply filters to job query"""
        if params.query:
            query = query.filter(
                or_(
                    Job.title.ilike(f"%{params.query}%"),
                    Job.description.ilike(f"%{params.query}%")
                )
            )
        
        if params.job_type:
            query = query.filter(Job.job_type == params.job_type)
        
        if params.experience_level:
            query = query.filter(Job.experience_level == params.experience_level)
        
        if params.location:
            query = query.filter(Job.location.ilike(f"%{params.location}%"))
        
        if params.industry:
            query = query.join(Company).filter(Company.industry == params.industry)
        
        if params.salary_min is not None:
            query = query.filter(Job.salary_min >= params.salary_min)
        
        if params.salary_max is not None:
            query = query.filter(Job.salary_max <= params.salary_max)
        
        if params.remote_only:
            query = query.filter(Job.is_remote == True)
        
        if params.posted_within_days:
            cutoff_date = datetime.now() - timedelta(days=params.posted_within_days)
            query = query.filter(Job.created_at >= cutoff_date)
        
        if params.company_size:
            query = query.join(Company).filter(Company.size == params.company_size)

        return query

    def _apply_company_filters(self, query, params: SearchParams):
        """Apply filters to company query"""
        if params.query:
            query = query.filter(
                or_(
                    Company.name.ilike(f"%{params.query}%"),
                    Company.description.ilike(f"%{params.query}%")
                )
            )
        
        if params.industry:
            query = query.filter(Company.industry == params.industry)
        
        if params.location:
            query = query.filter(Company.location.ilike(f"%{params.location}%"))
        
        if params.company_size:
            query = query.filter(Company.size == params.company_size)

        return query

    def _apply_sorting(self, query, params: SearchParams):
        """Apply sorting to query"""
        if params.sort_by == SortBy.DATE:
            query = query.order_by(desc(Job.created_at) if params.sort_order == SortOrder.DESC else Job.created_at)
        elif params.sort_by == SortBy.SALARY:
            query = query.order_by(desc(Job.salary_min) if params.sort_order == SortOrder.DESC else Job.salary_min)
        elif params.sort_by == SortBy.TITLE:
            query = query.order_by(desc(Job.title) if params.sort_order == SortOrder.DESC else Job.title)
        elif params.sort_by == SortBy.COMPANY:
            query = query.join(Company).order_by(desc(Company.name) if params.sort_order == SortOrder.DESC else Company.name)
        else:  # relevance
            query = query.order_by(desc(Job.created_at))
        
        return query

    def _get_pagination_info(self, total_items: int, page: int, page_size: int) -> PaginationInfo:
        """Calculate pagination information"""
        total_pages = (total_items + page_size - 1) // page_size
        return PaginationInfo(
            current_page=page,
            total_pages=total_pages,
            total_items=total_items,
            has_next=page < total_pages,
            has_previous=page > 1,
            page_size=page_size
        )

    def search(self, db: Session, params: SearchParams) -> SearchResponse:
        """
        Perform a unified search across jobs and companies with pagination and advanced filtering.
        """
        self._start_timer()
        
        # Calculate pagination offsets
        skip = (params.page - 1) * params.page_size
        
        # Build and execute job search query
        job_query = db.query(Job).join(Company)
        job_query = self._apply_job_filters(job_query, params)
        job_query = self._apply_sorting(job_query, params)
        
        # Get total count for pagination
        total_jobs = job_query.count()
        
        # Apply pagination
        jobs = job_query.offset(skip).limit(params.page_size).all()
        
        # Build and execute company search query
        company_query = db.query(Company)
        company_query = self._apply_company_filters(company_query, params)
        
        # Get total count for pagination
        total_companies = company_query.count()
        
        # Apply pagination
        companies = company_query.offset(skip).limit(params.page_size).all()

        # Calculate pagination info
        pagination = self._get_pagination_info(
            total_items=max(total_jobs, total_companies),
            page=params.page,
            page_size=params.page_size
        )

        # Prepare active filters for response
        active_filters = {
            "job_type": params.job_type,
            "experience_level": params.experience_level,
            "location": params.location,
            "industry": params.industry,
            "salary_range": {
                "min": params.salary_min,
                "max": params.salary_max
            } if params.salary_min or params.salary_max else None,
            "remote_only": params.remote_only,
            "posted_within_days": params.posted_within_days,
            "company_size": params.company_size
        }

        return SearchResponse(
            jobs=jobs,
            companies=companies,
            pagination=pagination,
            took_ms=self._get_elapsed_time(),
            filters=active_filters
        )

    @staticmethod
    def build_search_query(db: Session, criteria: SearchCriteria) -> Any:
        """Build search query based on criteria."""
        query = db.query(User)

        # Skills search
        if criteria.skills:
            for skill in criteria.skills:
                query = query.filter(User.skills.contains([skill]))

        # Experience years
        if criteria.experience_years:
            query = query.filter(User.work_experience["years_of_experience"].astext.cast(int) >= criteria.experience_years)

        # Education level
        if criteria.education_level:
            query = query.filter(User.education["degree"].contains([criteria.education_level]))

        # Location
        if criteria.location:
            query = query.filter(User.location.ilike(f"%{criteria.location}%"))

        # Employment preferences
        if criteria.employment_type:
            query = query.filter(User.employment_preferences["preferred_employment_types"].contains([criteria.employment_type]))

        if criteria.work_schedule:
            query = query.filter(User.employment_preferences["preferred_work_schedule"].contains([criteria.work_schedule]))

        if criteria.company_size:
            query = query.filter(User.employment_preferences["preferred_company_size"].contains([criteria.company_size]))

        if criteria.benefits:
            query = query.filter(User.employment_preferences["preferred_benefits"].contains([criteria.benefits]))

        # Salary range
        if criteria.salary_range:
            if "min" in criteria.salary_range:
                query = query.filter(User.employment_preferences["preferred_salary_range"]["min"].astext.cast(int) >= criteria.salary_range["min"])
            if "max" in criteria.salary_range:
                query = query.filter(User.employment_preferences["preferred_salary_range"]["max"].astext.cast(int) <= criteria.salary_range["max"])

        # Availability
        if criteria.availability:
            query = query.filter(User.availability_status == criteria.availability)

        # Languages
        if criteria.languages:
            for language in criteria.languages:
                query = query.filter(User.languages.contains([{"language": language}]))

        # Certifications
        if criteria.certifications:
            for cert in criteria.certifications:
                query = query.filter(User.certifications.contains([{"name": cert}]))

        # Keywords search
        if criteria.keywords:
            keyword_conditions = []
            for keyword in criteria.keywords.split():
                keyword_conditions.extend([
                    User.tagline.ilike(f"%{keyword}%"),
                    User.profile_overview.ilike(f"%{keyword}%"),
                    User.work_experience["description"].astext.ilike(f"%{keyword}%"),
                    User.education["description"].astext.ilike(f"%{keyword}%")
                ])
            query = query.filter(or_(*keyword_conditions))

        # Sorting
        if criteria.sort_by:
            sort_order = desc if criteria.sort_order == "desc" else None
            if sort_order:
                query = query.order_by(sort_order(getattr(User, criteria.sort_by)))
            else:
                query = query.order_by(getattr(User, criteria.sort_by))

        return query

    @staticmethod
    def calculate_match_score(user: User, criteria: SearchCriteria) -> float:
        """Calculate match score between user and search criteria."""
        score = 0.0
        total_weights = 0

        # Skills match (weight: 30)
        if criteria.skills and user.skills:
            matching_skills = set(criteria.skills) & set(user.skills)
            if matching_skills:
                score += 30 * (len(matching_skills) / len(criteria.skills))
            total_weights += 30

        # Experience match (weight: 20)
        if criteria.experience_years:
            total_years = sum(
                (datetime.fromisoformat(exp["end_date"]) - datetime.fromisoformat(exp["start_date"])).days / 365.25
                for exp in user.work_experience
                if exp.get("end_date")
            )
            if total_years >= criteria.experience_years:
                score += 20
            total_weights += 20

        # Location match (weight: 15)
        if criteria.location and user.location:
            if criteria.location.lower() in user.location.lower():
                score += 15
            total_weights += 15

        # Employment preferences match (weight: 15)
        if criteria.employment_type and user.employment_preferences.preferred_employment_types:
            matching_types = set(criteria.employment_type) & set(user.employment_preferences.preferred_employment_types)
            if matching_types:
                score += 15 * (len(matching_types) / len(criteria.employment_type))
            total_weights += 15

        # Education match (weight: 10)
        if criteria.education_level and user.education:
            matching_education = any(
                criteria.education_level.lower() in edu["degree"].lower()
                for edu in user.education
            )
            if matching_education:
                score += 10
            total_weights += 10

        # Languages match (weight: 10)
        if criteria.languages and user.languages:
            matching_languages = set(criteria.languages) & {lang["language"] for lang in user.languages}
            if matching_languages:
                score += 10 * (len(matching_languages) / len(criteria.languages))
            total_weights += 10

        return score / total_weights if total_weights > 0 else 0

    @staticmethod
    def get_search_suggestions(db, query: str) -> List[str]:
        """Get search suggestions based on partial query."""
        if not query or len(query) < 2:
            return []

        # Get suggestions from various fields
        suggestions = set()

        # Skills suggestions
        skills_response = (
            db.query(User.skills)
            .execute()
        )
        for user in skills_response.scalars():
            if user:
                for skill in user:
                    if query.lower() in skill.lower():
                        suggestions.add(skill)

        # Location suggestions
        locations_response = (
            db.query(User.location)
            .execute()
        )
        for user in locations_response.scalars():
            if user and query.lower() in user.lower():
                suggestions.add(user)

        # Education suggestions
        education_response = (
            db.query(User.education)
            .execute()
        )
        for user in education_response.scalars():
            if user:
                for edu in user:
                    if query.lower() in edu.get("degree", "").lower():
                        suggestions.add(edu["degree"])

        return sorted(list(suggestions))[:5]  # Return top 5 suggestions

    @staticmethod
    def get_search_facets(db) -> Dict[str, Any]:
        """Get search facets for filtering."""
        facets = {
            "skills": {},
            "locations": {},
            "education_levels": {},
            "employment_types": {},
            "work_schedules": {},
            "company_sizes": {},
            "benefits": {}
        }

        # Get all users
        response = db.query(User).execute()
        users = response.scalars()

        for user in users:
            # Count skills
            if user.skills:
                for skill in user.skills:
                    facets["skills"][skill] = facets["skills"].get(skill, 0) + 1

            # Count locations
            if user.location:
                facets["locations"][user.location] = facets["locations"].get(user.location, 0) + 1

            # Count education levels
            if user.education:
                for edu in user.education:
                    if edu.get("degree"):
                        facets["education_levels"][edu["degree"]] = facets["education_levels"].get(edu["degree"], 0) + 1

            # Count employment preferences
            prefs = user.employment_preferences
            if prefs.preferred_employment_types:
                for emp_type in prefs.preferred_employment_types:
                    facets["employment_types"][emp_type] = facets["employment_types"].get(emp_type, 0) + 1

            if prefs.preferred_work_schedule:
                for schedule in prefs.preferred_work_schedule:
                    facets["work_schedules"][schedule] = facets["work_schedules"].get(schedule, 0) + 1

            if prefs.preferred_company_size:
                for size in prefs.preferred_company_size:
                    facets["company_sizes"][size] = facets["company_sizes"].get(size, 0) + 1

            if prefs.preferred_benefits:
                for benefit in prefs.preferred_benefits:
                    facets["benefits"][benefit] = facets["benefits"].get(benefit, 0) + 1

        return facets

search_service = SearchService() 