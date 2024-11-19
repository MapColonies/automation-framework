import csv
import os
from typing import List, Dict, Any


class CsvFileManager:
    """
    CsvFileManager provides methods to handle CSV file operations.
    """

    @staticmethod
    def load_csv_data(file_path: str) -> List[Dict[str, str]]:
        """
        Load data from a CSV file.
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

    @staticmethod
    def save_csv_data(
        file_path: str, data: List[Dict[str, Any]], fieldnames: List[str]
    ) -> None:
        """
        Save data to a CSV file.
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
