import tempfile
import os
from typing import Generator


class TemporaryFileManager:
    """
    A utility class for managing temporary files.
    """

    @staticmethod
    def create_temp_file(
        suffix: str = "", prefix: str = "temp_", dir: str = None
    ) -> str:
        """
        Creates a temporary file and returns its path.

        :param suffix: The file name suffix (e.g., '.json').
        :param prefix: The file name prefix.
        :param dir: The directory where the file is to be created.
        :return: The path to the created temporary file.
        """
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix=suffix, prefix=prefix, dir=dir
        )
        return temp_file.name

    @staticmethod
    def create_temp_file_with_content(
        content: str, suffix: str = "", prefix: str = "temp_", dir: str = None
    ) -> str:
        """
        Creates a temporary file with the specified content.

        :param content: The content to write to the file.
        :param suffix: The file name suffix.
        :param prefix: The file name prefix.
        :param dir: The directory where the file is to be created.
        :return: The path to the created temporary file.
        """
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix=suffix, prefix=prefix, dir=dir, mode="w"
        )
        temp_file.write(content)
        temp_file.close()
        return temp_file.name

    @staticmethod
    def delete_temp_file(file_path: str) -> None:
        """
        Deletes a temporary file.

        :param file_path: Path to the file to delete.
        :raises FileNotFoundError: If the file does not exist.
        """
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            raise FileNotFoundError(f"Temporary file not found: {file_path}")

    @staticmethod
    def temp_file_context(
        suffix: str = "", prefix: str = "temp_", dir: str = None
    ) -> Generator[str, None, None]:
        """
        Creates a temporary file and provides its path in a context manager-like usage.

        :param suffix: The file name suffix.
        :param prefix: The file name prefix.
        :param dir: The directory where the file is to be created.
        :yield: The path to the created temporary file.
        """
        temp_file_path = tempfile.NamedTemporaryFile(
            delete=False, suffix=suffix, prefix=prefix, dir=dir
        ).name
        try:
            yield temp_file_path
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
