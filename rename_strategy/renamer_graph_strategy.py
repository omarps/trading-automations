import os
from rename_strategy.renamer_strategy import RenamerStrategy
from utils.constants import GRAPHS, GRAFICOS


class RenamerGraphStrategy(RenamerStrategy):
    """
    This class is responsible for renaming files in a graph folder structure using a graph strategy.

    Attributes:
        section_name (str): The section name for which the files are being renamed. (GRAPHS)
        folder_name (str): The folder name for which the files are being renamed. (GRAFICOS)
        pattern (str): The pattern to be used in the renaming process. (None)
        new_filename (str): The new filename to be used in the renaming process (ticker_folder_name_date_time.ext)
    """
    def __init__(self):
        super().__init__()
        self.section_name = GRAPHS
        self.folder_name = GRAFICOS
        self.new_filename = "{ticker}_{folder_name}_{date_time}{ext}"

    def rename(self, original_filepath, root, file, idx=None, ticker='SPY'):
        """
        Renames a file using a graph strategy.

        This method renames a file using the graph strategy.

        Args:
            original_filepath (str): The original file path.
            root (str): The root directory path.
            file (str): The file name.
            idx (int): The index of the file in the directory. (None)
            ticker (str): The ticker to be used in the renaming process. (default is 'SPY')

        Returns:
            str: The new file path.
        """
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
