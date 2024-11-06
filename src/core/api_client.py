import requests
from requests.exceptions import RequestException
from tenacity import retry, stop_after_attempt, wait_fixed
from utils.logger import get_logger
from utils.config_loader import get_config_value

# Get a logger instance
logger = get_logger(__name__)


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def make_request(self, method, endpoint, params=None, data=None, headers=None):
        """
        Make an HTTP request with retry logic.

        :param method: HTTP method (e.g., 'GET', 'POST')
        :param endpoint: API endpoint
        :param params: Query parameters
        :param data: Request payload
        :param headers: Custom headers
        :return: Response object
        """
        url = f"{self.base_url}{endpoint}"
        request_headers = headers if headers else self.headers

        try:
            response = requests.request(method, url, params=params, json=data, headers=request_headers)
            response.raise_for_status()
            return response
        except RequestException as e:
            logger.error(f"Request failed: {e}")
            raise

    def get(self, endpoint, params=None):
        """
        Make a GET request.

        :param endpoint: API endpoint
        :param params: Query parameters
        :return: Response object
        """
        return self.make_request('GET', endpoint, params=params)

    def post(self, endpoint, data=None):
        """
        Make a POST request.

        :param endpoint: API endpoint
        :param data: Request payload
        :return: Response object
        """
        return self.make_request('POST', endpoint, data=data)

    def put(self, endpoint, data=None):
        """
        Make a PUT request.

        :param endpoint: API endpoint
        :param data: Request payload
        :return: Response object
        """
        return self.make_request('PUT', endpoint, data=data)

    def delete(self, endpoint, params=None):
        """
        Make a DELETE request.

        :param endpoint: API endpoint
        :param params: Query parameters
        :return: Response object
        """
        return self.make_request('DELETE', endpoint, params=params)


# Usage example
# if __name__ == "__main__":
#     base_url = get_config_value("API_BASE_URL", "http://localhost:5000")
#     client = APIClient(base_url)
#
#     # Example GET request
#     response = client.get("/example-endpoint")
#     logger.info(f"Response: {response.status_code}, {response.json()}")