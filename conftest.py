import pytest
import logging
import os
from datetime import datetime


def pytest_configure(config):
    # Define the log directory relative to the root of the project
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    LOG_DIR = os.path.join(BASE_DIR, "logs")

    # Create logs directory if it doesn't exist
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Set up log file path with dynamic date
    log_file_path = os.path.join(
        LOG_DIR, f"automation_{datetime.now().strftime('%Y-%m-%d')}.log"
    )

    # Set up logging configuration
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file_path, mode="a"),  # Append mode
            logging.StreamHandler(),  # Output to console
        ],
    )

    # Debug statement to confirm log file path
    print(f"Logging to file: {log_file_path}")

    # Configure root logger to ensure all messages are logged
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    for handler in root_logger.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.setLevel(logging.DEBUG)

    # Adding a separate handler to ensure compatibility with pytest's capturing
    if not any(
        isinstance(handler, logging.FileHandler) for handler in root_logger.handlers
    ):
        file_handler = logging.FileHandler(log_file_path, mode="a")
        file_handler.setLevel(logging.DEBUG)
        root_logger.addHandler(file_handler)


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    """Fixture for logging, useful when running manually or outside pytest."""
    pass  # The actual configuration is done in pytest_configure hook
