import os
import re
from rename_strategy.renamer_strategy import RenamerStrategy
from utils.constants import GAMMAS


class RenamerGammaStrategy(RenamerStrategy):
    def __init__(self):
        super().__init__()
        self.section_name = GAMMAS
        self.folder_name = GAMMAS
        self.pattern = r'Screenshot (\d{4}-\d{2}-\d{2}) at (\d{1,2})\.(\d{2})\.(\d{2})\s([ap]\.m\.)'
        self.new_filename = "{ticker}_gamma_{date}-{hour:02d}_{minute}_{second}.png"

    def rename(self, original_filepath, root, file, idx=None):
        folder_name = os.path.basename(root)
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
