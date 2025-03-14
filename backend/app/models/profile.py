from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base
import uuid

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), unique=True)
    avatar_url = Column(String)
    bio = Column(Text)
    phone_number = Column(String(20))
    location = Column(String(100))
    skills = Column(JSON)  # List of skills
    experience = Column(JSON)  # List of work experiences
    education = Column(JSON)  # List of education details
    resume_url = Column(String)  # URL to stored resume
    linkedin_url = Column(String)
    github_url = Column(String)
    portfolio_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # For employers
    company_name = Column(String(100))
    company_website = Column(String)
    company_description = Column(Text)
    industry = Column(String(50))
    company_size = Column(String(20))

    # Relationships
    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<Profile {self.user_id}>" 