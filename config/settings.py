import os
from configparser import ConfigParser
from dotenv import load_dotenv

load_dotenv()

# Determine the environment (default to 'dev')
ENV = os.getenv('ENV', 'dev').lower()

CONFIG_FILE = os.path.join(os.path.dirname(__file__), f"{ENV}.ini")

if not os.path.exists(CONFIG_FILE):
    raise FileNotFoundError(f"Configuration file not found: {CONFIG_FILE}")

config = ConfigParser()
config.read(CONFIG_FILE)


# Usage
# DEBUG = config.getboolean('DEFAULT', 'DEBUG', fallback=False)
# DATABASE_URL = config.get('DEFAULT', 'DATABASE_URL', fallback='sqlite:///:memory:')
# API_KEY = config.get('DEFAULT', 'API_KEY', fallback='default_api_key')

# Debugging logs
# print(f"Environment: {ENV}")
# print(f"Using configuration file: {CONFIG_FILE}")


# Class Example for easier passs to other functions

# class Config:
#     DEBUG = config.getboolean('DEFAULT', 'DEBUG', fallback=False)
#     DATABASE_URL = config.get('DEFAULT', 'DATABASE_URL', fallback='sqlite:///:memory:')
#     API_KEY = config.get('DEFAULT', 'API_KEY', fallback='default_api_key')
#
#
# print(Config.API_KEY)
