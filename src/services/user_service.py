from src.core.api_client import APIClient
from src.utils.logger import get_logger
from src.utils.config.config_loader import get_config_value
from typing import Optional, Dict, Any
from requests import Response

# Get a logger instance
logger = get_logger(__name__)


class UserService:
    def __init__(self, api_client: Optional[APIClient] = None) -> None:
        self.api_client: APIClient = api_client or APIClient(
            base_url=get_config_value("API_BASE_URL", "http://localhost:5000")
        )
        self.endpoint: str = "/users"

    def get_user(self, user_id: int) -> Response:
        """
        Get a user's details by user ID.

        :param user_id: The ID of the user to retrieve
        :return: Response object
        """
        logger.info(f"Fetching user with ID: {user_id}")
        response: Response = self.api_client.get(f"{self.endpoint}/{user_id}")
        return response

    def create_user(self, user_data: Dict[str, Any]) -> Response:
        """
        Create a new user with the provided user data.

        :param user_data: Dictionary containing user data to create
        :return: Response object
        """
        logger.info(f"Creating a new user with data: {user_data}")
        response: Response = self.api_client.post(self.endpoint, data=user_data)
        return response

    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Response:
        """
        Update an existing user's details by user ID.

        :param user_id: The ID of the user to update
        :param user_data: Dictionary containing updated user data
        :return: Response object
        """
        logger.info(f"Updating user with ID: {user_id} with data: {user_data}")
        response: Response = self.api_client.put(
            f"{self.endpoint}/{user_id}", data=user_data
        )
        return response

    def delete_user(self, user_id: int) -> Response:
        """
        Delete a user by user ID.

        :param user_id: The ID of the user to delete
        :return: Response object
        """
        logger.info(f"Deleting user with ID: {user_id}")
        response: Response = self.api_client.delete(f"{self.endpoint}/{user_id}")
        return response


# Usage example
# if __name__ == "__main__":
#     user_service = UserService()
#
#     # Example to get user details
#     response = user_service.get_user(user_id=1)
#     logger.info(f"Response: {response.status_code}, {response.json()}")
