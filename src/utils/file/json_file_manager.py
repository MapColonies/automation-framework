import json
import os
from typing import Any


class JsonFileManager:
    """
    JsonFileManager provides methods to handle JSON file operations.
    """

    @staticmethod
    def load_json_data(file_path: str) -> Any:
        """
        Load data from a JSON file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Error parsing JSON from file {file_path}: {str(e)}")
        except OSError as e:
            raise RuntimeError(f"Error reading file {file_path}: {str(e)}")

    @staticmethod
    def save_json_data(file_path: str, data: Any) -> None:
        """
        Save data to a JSON file.
        """
        try:
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
        except TypeError as e:
            raise RuntimeError(f"Data provided cannot be serialized to JSON: {str(e)}")
        except OSError as e:
            raise RuntimeError(f"Error writing to file {file_path}: {str(e)}")
