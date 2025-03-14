import secrets
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, PostgresDsn, validator
from pydantic_settings import BaseSettings
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "JobHunter"
    VERSION: str = "1.0.0"
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
    
    # JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
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
    
    # Database Configuration
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "jobhunter")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
    
    def get_database_url(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Email Configuration
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None

    # AWS Configuration
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET: Optional[str] = None
    
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