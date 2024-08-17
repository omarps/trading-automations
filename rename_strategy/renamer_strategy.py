import os
from abc import ABC, abstractmethod


class RenamerStrategy(ABC):
    """
    Abstract base class for renaming files in a given folder structure.

    This class provides a template for renaming files in a given folder structure using a specific strategy.

    Attributes:
        section_name (str): The section name for which the files are being renamed.
        folder_name (str): The folder name for which the files are being renamed.
        pattern (str): The pattern to be used in the renaming process.
        new_filename (str): The new filename to be used in the renaming process
    """

    def __init__(self):
        self.section_name = None
        self.folder_name = None
        self.pattern = None
        self.new_filename = None

    @abstractmethod
    def rename(self, original_filepath, root, file, idx):
        """
        Renames a file using a specific strategy.

        This is an abstract method that must be implemented by subclasses to rename a file

        Args:
            original_filepath (str): The original file path.
            root (str): The root directory path.
            file (str): The file name.
            idx (int): The index of the file in the directory.

        Returns:
            str: The new file path.
        """
        if file.startswith("."):
            return None  # ignore .DS_Store files

        if not os.path.isfile(original_filepath):
            return None  # Skip directories and only process files

        pass
