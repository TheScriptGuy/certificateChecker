import os
from typing import Union

class FileOperations:
    """
    A class to write the contents of a variable to a file in binary form.

    Attributes:
        file_path (str): The path to the file where the binary data will be written.
    """

    def __init__(self, file_path: str):
        """
        Initializes the BinaryFileWriter with the specified file path.

        Args:
            file_path (str): The path to the file where the binary data will be written.
        """
        self.file_path = file_path

    def ensure_directory(self) -> None:
        """
        Ensures that the directory for the file path exists. If not, it creates the necessary directories.
        """
        directory = os.path.dirname(self.file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def write_binary(self, content: bytes) -> None:
        """
        Writes the provided content to the file in binary form.

        Args:
            content (bytes): The binary data to be written to the file.

        Raises:
            ValueError: If the content is not of type bytes.
            IOError: If there is an issue writing to the file.
        """
        if not isinstance(content, bytes):
            raise ValueError("Content must be of type bytes.")

        # Ensure the directory exists
        self.ensure_directory()

        try:
            with open(self.file_path, 'wb') as file:
                file.write(content)
        except IOError as e:
            print(f"An error occurred while writing to the file: {e}")
            raise

