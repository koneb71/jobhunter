from typing import Generator
from supabase import create_client, Client
from app.core.config import settings

def get_supabase() -> Client:
    """
    Get Supabase client instance.
    """
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def get_db() -> Generator[Client, None, None]:
    """
    Get database session.
    """
    try:
        db = get_supabase()
        yield db
    finally:
        # Clean up if needed
        pass 