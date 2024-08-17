import os
from rename_strategy.renamer_strategy import RenamerStrategy
from utils.constants import GRAPHS, GRAFICOS


class RenamerGraphStrategy(RenamerStrategy):
    def __init__(self):
        super().__init__()
        self.section_name = GRAPHS
        self.folder_name = GRAFICOS
        self.new_filename = "{ticker}_{folder_name}_{date_time}{ext}"

    def rename(self, original_filepath, root, file, idx=None):
        folder_name = os.path.basename(root)
        if folder_name in file:
            return None  # Skip if filename contains the folder name already

        filename, ext = os.path.splitext(file)
        parts = filename.split('_')
        if len(parts) < 3:
            return None  # Skip files that don't match the expected pattern

        ticker = parts[0]
        date_time = '_'.join(parts[1:])
        new_filename = self.new_filename.format(ticker=ticker, folder_name=folder_name, date_time=date_time, ext=ext)
        new_filepath = os.path.join(root, new_filename)
        return new_filepath
