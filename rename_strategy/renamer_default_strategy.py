import os
import re
import datetime
import inflect
from rename_strategy.renamer_strategy import RenamerStrategy
from resources import images

DEFAULT_PATTERN = r'IMG_(\d+)'
DEFAULT_NEW_FILENAME = "{ticker}_{section_name}_{formatted_creation_time}_{file}"


# TODO: move to string utils
def singularize_section_name(section_name):
    """
    Singularizes the section name.

    Args:
        section_name (str): The section name.

    Returns:
        str: The singularized section name.
    """
    p = inflect.engine()
    singular = p.singular_noun(section_name)
    return singular if singular else section_name


class RenamerDefaultStrategy(RenamerStrategy):
    """
    Default renamer strategy for renaming files in a default folder structure.

    This class provides a default implementation for renaming files in a given folder structure using a default
    strategy.

    Attributes:
        section_name (str): The section name for which the files are being renamed.
        folder_name (str): The folder name for which the files are being renamed. If not provided, it defaults to the
        section name.
        pattern (str): The pattern to be used in the renaming process. If not provided, it defaults to the default
        pattern.
        new_filename (str): The new filename to be used in the renaming process If not provided, it defaults to the
        default new filename.
    """
    def __init__(self, section_name, folder_name=None, pattern=None, new_filename=None):
        super().__init__()
        self.section_name = section_name
        self.folder_name = folder_name if folder_name is not None else section_name
        self.pattern = pattern if pattern is not None else DEFAULT_PATTERN
        self.new_filename = new_filename if new_filename is not None else DEFAULT_NEW_FILENAME

    def rename(self, original_filepath, root, file, idx=None, ticker='SPY'):
        """
        Renames a file using the default strategy.

        This method renames a file using the default strategy, which consists of extracting the creation time of the
        file and using it in the new filename.

        Args:
            original_filepath (str): The original file path.
            root (str): The root directory path.
            file (str): The file name.
            idx (int): The index of the file in the directory. (default is None)
            ticker (str): The ticker to be used in the renaming process. (default is 'SPY')
        """
        match = re.match(self.pattern, file)

        if not match:
            return None

        # Get file image orientation
        orientation = images.get_image_orientation(original_filepath)
        # Rotate if horizontal
        if orientation == 'Horizontal':
            images.rotate_image(original_filepath, original_filepath)

        # Rename file using creation time
        creation_time = os.path.getctime(original_filepath)
        # formatted_creation_time = datetime.datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d_%H-%M-%S")
        formatted_creation_time = datetime.datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d")
        new_filename = self.new_filename.format(
            ticker='SPY',  # introduce parameter
            section_name=singularize_section_name(self.section_name),
            formatted_creation_time=formatted_creation_time,
            file=file
        )
        new_filepath = os.path.join(root, new_filename)
        return new_filepath
