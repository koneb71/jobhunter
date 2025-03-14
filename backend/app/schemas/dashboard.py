from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_jobs: int
    active_jobs: int
    total_applications: int
    new_applications: int
    total_candidates: int
    upcoming_interviews: int


class DashboardJob(BaseModel):
    id: str
    title: str
    location: str
    type: str
    posted_date: str
    applications_count: int
    status: str


class DashboardCandidate(BaseModel):
    id: str
    name: str
    position: str
    experience: str
    applied_date: str
    status: str


class ApplicationTrend(BaseModel):
    date: str
    applications: int
    interviews: int
    offers: int


class ApplicationStatusDistribution(BaseModel):
    name: str
    value: int
