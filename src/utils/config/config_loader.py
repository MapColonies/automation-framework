import logging
import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv


class ConfigLoader:
    # Load environment variables from a .env file
    try:
        load_dotenv()
    except Exception as e:
        raise RuntimeError(f"Error loading .env file: {str(e)}")

    # Set up a logger
    logger = logging.getLogger("ConfigLoader")
    logging.basicConfig(level=logging.INFO)

    @staticmethod
    def get_config_value(key: str, default: Optional[Any] = None) -> Optional[str]:
        """
        Get a configuration value from environment variables.

        :param key: The key for the configuration value
        :param default: The default value to return if the key is not found
        :return: The configuration value as a string or the default value
        :raises RuntimeError: If there is an issue accessing the environment variable
        """
        try:
            value = os.getenv(key, default)
            if value is None:
                ConfigLoader.logger.warning(
                    f"Config key '{key}' not found. Using default value: {default}"
                )
            return value
        except Exception as e:
            ConfigLoader.logger.error(
                f"Error accessing environment variable '{key}': {str(e)}"
            )
            raise RuntimeError(
                f"Error accessing environment variable '{key}': {str(e)}"
            )

    @staticmethod
    def load_all_config() -> Dict[str, str]:
        """
        Load all configuration values into a dictionary.

        :return: Dictionary of all configuration key-value pairs
        :raises RuntimeError: If there is an issue accessing environment variables
        """
        try:
            return {key: value for key, value in os.environ.items()}
        except Exception as e:
            ConfigLoader.logger.error(f"Error loading environment variables: {str(e)}")
            raise RuntimeError(f"Error loading environment variables: {str(e)}")


# Example usage:
# value = ConfigLoader.get_config_value('MY_CONFIG_KEY', 'default_value')
# all_configs = ConfigLoader.load_all_config()
