import requests
from requests import Response
from requests.exceptions import HTTPError, Timeout, RequestException
from tenacity import retry, stop_after_attempt, wait_fixed

from src.utils.logger import get_logger
from typing import Optional, Dict, Any
from src.core.exceptions.api_exceptions import (
    APIRequestError,
    APITimeoutError,
    APIClientError,
)

# Get a logger instance
logger = get_logger(__name__)


class APIClient:
    def __init__(self, base_url: str) -> None:
        self.base_url: str = base_url
        self.headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Response:
        """
        Make an HTTP request with retry logic.

        :param method: HTTP method (e.g., 'GET', 'POST')
        :param endpoint: API endpoint
        :param params: Query parameters
        :param data: Request payload
        :param headers: Custom headers
        :return: Response object
        :raises APIRequestError: If the API request fails
        :raises APITimeoutError: If the API request times out
        :raises APIClientError: For other types of request failures
        """
        url = f"{self.base_url}{endpoint}"
        request_headers = headers if headers else self.headers

        try:
            logger.info(
                f"Making {method} request to {url} with params={params} and data={data}"
            )
            response = requests.request(
                method,
                url,
                params=params,
                json=data,
                headers=request_headers,
                timeout=10,
            )
            response.raise_for_status()
            logger.info(
                f"Request to {url} succeeded with status code {response.status_code}"
            )
            return response

        except HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err} - URL: {url}")
            raise APIRequestError(response.status_code, str(http_err)) from http_err

        except Timeout as timeout_err:
            logger.error(f"Request timed out: {timeout_err} - URL: {url}")
            raise APITimeoutError(10) from timeout_err

        except RequestException as req_err:
            logger.error(f"An error occurred with the request: {req_err} - URL: {url}")
            raise APIClientError(
                f"An error occurred with the request: {req_err}"
            ) from req_err

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Response:
        """
        Make a GET request.

        :param endpoint: API endpoint
        :param params: Query parameters
        :return: Response object
        """
        return self.make_request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Response:
        """
        Make a POST request.

        :param endpoint: API endpoint
        :param data: Request payload
        :return: Response object
        """
        return self.make_request("POST", endpoint, data=data)

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Response:
        """
        Make a PUT request.

        :param endpoint: API endpoint
        :param data: Request payload
        :return: Response object
        """
        return self.make_request("PUT", endpoint, data=data)

    def delete(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Response:
        """
        Make a DELETE request.

        :param endpoint: API endpoint
        :param params: Query parameters
        :return: Response object
        """
        return self.make_request("DELETE", endpoint, params=params)


# Usage example
# if __name__ == "__main__":
#     from src.utils.config_loader import get_config_value
#     base_url = get_config_value("API_BASE_URL", "http://localhost:5000")
#     client = APIClient(base_url)
#
#     # Example GET request
#     response = client.get("/example-endpoint")
#     logger.info(f"Response: {response.status_code}, {response.json()}")
