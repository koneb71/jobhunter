from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.base_class import Base

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(500), nullable=True)
    category = Column(String(50), nullable=True)  # e.g., "Technical", "Soft Skills", "Tools"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Skill {self.name}>" 