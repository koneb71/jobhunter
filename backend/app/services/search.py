from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime, timedelta
from supabase import Client

from app.crud import crud_job, crud_company
from app.schemas.search import (
    SearchParams, SearchResponse, PaginationInfo,
    JobType, ExperienceLevel, SortBy, SortOrder
)
from app.schemas.profile import SearchCriteria, SearchResult
from app.schemas.user import User

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
            query = query.or_(
                f"title.ilike.%{params.query}%,description.ilike.%{params.query}%"
            )
        
        if params.job_type:
            query = query.eq("job_type", params.job_type)
        
        if params.experience_level:
            query = query.eq("experience_level", params.experience_level)
        
        if params.location:
            query = query.ilike("location", f"%{params.location}%")
        
        if params.industry:
            query = query.eq("companies.industry", params.industry)
        
        if params.salary_min is not None:
            query = query.gte("salary_min", params.salary_min)
        
        if params.salary_max is not None:
            query = query.lte("salary_max", params.salary_max)
        
        if params.remote_only:
            query = query.eq("is_remote", True)
        
        if params.posted_within_days:
            cutoff_date = datetime.now() - timedelta(days=params.posted_within_days)
            query = query.gte("created_at", cutoff_date.isoformat())
        
        if params.company_size:
            query = query.eq("companies.size", params.company_size)

        return query

    def _apply_company_filters(self, query, params: SearchParams):
        """Apply filters to company query"""
        if params.query:
            query = query.or_(
                f"name.ilike.%{params.query}%,description.ilike.%{params.query}%"
            )
        
        if params.industry:
            query = query.eq("industry", params.industry)
        
        if params.location:
            query = query.ilike("location", f"%{params.location}%")
        
        if params.company_size:
            query = query.eq("size", params.company_size)

        return query

    def _apply_sorting(self, query, params: SearchParams):
        """Apply sorting to query"""
        if params.sort_by == SortBy.DATE:
            query = query.order("created_at", desc=(params.sort_order == SortOrder.DESC))
        elif params.sort_by == SortBy.SALARY:
            query = query.order("salary_min", desc=(params.sort_order == SortOrder.DESC))
        elif params.sort_by == SortBy.TITLE:
            query = query.order("title", desc=(params.sort_order == SortOrder.DESC))
        elif params.sort_by == SortBy.COMPANY:
            query = query.order("companies.name", desc=(params.sort_order == SortOrder.DESC))
        else:  # relevance
            query = query.order("created_at", desc=True)
        
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

    def search(self, db: Client, params: SearchParams) -> SearchResponse:
        """
        Perform a unified search across jobs and companies with pagination and advanced filtering.
        """
        self._start_timer()
        
        # Calculate pagination offsets
        skip = (params.page - 1) * params.page_size
        
        # Build and execute job search query
        job_query = db.table("jobs").select("*, companies(*)")
        job_query = self._apply_job_filters(job_query, params)
        job_query = self._apply_sorting(job_query, params)
        
        # Get total count for pagination
        count_query = job_query.count()
        total_jobs = count_query.execute().count
        
        # Apply pagination
        job_query = job_query.range(skip, skip + params.page_size - 1)
        jobs_response = job_query.execute()
        
        # Process job results
        jobs = []
        for job_data in jobs_response.data:
            job_data["company"] = job_data.pop("companies")
            jobs.append(job_data)

        # Build and execute company search query
        company_query = db.table("companies").select("*")
        company_query = self._apply_company_filters(company_query, params)
        
        # Get total count for pagination
        count_query = company_query.count()
        total_companies = count_query.execute().count
        
        # Apply pagination
        company_query = company_query.range(skip, skip + params.page_size - 1)
        companies_response = company_query.execute()

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
            companies=companies_response.data,
            pagination=pagination,
            took_ms=self._get_elapsed_time(),
            filters=active_filters
        )

    @staticmethod
    def build_search_query(db, criteria: SearchCriteria) -> Any:
        """Build search query based on criteria."""
        query = db.table("users").select("*")

        # Skills search
        if criteria.skills:
            for skill in criteria.skills:
                query = query.contains("skills", [skill])

        # Experience years
        if criteria.experience_years:
            query = query.gte("work_experience->years_of_experience", criteria.experience_years)

        # Education level
        if criteria.education_level:
            query = query.contains("education->degree", [criteria.education_level])

        # Location
        if criteria.location:
            query = query.ilike("location", f"%{criteria.location}%")

        # Employment preferences
        if criteria.employment_type:
            query = query.contains("employment_preferences->preferred_employment_types", criteria.employment_type)

        if criteria.work_schedule:
            query = query.contains("employment_preferences->preferred_work_schedule", criteria.work_schedule)

        if criteria.company_size:
            query = query.contains("employment_preferences->preferred_company_size", criteria.company_size)

        if criteria.benefits:
            query = query.contains("employment_preferences->preferred_benefits", criteria.benefits)

        # Salary range
        if criteria.salary_range:
            if "min" in criteria.salary_range:
                query = query.gte("employment_preferences->preferred_salary_range->min", criteria.salary_range["min"])
            if "max" in criteria.salary_range:
                query = query.lte("employment_preferences->preferred_salary_range->max", criteria.salary_range["max"])

        # Availability
        if criteria.availability:
            query = query.eq("availability_status", criteria.availability)

        # Languages
        if criteria.languages:
            for language in criteria.languages:
                query = query.contains("languages", [{"language": language}])

        # Certifications
        if criteria.certifications:
            for cert in criteria.certifications:
                query = query.contains("certifications", [{"name": cert}])

        # Keywords search
        if criteria.keywords:
            keyword_conditions = []
            for keyword in criteria.keywords.split():
                keyword_conditions.extend([
                    f"tagline.ilike.%{keyword}%",
                    f"profile_overview.ilike.%{keyword}%",
                    f"work_experience->description.ilike.%{keyword}%",
                    f"education->description.ilike.%{keyword}%"
                ])
            query = query.or_(",".join(keyword_conditions))

        # Sorting
        if criteria.sort_by:
            sort_order = "desc" if criteria.sort_order == "desc" else "asc"
            query = query.order(criteria.sort_by, desc=(sort_order == "desc"))

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
            db.table("users")
            .select("skills")
            .execute()
        )
        for user in skills_response.data:
            if user.get("skills"):
                for skill in user["skills"]:
                    if query.lower() in skill.lower():
                        suggestions.add(skill)

        # Location suggestions
        locations_response = (
            db.table("users")
            .select("location")
            .execute()
        )
        for user in locations_response.data:
            if user.get("location") and query.lower() in user["location"].lower():
                suggestions.add(user["location"])

        # Education suggestions
        education_response = (
            db.table("users")
            .select("education")
            .execute()
        )
        for user in education_response.data:
            if user.get("education"):
                for edu in user["education"]:
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
        response = db.table("users").select("*").execute()
        users = response.data

        for user in users:
            # Count skills
            if user.get("skills"):
                for skill in user["skills"]:
                    facets["skills"][skill] = facets["skills"].get(skill, 0) + 1

            # Count locations
            if user.get("location"):
                facets["locations"][user["location"]] = facets["locations"].get(user["location"], 0) + 1

            # Count education levels
            if user.get("education"):
                for edu in user["education"]:
                    if edu.get("degree"):
                        facets["education_levels"][edu["degree"]] = facets["education_levels"].get(edu["degree"], 0) + 1

            # Count employment preferences
            prefs = user.get("employment_preferences", {})
            if prefs.get("preferred_employment_types"):
                for emp_type in prefs["preferred_employment_types"]:
                    facets["employment_types"][emp_type] = facets["employment_types"].get(emp_type, 0) + 1

            if prefs.get("preferred_work_schedule"):
                for schedule in prefs["preferred_work_schedule"]:
                    facets["work_schedules"][schedule] = facets["work_schedules"].get(schedule, 0) + 1

            if prefs.get("preferred_company_size"):
                for size in prefs["preferred_company_size"]:
                    facets["company_sizes"][size] = facets["company_sizes"].get(size, 0) + 1

            if prefs.get("preferred_benefits"):
                for benefit in prefs["preferred_benefits"]:
                    facets["benefits"][benefit] = facets["benefits"].get(benefit, 0) + 1

        return facets

search_service = SearchService() 