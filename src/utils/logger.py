import logging
import os
from datetime import datetime

# Define the root of the project and log directory explicitly
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)  # Moving up to the project root
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Create logs directory if it doesn't exist
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Set up log file path
LOG_FILE: str = os.path.join(
    LOG_DIR, f"automation_{datetime.now().strftime('%Y-%m-%d')}.log"
)

# Print log path for debugging purposes
print(f"Log file path: {LOG_FILE}")  # Debugging: Check if the path is correct

# Set up logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a"),  # 'a' for append mode
        logging.StreamHandler(),
    ],
)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.

    :param name: Name of the logger
    :return: Configured logger instance
    """
    return logging.getLogger(name)
