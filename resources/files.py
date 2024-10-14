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
    week_path = os.getenv("WEEK_PATH")
    base_path = os.getenv("BASE_PATH")
    ticker = os.getenv("TICKER")
    dry_run = os.getenv("DRY_RUN").lower() == 'true'

    # Ask for which option to run for resources
    option = input(
        "Which option do you want to run?\n"
        "1: Rename files in folders (PDT)\n"
        "2: Move files and restructuring (PDT)\n"
        "3: Rename files in folders (Week)\n"
        "4: Move files and restructuring (Week)\n"
    )

    if option == "1":
        # 1. Rename the files in the folder structure (PDT: graficos, contratos, gammas)
        rename_files_in_folders(input_path, ticker, dry_run)
    elif option == "2":
        # 2. Move the files from the input folder to the base folder (PDT)
        move_and_restructure(input_path, base_path, date)
    if option == "3":
        # 3. Rename the files in the folder structure (Week: graficos, screenshots, other)
        rename_files_in_folders(week_path, ticker="PDTS", dry_run=dry_run)
    elif option == "4":
        # 4. Move the files from the input folder to the base folder (Week)
        move_and_restructure(week_path, base_path, dates.get_date_param("week"), suffix="week")
    else:
        print("Invalid option. Exiting...")


if __name__ == "__main__":
    run()
