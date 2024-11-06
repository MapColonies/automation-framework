import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
if not os.path.exists('../logs'):
    os.makedirs('../logs')

# Set up logging configuration
LOG_FILE = f"../logs/automation_{datetime.now().strftime('%Y-%m-%d')}.log"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)


def get_logger(name):
    """
    Get a logger instance with the specified name.

    :param name: Name of the logger
    :return: Configured logger instance
    """
    return logging.getLogger(name)
