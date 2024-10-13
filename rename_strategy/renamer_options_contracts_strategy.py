import os
import re
from datetime import datetime
from rename_strategy.renamer_strategy import RenamerStrategy
from utils.constants import OPTIONS, CONTRATOS


class RenamerOptionsContractsStrategy(RenamerStrategy):
    """
    This class is responsible for renaming files in a contracts folder structure using an options contract strategy.

    Attributes:
        section_name (str): The section name for which the files are being renamed. (OPTIONS)
        folder_name (str): The folder name for which the files are being renamed. (CONTRATOS)
        pattern (str): The pattern to be used in the renaming process. (\\d{4}-\\d{2}-\\d{2})
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

        # Skip it if folder_name already matches the pattern
        # Example: SPY241010C577_2024-10-10_2.png
        ticker = 'SPY'
        pattern = f'{ticker}\\d{{6}}[CP]\\d{{3,4}}_\\d{{4}}-\\d{{2}}-\\d{{2}}_\\d+.png'
        if re.match(pattern, file):
            return None

        filename, ext = os.path.splitext(file)
        parts = filename.split('_')
        if len(parts) < 2:
            # match pattern
            match = re.match(self.pattern, file)
            if not match:
                return None

            # Extract date from filename
            date = match.group(1)
        else:
            # Include SPYDojis folder

            # Extract date from file's creation date
            creation_time = os.path.getctime(original_filepath)
            date = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d')

        new_filename = self.new_filename.format(folder_name=folder_name, date=date, idx=idx)
        new_filepath = os.path.join(root, new_filename)
        return new_filepath
