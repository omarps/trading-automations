import os
import re
from rename_strategy.renamer_strategy import RenamerStrategy
from utils.constants import OPTIONS, CONTRATOS


class RenamerOptionsContractsStrategy(RenamerStrategy):
    def __init__(self):
        super().__init__()
        self.section_name = OPTIONS
        self.folder_name = CONTRATOS
        self.pattern = r'(\d{4}-\d{2}-\d{2})'
        self.new_filename = "{folder_name}_{date}_{idx}.png"

    def rename(self, original_filepath, root, file, idx):
        # Skip directories and only process files
        if not os.path.isfile(original_filepath):
            return None

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
