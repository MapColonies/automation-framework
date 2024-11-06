import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


def get_config_value(key, default=None):
    """
    Get a configuration value from environment variables.

    :param key: The key for the configuration value
    :param default: The default value to return if the key is not found
    :return: The configuration value
    """
    return os.getenv(key, default)


def load_all_config():
    """
    Load all configuration values into a dictionary.

    :return: Dictionary of all configuration key-value pairs
    """
    return {key: value for key, value in os.environ.items()}