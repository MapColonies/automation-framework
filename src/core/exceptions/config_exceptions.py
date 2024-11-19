from .base_exception import AutomationFrameworkError


class ConfigError(AutomationFrameworkError):
    """
    Base class for configuration-related errors.
    """

    pass


class FileNotFoundError(ConfigError):
    """
    Raised when the configuration file cannot be found.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(f"Configuration file not found: {file_path}")
        self.file_path = file_path


class JSONParsingError(ConfigError):
    """
    Raised when there is an error parsing the JSON configuration file.
    """

    def __init__(self, file_path: str, error_details: str) -> None:
        super().__init__(
            f"Error parsing the JSON configuration file at {file_path}: {error_details}"
        )
        self.file_path = file_path
        self.error_details = error_details


class EnvironmentVariableError(ConfigError):
    """
    Raised when an expected environment variable is missing or has an invalid value.
    """

    def __init__(self, variable_name: str) -> None:
        super().__init__(
            f"Environment variable '{variable_name}' is missing or invalid"
        )
        self.variable_name = variable_name
