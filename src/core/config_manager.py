import json
import logging
import os
from typing import Any, Dict, Optional

import toml
import yaml
from dotenv import load_dotenv

from src.core.exceptions.config_exceptions import ConfigError, JSONParsingError

# Load environment variables from a .env file if present
load_dotenv()

# Set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class ConfigManager:
    def __init__(self, config_file_path: Optional[str] = None) -> None:
        """
        Initialize ConfigManager.

        :param config_file_path: Path to the configuration file (optional)
        """
        self.config: Dict[str, Any] = {}
        if config_file_path:
            self.load_config_file(config_file_path)

    def load_config_file(self, file_path: str) -> None:
        """
        Load configuration values from a JSON, YAML, or TOML file.

        :param file_path: Path to the configuration file
        :raises FileNotFoundError: If the file does not exist
        :raises JSONParsingError: If the JSON file cannot be parsed
        :raises ConfigError: If the configuration file format is not supported
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)

        try:
            if file_path.endswith(".json"):
                with open(file_path, "r") as config_file:
                    self.config = json.load(config_file)
                logger.info(f"Configuration loaded successfully from {file_path}.")
            elif file_path.endswith((".yaml", ".yml")):
                with open(file_path, "r") as config_file:
                    self.config = yaml.safe_load(config_file)
                logger.info(f"Configuration loaded successfully from {file_path}.")
            elif file_path.endswith(".toml"):
                with open(file_path, "r") as config_file:
                    self.config = toml.load(config_file)
                logger.info(f"Configuration loaded successfully from {file_path}.")
            else:
                raise ConfigError(
                    "Unsupported configuration file format. Supported formats are JSON, YAML, and TOML."
                )
        except (json.JSONDecodeError, yaml.YAMLError, toml.TomlDecodeError) as e:
            raise JSONParsingError(file_path, str(e))

    def get_config_value(
        self, key: str, expected_type: type, default: Optional[Any] = None
    ) -> Any:
        """
        Get a configuration value from the environment or config file.

        :param key: The key for the configuration value
        :param expected_type: The expected type of the configuration value
        :param default: The default value to return if the key is not found
        :return: The configuration value or the default value
        :raises TypeError: If the value does not match the expected type
        """
        # First, try to get the value from environment variables
        value = os.getenv(key)
        if value is not None:
            logger.debug(
                f"Retrieved config key '{key}' from environment with value: {value}"
            )
            return self._validate_type(key, value, expected_type)

        # Then, try to get the value from the loaded config file
        if key in self.config:
            value = self.config[key]
            logger.debug(
                f"Retrieved config key '{key}' from config file with value: {value}"
            )
            return self._validate_type(key, value, expected_type)

        # If not found, use the provided default
        logger.warning(f"Config key '{key}' not found. Using default value: {default}")
        return (
            self._validate_type(key, default, expected_type)
            if default is not None
            else default
        )

    def load_all_environment_variables(self) -> Dict[str, str]:
        """
        Load all configuration values from the environment.

        :return: Dictionary of all configuration key-value pairs from the environment
        """
        logger.info("Loading all configuration values from environment variables.")
        return {key: value for key, value in os.environ.items()}

    def _validate_type(self, key: str, value: Any, expected_type: type) -> Any:
        """
        Validate the type of the configuration value.

        :param key: The key for the configuration value
        :param value: The configuration value to validate
        :param expected_type: The expected type of the value
        :return: The validated value
        :raises TypeError: If the value does not match the expected type
        """
        if not isinstance(value, expected_type):
            raise TypeError(
                f"Config key '{key}' is expected to be of type '{expected_type.__name__}', but got '{type(value).__name__}'"
            )
        return value


# Example usage
# if __name__ == "__main__":
#     # Initialize ConfigManager with a config file (optional)
#     config_manager = ConfigManager(config_file_path="config/environment_config.yaml")
#
#     # Example to get a configuration value with type validation
#     api_base_url = config_manager.get_config_value(
#         "API_BASE_URL", str, "http://localhost:5000"
#     )
#     logger.info(f"API Base URL: {api_base_url}")
