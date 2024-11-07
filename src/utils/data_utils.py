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
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, "r") as file:
        return json.load(file)


def save_json_data(file_path: str, data: Any) -> None:
    """
    Save data to a JSON file.

    :param file_path: Path to the JSON file
    :param data: Data to write to the file
    """
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def load_csv_data(file_path: str) -> List[Dict[str, str]]:
    """
    Load data from a CSV file.

    :param file_path: Path to the CSV file
    :return: List of dictionaries representing rows in the CSV file
    :raises FileNotFoundError: If the file does not exist
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def save_csv_data(
    file_path: str, data: List[Dict[str, Any]], fieldnames: List[str]
) -> None:
    """
    Save data to a CSV file.

    :param file_path: Path to the CSV file
    :param data: List of dictionaries representing rows to write to the file
    :param fieldnames: List of field names for the CSV
    """
    with open(file_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
