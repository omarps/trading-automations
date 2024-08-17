from abc import ABC, abstractmethod
from rename_strategy.renamer_strategy import RenamerStrategy


class Renamer(ABC):

    def __init__(self, strategy: RenamerStrategy):
        self.strategy = strategy

    @abstractmethod
    def rename_files(self, base_path, ticker='SPY', dry_run=True):
        pass
