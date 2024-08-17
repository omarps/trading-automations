import os
from rename_strategy.renamer import Renamer
from rename_strategy.renamer_strategy import RenamerStrategy


class BaseRenamer(Renamer):
    def __init__(self, strategy: RenamerStrategy):
        super().__init__(strategy)

    def rename_files(self, base_path, ticker='SPY', dry_run=True):
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
