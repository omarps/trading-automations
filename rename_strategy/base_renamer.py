import os
from rename_strategy.renamer import Renamer
from rename_strategy.renamer_strategy import RenamerStrategy


class BaseRenamer(Renamer):
    """
    This class is responsible for renaming files in a given folder structure using a specific strategy.

    Attributes:
        strategy (RenamerStrategy): The strategy to be used in the renaming process
    """

    def __init__(self, strategy: RenamerStrategy):
        super().__init__(strategy)

    def rename_files(self, base_path, ticker='SPY', dry_run=True):
        """
        This method renames files in a given folder structure using the specified strategy.

        Args:
            base_path (str): The base path where the files are located.
            ticker (str): The ticker to be used in the renaming process.
            dry_run (bool): A boolean value that indicates if the renaming should be done or not.

        Returns:
            None
        """
        rename_count = 0
        folder_path = os.path.join(base_path, self.strategy.folder_name)
        # Iterate over each directory in the base path
        for root, dirs, files in os.walk(folder_path):
            # Only process if there are files in the current directory
            if not files:
                continue

            # Sort files to ensure consistent incremental numbering
            files.sort()

            for idx, file in enumerate(files, start=1):
                original_filepath = os.path.join(root, file)

                # New filepath is returned by the strategy
                new_filepath = self.strategy.rename(original_filepath, root, file, idx)

                if new_filepath:
                    if dry_run:
                        print(f"Would rename: {original_filepath} to {new_filepath}")
                    else:
                        os.rename(original_filepath, new_filepath)
                        print(f"Renamed: {original_filepath} to {new_filepath}")
                    rename_count += 1

        print(f"Renamed {rename_count} files in {folder_path}")