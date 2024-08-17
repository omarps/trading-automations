import os
import re
import datetime
import inflect
from rename_strategy.renamer_strategy import RenamerStrategy

DEFAULT_PATTERN = r'IMG_(\d+)'
DEFAULT_NEW_FILENAME = "{ticker}_{section_name}_{formatted_creation_time}_{file}"


def singularize_section_name(section_name):
    p = inflect.engine()
    singular = p.singular_noun(section_name)
    return singular if singular else section_name


class RenamerDefaultStrategy(RenamerStrategy):
    def __init__(self, section_name, folder_name=None, pattern=None, new_filename=None):
        super().__init__()
        self.section_name = section_name
        self.folder_name = folder_name if folder_name is not None else section_name
        self.pattern = pattern if pattern is not None else DEFAULT_PATTERN
        self.new_filename = new_filename if new_filename is not None else DEFAULT_NEW_FILENAME

    def rename(self, original_filepath, root, file, idx=None):
        match = re.match(self.pattern, file)

        if not match:
            return None

        creation_time = os.path.getctime(original_filepath)
        formatted_creation_time = datetime.datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d_%H-%M-%S")
        new_filename = self.new_filename.format(
            ticker='SPY', # introduce parameter
            section_name=singularize_section_name(self.section_name),
            formatted_creation_time=formatted_creation_time,
            file=file
        )
        new_filepath = os.path.join(root, new_filename)
        return new_filepath
