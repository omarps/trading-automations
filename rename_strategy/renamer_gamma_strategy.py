import os
import re
from rename_strategy.renamer_strategy import RenamerStrategy
from utils.constants import GAMMAS


class RenamerGammaStrategy(RenamerStrategy):
    """
    This class is responsible for renaming files in a gammas folder structure using a gamma strategy.

    Attributes:
        section_name (str): The section name for which the files are being renamed. (GAMMAS)
        folder_name (str): The folder name for which the files are being renamed. (GAMMAS)
        pattern (str): The pattern to be used in the renaming process.
        (Screenshot (\\d{4}-\\d{2}-\\d{2}) at (\\d{1,2})\\.(\\d{2})\\.(\\d{2})\\s([ap]\\.m\\.))
        new_filename (str): The new filename to be used in the renaming process (ticker_gamma_date-hour_minute_second.png)
    """
    def __init__(self):
        super().__init__()
        self.section_name = GAMMAS
        self.folder_name = GAMMAS
        self.pattern = r'Screenshot (\d{4}-\d{2}-\d{2}) at (\d{1,2})\.(\d{2})\.(\d{2})\s([ap]\.*m\.*)'
        self.new_filename = "{ticker}_gamma_{date}-{hour:02d}_{minute}_{second}.png"

    def rename(self, original_filepath, root, file, idx=None, ticker='SPY'):
        """
        Renames a file using a gamma strategy.

        This method renames a file using the gamma strategy.

        Args:
            original_filepath (str): The original file path.
            root (str): The root directory path.
            file (str): The file name.
            idx (int): The index of the file in the directory. (not used)
            ticker (str): The ticker to be used in the renaming process. (default is 'SPY')

        Returns:
            str: The new file path.
        """
        match = re.match(self.pattern, file)

        if not match:
            return None

        date = match.group(1)
        hour = int(match.group(2))
        minute = match.group(3)
        second = match.group(4)
        period = match.group(5)

        # Convert hour to 24-hour format if necessary
        if period == 'p.m.' and hour != 12:
            hour += 12
        elif period == 'a.m.' and hour == 12:
            hour = 0

        new_filename = self.new_filename.format(ticker='SPY', date=date, hour=hour, minute=minute, second=second)
        new_filepath = os.path.join(root, new_filename)
        return new_filepath
