import logging
import sys
from pathlib import Path

# Create logs directory if it doesn't exist
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Configure logger
logger = logging.getLogger("jobhunter")
logger.setLevel(logging.INFO)

# Create formatters
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_formatter = logging.Formatter("%(levelname)s: %(message)s")

# File handler
file_handler = logging.FileHandler(filename=logs_dir / "app.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(file_formatter)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(console_formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Prevent duplicate logs
logger.propagate = False

# Export logger
__all__ = ["logger"]
