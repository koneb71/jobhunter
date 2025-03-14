from typing import Dict, List
from sqlalchemy.orm import Session
from app import crud, schemas

# Technical Skills
TECHNICAL_SKILLS = [
    {
        "name": "Python",
        "description": "Python programming language",
        "category": "Programming Languages"
    },
    {
        "name": "JavaScript",
        "description": "JavaScript programming language",
        "category": "Programming Languages"
    },
    {
        "name": "TypeScript",
        "description": "TypeScript programming language",
        "category": "Programming Languages"
    },
    {
        "name": "Java",
        "description": "Java programming language",
        "category": "Programming Languages"
    },
    {
        "name": "C++",
        "description": "C++ programming language",
        "category": "Programming Languages"
    },
    {
        "name": "React",
        "description": "React.js frontend framework",
        "category": "Frontend"
    },
    {
        "name": "Angular",
        "description": "Angular frontend framework",
        "category": "Frontend"
    },
    {
        "name": "Vue.js",
        "description": "Vue.js frontend framework",
        "category": "Frontend"
    },
    {
        "name": "Node.js",
        "description": "Node.js runtime environment",
        "category": "Backend"
    },
    {
        "name": "Django",
        "description": "Django web framework",
        "category": "Backend"
    },
    {
        "name": "FastAPI",
        "description": "FastAPI web framework",
        "category": "Backend"
    },
    {
        "name": "PostgreSQL",
        "description": "PostgreSQL database",
        "category": "Databases"
    },
    {
        "name": "MongoDB",
        "description": "MongoDB database",
        "category": "Databases"
    },
    {
        "name": "Redis",
        "description": "Redis in-memory data store",
        "category": "Databases"
    },
    {
        "name": "Docker",
        "description": "Docker containerization",
        "category": "DevOps"
    },
    {
        "name": "Kubernetes",
        "description": "Kubernetes container orchestration",
        "category": "DevOps"
    },
    {
        "name": "AWS",
        "description": "Amazon Web Services",
        "category": "Cloud"
    },
    {
        "name": "Azure",
        "description": "Microsoft Azure",
        "category": "Cloud"
    },
    {
        "name": "GCP",
        "description": "Google Cloud Platform",
        "category": "Cloud"
    }
]

# Soft Skills
SOFT_SKILLS = [
    {
        "name": "Communication",
        "description": "Effective verbal and written communication",
        "category": "Soft Skills"
    },
    {
        "name": "Leadership",
        "description": "Team leadership and management",
        "category": "Soft Skills"
    },
    {
        "name": "Problem Solving",
        "description": "Analytical and creative problem solving",
        "category": "Soft Skills"
    },
    {
        "name": "Teamwork",
        "description": "Collaboration and team player mentality",
        "category": "Soft Skills"
    },
    {
        "name": "Time Management",
        "description": "Efficient time and task management",
        "category": "Soft Skills"
    }
]

# Benefits
BENEFITS = [
    # Health Benefits
    {
        "name": "Health Insurance",
        "description": "Comprehensive medical, dental, and vision coverage",
        "category": "Health"
    },
    {
        "name": "Life Insurance",
        "description": "Company-provided life insurance coverage",
        "category": "Health"
    },
    {
        "name": "Mental Health Support",
        "description": "Access to mental health resources and counseling",
        "category": "Health"
    },
    {
        "name": "Wellness Program",
        "description": "Fitness reimbursement and wellness initiatives",
        "category": "Health"
    },
    
    # Financial Benefits
    {
        "name": "401(k) Plan",
        "description": "Retirement savings plan with company match",
        "category": "Financial"
    },
    {
        "name": "Stock Options",
        "description": "Employee stock ownership opportunities",
        "category": "Financial"
    },
    {
        "name": "Performance Bonus",
        "description": "Annual performance-based bonus",
        "category": "Financial"
    },
    {
        "name": "Profit Sharing",
        "description": "Company profit sharing program",
        "category": "Financial"
    },
    
    # Work-Life Balance
    {
        "name": "Flexible Hours",
        "description": "Flexible working hours and schedules",
        "category": "Work-Life Balance"
    },
    {
        "name": "Remote Work",
        "description": "Option to work remotely",
        "category": "Work-Life Balance"
    },
    {
        "name": "Unlimited PTO",
        "description": "Unlimited paid time off policy",
        "category": "Work-Life Balance"
    },
    {
        "name": "Paid Parental Leave",
        "description": "Paid leave for new parents",
        "category": "Work-Life Balance"
    },
    
    # Professional Development
    {
        "name": "Training Budget",
        "description": "Annual budget for professional development",
        "category": "Professional Development"
    },
    {
        "name": "Conference Attendance",
        "description": "Sponsored attendance at industry conferences",
        "category": "Professional Development"
    },
    {
        "name": "Education Reimbursement",
        "description": "Tuition reimbursement for relevant education",
        "category": "Professional Development"
    },
    
    # Office Perks
    {
        "name": "Free Meals",
        "description": "Free meals and snacks at the office",
        "category": "Office Perks"
    },
    {
        "name": "Transportation Benefits",
        "description": "Commuter benefits or parking allowance",
        "category": "Office Perks"
    },
    {
        "name": "Equipment Allowance",
        "description": "Budget for home office or work equipment",
        "category": "Office Perks"
    }
]

def init_skills(db: Session) -> None:
    """Initialize skills data."""
    for skill_data in TECHNICAL_SKILLS + SOFT_SKILLS:
        skill = crud.skill.get_by_name(db, name=skill_data["name"])
        if not skill:
            skill_in = schemas.SkillCreate(**skill_data)
            crud.skill.create(db, obj_in=skill_in)

def init_benefits(db: Session) -> None:
    """Initialize benefits data."""
    for benefit_data in BENEFITS:
        benefit = crud.benefit.get_by_name(db, name=benefit_data["name"])
        if not benefit:
            benefit_in = schemas.BenefitCreate(**benefit_data)
            crud.benefit.create(db, obj_in=benefit_in)

def init_db(db: Session) -> None:
    """Initialize database with seed data."""
    init_skills(db)
    init_benefits(db)