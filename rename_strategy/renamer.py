from abc import ABC, abstractmethod
from rename_strategy.renamer_strategy import RenamerStrategy


class Renamer(ABC):
    """
    This class is responsible for renaming files in a given folder structure.

    Attributes:
        strategy (RenamerStrategy): The strategy to be used in the renaming process.
    """

    def __init__(self, strategy: RenamerStrategy):
        self.strategy = strategy

    @abstractmethod
    def rename_files(self, base_path, ticker='SPY', dry_run=True):
        """
        This method should rename files in a given folder structure.

        Args:
            base_path: The base path where the files are located.
            ticker: The ticker to be used in the renaming process.
            dry_run: A boolean value that indicates if the renaming should be done or not.

        Returns:
            None
        """
        pass
