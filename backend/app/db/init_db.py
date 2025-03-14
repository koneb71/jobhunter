import logging

from sqlalchemy.orm import Session

from app.core.password import get_password_hash
from app.db.base_class import Base
from app.db.session import engine
from app.models import Job, JobApplication, Profile, User, UserType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    # Create tables
    Base.metadata.create_all(bind=engine)
    logger.info("Created database tables")

    # Check if we already have users
    user = db.query(User).first()
    if user:
        logger.info("Database already initialized")
        return

    users_data = [
        {
            "email": "admin@example.com",
            "full_name": "John Doe",
            "password": "admin123",
            "user_type": UserType.ADMIN,
            "is_superuser": True,
        },
        {
            "email": "employer@example.com",
            "full_name": "Jane Smith",
            "password": "employer123",
            "user_type": UserType.EMPLOYER,
        },
    ]

    for user_data in users_data:
        db_obj = User(
            email=user_data["email"],
            full_name=user_data["full_name"],
            hashed_password=get_password_hash(user_data["password"]),
            user_type=user_data["user_type"],
            is_superuser=user_data.get("is_superuser", False),
        )
        db.add(db_obj)

    db.commit()
    logger.info("Database initialized")


if __name__ == "__main__":
    from app.db.session import SessionLocal

    db = SessionLocal()
    init_db(db)
