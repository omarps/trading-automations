import os
import re
from rename_strategy.renamer_strategy import RenamerStrategy
from utils.constants import OPTIONS, CONTRATOS


class RenamerOptionsContractsStrategy(RenamerStrategy):
    """
    This class is responsible for renaming files in a contracts folder structure using an options contract strategy.

    Attributes:
        section_name (str): The section name for which the files are being renamed. (OPTIONS)
        folder_name (str): The folder name for which the files are being renamed. (CONTRATOS)
        pattern (str): The pattern to be used in the renaming process. (\d{4}-\d{2}-\d{2})
        new_filename (str): The new filename to be used in the renaming process (folder_name_date_idx.ext)
    """
    def __init__(self):
        super().__init__()
        self.section_name = OPTIONS
        self.folder_name = CONTRATOS
        self.pattern = r'(\d{4}-\d{2}-\d{2})'
        self.new_filename = "{folder_name}_{date}_{idx}.png"

    def rename(self, original_filepath, root, file, idx):
        """
        Renames a file using an options contract strategy.

        This method renames a file using the options contract strategy.

        Args:
            original_filepath (str): The original file path.
            root (str): The root directory path.
            file (str): The file name.
            idx (int): The index of the file in the directory.
        """
        # Extract the folder name
        folder_name = os.path.basename(root)

        filename, ext = os.path.splitext(file)
        parts = filename.split('_')
        if len(parts) < 2:
            return None  # Skip files that don't match the expected pattern

        match = re.match(self.pattern, file)
        if not match:
            return None

        date = match.group(1)
        new_filename = self.new_filename.format(folder_name=folder_name, date=date, idx=idx)
        new_filepath = os.path.join(root, new_filename)
        return new_filepath
