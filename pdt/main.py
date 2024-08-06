import sys
from datetime import datetime
import os
from dotenv import load_dotenv
from resources import rename_files_in_folders, move_and_restructure
from reports import generate_yaml, generate_pdf


load_dotenv()

def run():
    date = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y%m%d")

    # Get parameters from environment variables
    input_path = os.getenv("INPUT_PATH")
    base_path = os.getenv("BASE_PATH")
    ticker = os.getenv("TICKER")
    dry_run = os.getenv("DRY_RUN").lower() == 'true'

    # 1. Rename the files in the folder structure (graficos, contratos, gammas)
    rename_files_in_folders(input_path, ticker, dry_run)

    # 2. Move the files from the input folder to the base folder
    # operation = "copy" if dry_run else "move"
    # move_and_restructure(input_path, base_path, date, operation)
    move_and_restructure(input_path, base_path, date)

    # 3. Generate the YAML file
    generate_yaml(base_path, date)

    # 4. Generate the PDF file
    generate_pdf(base_path, date, ticker)

    # TODO: If folder exists ask if want to overwrite.
    # TODO: NTH - Add a command-line interface to run the scripts
    # TODO: NTH - Process MD files to extract contracts: targets and stops.


if __name__ == "__main__":
    run()
