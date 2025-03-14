from fastapi import APIRouter

from app.api.v1.endpoints import (
    applications,
    auth,
    companies,
    dashboard,
    jobs,
    notifications,
    payments,
    search,
    users,
    verification,
    skills,
    benefits,
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
api_router.include_router(companies.router, prefix="/companies", tags=["Companies"])
api_router.include_router(
    applications.router, prefix="/applications", tags=["Applications"]
)
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(payments.router, prefix="/payments", tags=["Payments"])
api_router.include_router(
    notifications.router, prefix="/notifications", tags=["Notifications"]
)
api_router.include_router(
    verification.router, prefix="/verification", tags=["Verification"]
)
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(skills.router, prefix="/skills", tags=["Skills"])
api_router.include_router(benefits.router, prefix="/benefits", tags=["Benefits"])
