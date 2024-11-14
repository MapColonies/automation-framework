from .base_exception import AutomationFrameworkError


class APIClientError(AutomationFrameworkError):
    """
    Base class for API client-related errors.
    """

    pass


class APIRequestError(APIClientError):
    """
    Raised when an API request fails.
    """

    def __init__(self, status_code: int, response_message: str) -> None:
        super().__init__(
            f"API request failed with status code {status_code}: {response_message}"
        )
        self.status_code = status_code
        self.response_message = response_message


class APITimeoutError(APIClientError):
    """
    Raised when an API request times out.
    """

    def __init__(self, timeout_value: int) -> None:
        super().__init__(f"API request timed out after {timeout_value} seconds")
        self.timeout_value = timeout_value
