import json
import csv
import os
from typing import Any, Dict, List


class FileReaderWriter:
    """
    A utility class for reading and writing files in different formats.
    """

    @staticmethod
    def read_json(file_path: str) -> Dict[str, Any]:
        """
        Reads JSON data from a file.

        :param file_path: Path to the JSON file.
        :return: Parsed JSON data as a dictionary.
        :raises FileNotFoundError: If the file does not exist.
        :raises json.JSONDecodeError: If the file content is not valid JSON.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, "r") as json_file:
            return json.load(json_file)

    @staticmethod
    def write_json(file_path: str, data: Dict[str, Any]) -> None:
        """
        Writes data to a JSON file.

        :param file_path: Path to the JSON file.
        :param data: Data to write.
        """
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

    @staticmethod
    def read_csv(file_path: str) -> List[Dict[str, str]]:
        """
        Reads CSV data from a file.

        :param file_path: Path to the CSV file.
        :return: List of dictionaries representing rows in the CSV.
        :raises FileNotFoundError: If the file does not exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            return [row for row in reader]

    @staticmethod
    def write_csv(
        file_path: str, data: List[Dict[str, Any]], fieldnames: List[str]
    ) -> None:
        """
        Writes data to a CSV file.

        :param file_path: Path to the CSV file.
        :param data: List of dictionaries representing rows to write.
        :param fieldnames: List of field names for the CSV.
        """
        with open(file_path, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def read_text(file_path: str) -> str:
        """
        Reads text data from a file.

        :param file_path: Path to the text file.
        :return: Content of the file as a string.
        :raises FileNotFoundError: If the file does not exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, "r") as text_file:
            return text_file.read()

    @staticmethod
    def write_text(file_path: str, data: str) -> None:
        """
        Writes text data to a file.

        :param file_path: Path to the text file.
        :param data: Text data to write.
        """
        with open(file_path, "w") as text_file:
            text_file.write(data)
