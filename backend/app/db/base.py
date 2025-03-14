# Import all the models, so that Base has them before being imported by Alembic
from app.db.base_class import Base
from app.models.user import User
from app.models.profile import Profile
from app.models.job import Job
from app.models.job_application import JobApplication
from app.models.notification import Notification
from app.models.verification_request import VerificationRequest
from app.models.payment import Payment
from app.models.interview import Interview 