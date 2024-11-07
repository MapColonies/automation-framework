import json
import os
import csv
from typing import List, Dict, Any


def load_json_data(file_path: str) -> Any:
    """
    Load data from a JSON file.

    :param file_path: Path to the JSON file
    :return: Parsed JSON data
    :raises FileNotFoundError: If the file does not exist
    :raises RuntimeError: If there is an error reading the file or parsing JSON
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


def save_json_data(file_path: str, data: Any) -> None:
    """
    Save data to a JSON file.

    :param file_path: Path to the JSON file
    :param data: Data to write to the file
    :raises RuntimeError: If there is an error writing to the file
    """
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
    except TypeError as e:
        raise RuntimeError(f"Data provided cannot be serialized to JSON: {str(e)}")
    except OSError as e:
        raise RuntimeError(f"Error writing to file {file_path}: {str(e)}")


def load_csv_data(file_path: str) -> List[Dict[str, str]]:
    """
    Load data from a CSV file.

    :param file_path: Path to the CSV file
    :return: List of dictionaries representing rows in the CSV file
    :raises FileNotFoundError: If the file does not exist
    :raises RuntimeError: If there is an error reading the file or parsing CSV
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            return [row for row in reader]
    except OSError as e:
        raise RuntimeError(f"Error reading file {file_path}: {str(e)}")
    except csv.Error as e:
        raise RuntimeError(f"Error parsing CSV file {file_path}: {str(e)}")


def save_csv_data(
    file_path: str, data: List[Dict[str, Any]], fieldnames: List[str]
) -> None:
    """
    Save data to a CSV file.

    :param file_path: Path to the CSV file
    :param data: List of dictionaries representing rows to write to the file
    :param fieldnames: List of field names for the CSV
    :raises RuntimeError: If there is an error writing to the file
    """
    try:
        with open(file_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except OSError as e:
        raise RuntimeError(f"Error writing to file {file_path}: {str(e)}")
    except csv.Error as e:
        raise RuntimeError(f"Error writing CSV data to file {file_path}: {str(e)}")
