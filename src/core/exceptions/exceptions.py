class ConfigError(Exception):
    """
    Base class for configuration-related errors.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return f"ConfigError: {self.message}"


class FileNotFoundError(ConfigError):
    """
    Raised when the configuration file cannot be found.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(f"Configuration file not found: {file_path}")
        self.file_path = file_path

    def __str__(self) -> str:
        return (
            f"FileNotFoundError: Configuration file not found at path: {self.file_path}"
        )


class JSONParsingError(ConfigError):
    """
    Raised when there is an error parsing the JSON configuration file.
    """

    def __init__(self, file_path: str, error_details: str) -> None:
        super().__init__(
            f"Error parsing the JSON configuration file: {file_path}. Error: {error_details}"
        )
        self.file_path = file_path
        self.error_details = error_details

    def __str__(self) -> str:
        return f"JSONParsingError: Error parsing JSON at {self.file_path}. Details: {self.error_details}"


class EnvironmentVariableError(Exception):
    """
    Raised when an expected environment variable is missing or has an invalid value.
    """

    def __init__(
        self,
        variable_name: str,
        message: str = "Environment variable is missing or invalid",
    ) -> None:
        super().__init__(f"{message}: {variable_name}")
        self.variable_name = variable_name
        self.message = message

    def __str__(self) -> str:
        return f"EnvironmentVariableError: {self.message} - {self.variable_name}"


class APIClientError(Exception):
    """
    Base class for API client-related errors.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return f"APIClientError: {self.message}"


class APIRequestError(APIClientError):
    """
    Raised when an API request fails.
    """

    def __init__(self, status_code: int, response_message: str) -> None:
        super().__init__(
            f"API request failed with status code {status_code}. Response: {response_message}"
        )
        self.status_code = status_code
        self.response_message = response_message

    def __str__(self) -> str:
        return f"APIRequestError: Status code {self.status_code}, Response: {self.response_message}"


class APITimeoutError(APIClientError):
    """
    Raised when an API request times out.
    """

    def __init__(self, timeout_value: int) -> None:
        super().__init__(f"API request timed out after {timeout_value} seconds.")
        self.timeout_value = timeout_value

    def __str__(self) -> str:
        return f"APITimeoutError: Request timed out after {self.timeout_value} seconds"
