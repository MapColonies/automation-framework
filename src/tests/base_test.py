import pytest
import logging
from src.core.api_client import APIClient
from src.utils.config_loader import get_config_value
from typing import Any

# Setting up a logger
logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("configure_logging")
class BaseTest:
    """
    A base test class that provides shared setup and utilities for derived test classes.
    """

    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, request: Any) -> None:
        """
        Set up method that is run once per test class.

        Initializes API client and other shared resources for the tests.

        :param request: Provides information about the requesting test context.
        """
        logger.info(f"Setting up test class: {request.cls.__name__}")

        # Initialize API client with base URL from configuration
        base_url = get_config_value("API_BASE_URL", "http://localhost:5000")
        request.cls.api_client = APIClient(base_url)

    @pytest.fixture(scope="function", autouse=True)
    def setup_method(self, request: Any) -> None:
        """
        Set up method that is run before every test function.

        Ensures any pre-test conditions are met and logs the start of each test.

        :param request: Provides information about the requesting test context.
        """
        test_name = request.node.name
        logger.info(f"\n=== Setting up for test: {test_name} ===")

    @pytest.fixture(scope="function", autouse=True)
    def teardown_method(self, request: Any) -> None:
        """
        Teardown method that is run after every test function.

        Cleans up resources and logs the end of each test.

        :param request: Provides information about the requesting test context.
        """
        yield  # Wait until the test has completed
        test_name = request.node.name
        logger.info(f"\n=== Tearing down after test: {test_name} ===")

    @pytest.fixture(scope="class", autouse=True)
    def teardown_class(self, request: Any) -> None:
        """
        Teardown method that is run after all tests in the class.

        Cleans up shared resources if needed.

        :param request: Provides information about the requesting test context.
        """
        yield  # Wait until all tests have completed
        logger.info(f"Tearing down test class: {request.cls.__name__}")
