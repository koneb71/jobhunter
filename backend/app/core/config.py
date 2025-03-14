from typing import List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator
import os
from pathlib import Path

class Settings(BaseSettings):
    # API Settings
    PROJECT_NAME: str = "JobHunter"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Supabase Configuration
    SUPABASE_URL: str = "your-supabase-url"
    SUPABASE_KEY: str = "your-supabase-key"
    
    # JWT Configuration
    SECRET_KEY: str = "your-secret-key-here"  # Change this in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # File Upload Configuration
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB
    
    # Local Storage Settings
    PROFILE_PICTURES_DIR: str = "profile_pictures"
    VERIFICATION_DOCUMENTS_DIR: str = "verification_documents"
    TEMP_DIR: str = "temp"
    
    # Email settings
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD", "")
    MAIL_FROM: str = os.getenv("MAIL_FROM", "noreply@jobhunter.com")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", "587"))
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME", "JobHunter")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # Create necessary directories
    def create_directories(self):
        """Create necessary directories for file uploads."""
        directories = [
            self.UPLOAD_DIR,
            os.path.join(self.UPLOAD_DIR, self.PROFILE_PICTURES_DIR),
            os.path.join(self.UPLOAD_DIR, self.VERIFICATION_DOCUMENTS_DIR),
            os.path.join(self.UPLOAD_DIR, self.TEMP_DIR)
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    # Get file URL for local storage
    def get_file_url(self, file_path: str) -> str:
        """Get the URL for a locally stored file."""
        return f"/static/{file_path}"

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"  # Allow extra fields in the settings

settings = Settings()
settings.create_directories() 