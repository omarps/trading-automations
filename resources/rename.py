from rename_strategy.base_renamer import BaseRenamer
from rename_strategy.renamer_options_contracts_strategy import RenamerOptionsContractsStrategy
from rename_strategy.renamer_graph_strategy import RenamerGraphStrategy
from rename_strategy.renamer_gamma_strategy import RenamerGammaStrategy
from rename_strategy.renamer_default_strategy import RenamerDefaultStrategy
from utils.constants import SCREENSHOTS, OTHERS


def rename_files_in_folders(base_path, ticker="SPY", dry_run=True):
    print("Renaming files in folders")

    strategies = [
        RenamerGraphStrategy(),
        RenamerOptionsContractsStrategy(),
        RenamerGammaStrategy(),
        RenamerDefaultStrategy(SCREENSHOTS),
        RenamerDefaultStrategy(OTHERS)
    ]

    for strategy in strategies:
        renamer = BaseRenamer(strategy)
        renamer.rename_files(base_path, ticker, dry_run)
