import pytest
import responses
import json
from pathlib import Path
from jsonschema import validate, ValidationError
from src.services.user_service import UserService
from src.utils.logger import get_logger
from typing import Generator

# Get a logger instance
logger = get_logger(__name__)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent

schema_path = ROOT_DIR / "schemas" / "user_schema.json"

with open(schema_path, "r") as f:
    USER_SCHEMA = json.load(f)


@pytest.fixture(scope="module")
def user_service() -> Generator[UserService, None, None]:
    """
    Fixture to initialize UserService instance.

    :return: Initialized UserService instance
    """
    logger.info("Initializing UserService instance")
    yield UserService()


@responses.activate
def test_get_user(user_service: UserService) -> None:
    """
    Test getting user details by user ID.

    :param user_service: Initialized UserService instance
    """
    user_id: int = 1
    url = f"http://localhost:5000/users/{user_id}"

    # Mocking the GET request
    responses.add(
        responses.GET,
        url,
        json={
            "id": user_id,
            "name": "John Doe",
            "email": "john.doe@example.com",
            "age": 30,
        },
        status=200,
    )

    logger.info(f"Testing GET user with ID: {user_id}")
    response = user_service.get_user(user_id)
    logger.debug(f"Response received: {response.status_code}, {response.json()}")

    # Validate response schema
    try:
        validate(instance=response.json(), schema=USER_SCHEMA)
        logger.info(
            f"GET user response schema validation passed for user ID: {user_id}"
        )
    except ValidationError as e:
        logger.error(f"GET user response schema validation failed: {e}")
        pytest.fail(f"Schema validation failed: {e}")

    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    logger.info(f"GET user test passed for user ID: {user_id}")


@responses.activate
def test_create_user(user_service: UserService) -> None:
    """
    Test creating a new user.

    :param user_service: Initialized UserService instance
    """
    user_data: dict = {"name": "John Doe", "email": "john.doe@example.com", "age": 30}
    url = "http://localhost:5000/users"

    # Mocking the POST request
    responses.add(responses.POST, url, json={"id": 1, **user_data}, status=201)

    logger.info("Testing CREATE user")
    logger.debug(f"User data being sent: {user_data}")
    response = user_service.create_user(user_data)
    logger.debug(f"Response received: {response.status_code}, {response.json()}")

    # Validate response schema
    try:
        validate(instance=response.json(), schema=USER_SCHEMA)
        logger.info("CREATE user response schema validation passed")
    except ValidationError as e:
        logger.error(f"CREATE user response schema validation failed: {e}")
        pytest.fail(f"Schema validation failed: {e}")

    assert response.status_code == 201, f"Expected 201 but got {response.status_code}"
    logger.info("CREATE user test passed")


@responses.activate
def test_update_user(user_service: UserService) -> None:
    """
    Test updating an existing user's details.

    :param user_service: Initialized UserService instance
    """
    user_id: int = 1
    updated_user_data: dict = {
        "name": "John Doe Updated",
        "email": "john.doe.updated@example.com",
        "age": 31,
    }
    url = f"http://localhost:5000/users/{user_id}"

    # Mocking the PUT request
    responses.add(
        responses.PUT, url, json={"id": user_id, **updated_user_data}, status=200
    )

    logger.info(f"Testing UPDATE user with ID: {user_id}")
    logger.debug(f"Updated user data being sent: {updated_user_data}")
    response = user_service.update_user(user_id, updated_user_data)
    logger.debug(f"Response received: {response.status_code}, {response.json()}")

    # Validate response schema
    try:
        validate(instance=response.json(), schema=USER_SCHEMA)
        logger.info(
            f"UPDATE user response schema validation passed for user ID: {user_id}"
        )
    except ValidationError as e:
        logger.error(f"UPDATE user response schema validation failed: {e}")
        pytest.fail(f"Schema validation failed: {e}")

    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    logger.info(f"UPDATE user test passed for user ID: {user_id}")


@responses.activate
def test_delete_user(user_service: UserService) -> None:
    """
    Test deleting a user by user ID.

    :param user_service: Initialized UserService instance
    """
    user_id: int = 1
    url = f"http://localhost:5000/users/{user_id}"

    # Mocking the DELETE request
    responses.add(responses.DELETE, url, status=204)

    logger.info(f"Testing DELETE user with ID: {user_id}")
    response = user_service.delete_user(user_id)
    logger.debug(f"Response received: {response.status_code}")

    assert response.status_code == 204, f"Expected 204 but got {response.status_code}"
    logger.info(f"DELETE user test passed for user ID: {user_id}")
