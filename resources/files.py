import os
from dotenv import load_dotenv
from utils import dates
from resources.rename import rename_files_in_folders
from resources.move import move_and_restructure

load_dotenv()


def run():
    date = dates.get_date_param()

    # Get parameters from environment variables
    input_path = os.getenv("INPUT_PATH")
    base_path = os.getenv("BASE_PATH")
    ticker = os.getenv("TICKER")
    dry_run = os.getenv("DRY_RUN").lower() == 'true'

    # Ask for which option to run for resources
    option = input(
        "Which option do you want to run?\n"
        "1: Rename files in folders\n"
        "2: Move files and restructuring\n"
    )

    if option == "1":
        # 1. Rename the files in the folder structure (graficos, contratos, gammas)
        rename_files_in_folders(input_path, ticker, dry_run)
    elif option == "2":
        # 2. Move the files from the input folder to the base folder
        # operation = "copy" if dry_run else "move"
        # move_and_restructure(input_path, base_path, date, operation)
        move_and_restructure(input_path, base_path, date)
    else:
        print("Invalid option. Exiting...")


if __name__ == "__main__":
    run()
