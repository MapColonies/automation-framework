import os
import json
from typing import Any, Dict, Optional
from dotenv import load_dotenv
import logging
from exceptions import JSONParsingError

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
        Load configuration values from a JSON file.

        :param file_path: Path to the configuration JSON file
        :raises FileNotFoundError: If the file does not exist
        :raises JSONParsingError: If the JSON file cannot be parsed
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)

        try:
            with open(file_path, "r") as config_file:
                self.config = json.load(config_file)
            logger.info(f"Configuration loaded successfully from {file_path}.")
        except json.JSONDecodeError as e:
            raise JSONParsingError(file_path, str(e))

    def get_config_value(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Get a configuration value from the environment or config file.

        :param key: The key for the configuration value
        :param default: The default value to return if the key is not found
        :return: The configuration value or the default value
        """
        # First, try to get the value from environment variables
        value = os.getenv(key)
        if value is not None:
            logger.debug(
                f"Retrieved config key '{key}' from environment with value: {value}"
            )
            return value

        # Then, try to get the value from the loaded config file
        if key in self.config:
            logger.debug(
                f"Retrieved config key '{key}' from config file with value: {self.config[key]}"
            )
            return self.config[key]

        # If not found, use the provided default
        logger.warning(f"Config key '{key}' not found. Using default value: {default}")
        return default

    def load_all_environment_variables(self) -> Dict[str, str]:
        """
        Load all configuration values from the environment.

        :return: Dictionary of all configuration key-value pairs from the environment
        """
        logger.info("Loading all configuration values from environment variables.")
        return {key: value for key, value in os.environ.items()}


# Example usage
# if __name__ == "__main__":
#     # Initialize ConfigManager with a config file (optional)
#     config_manager = ConfigManager(config_file_path="config/environment_config.json")
#
#     # Example to get a configuration value
#     api_base_url = config_manager.get_config_value("API_BASE_URL", "http://localhost:5000")
#     logger.info(f"API Base URL: {api_base_url}")
