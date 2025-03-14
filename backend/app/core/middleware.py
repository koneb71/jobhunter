import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.app = app

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log request
        logger.info(f"Request: {request.method} {request.url.path}")

        # Process request
        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time

        # Log response
        logger.info(
            f"Response: {response.status_code} - " f"Processed in {process_time:.2f}s"
        )

        return response
