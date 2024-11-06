import pytest
from services.user_service import UserService
from utils.logger import get_logger

# Get a logger instance
logger = get_logger(__name__)

@pytest.fixture(scope="module")
def user_service():
    """
    Fixture to initialize UserService instance.
    """
    return UserService()

def test_get_user(user_service):
    """
    Test getting user details by user ID.
    """
    user_id = 1
    response = user_service.get_user(user_id)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    logger.info(f"User details: {response.json()}")

def test_create_user(user_service):
    """
    Test creating a new user.
    """
    user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 30
    }
    response = user_service.create_user(user_data)
    assert response.status_code == 201, f"Expected 201 but got {response.status_code}"
    logger.info(f"Created user: {response.json()}")

def test_update_user(user_service):
    """
    Test updating an existing user's details.
    """
    user_id = 1
    updated_user_data = {
        "name": "John Doe Updated",
        "email": "john.doe.updated@example.com",
        "age": 31
    }
    response = user_service.update_user(user_id, updated_user_data)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    logger.info(f"Updated user details: {response.json()}")

def test_delete_user(user_service):
    """
    Test deleting a user by user ID.
    """
    user_id = 1
    response = user_service.delete_user(user_id)
    assert response.status_code == 204, f"Expected 204 but got {response.status_code}"
    logger.info(f"Deleted user with ID: {user_id}")

