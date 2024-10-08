import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from folders.utils import create_or_clear_folder
from utils.md import extract_contract_titles
from utils.constants import *


load_dotenv()


def create_folder_structure(base_path, date):
    # If path exists ask if you want to overwrite or exit
    if os.path.exists(base_path):
        overwrite = input(f"Folder structure already exists at {base_path}. Do you want to overwrite it? (y/n): ")
        if overwrite.lower() != "y":
            print("Exiting...")
            return
    else:
        # Create the base directory if it does not exist
        os.makedirs(base_path)

    # Define the folder structure
    folder_structure = [GRAFICOS, CONTRATOS, GAMMAS, SCREENSHOTS, OTHERS]
    graphs_structure = [V1D, ICHIM, V5M, V1M]

    # Create the folder structure
    for folder in folder_structure:
        folder_path = os.path.join(base_path, folder)
        create_or_clear_folder(folder_path)

        if folder == GRAFICOS:
            for graph in graphs_structure:
                graph_path = os.path.join(folder_path, graph)
                create_or_clear_folder(graph_path)

    # Find any MD file and remove them.
    for file in os.listdir(base_path):
        if file.endswith(".md"):
            os.remove(os.path.join(base_path, file))

    # Add a summary file to the folder
    # with name format SPY_{date}_summary.md
    # based on the summary.sample.utils file
    summary_file = os.path.join(base_path, f"SPY_{date}_summary.md")
    sample_md = os.path.join(os.path.dirname(__file__), "../templates", "summary.sample.md")
    with open(sample_md, "r") as f:
        content = f.read()
        content = content.replace("{{date}}", f"<u>{date}</u>")
        with open(summary_file, "w") as f:
            f.write(content)

    print(f"Folder structure created at: {base_path}")


def add_options_folders(input_path, date, ticker):
    sorted_folders = extract_contract_titles(os.path.join(input_path, f"SPY_{date}_summary.md"))
    sorted_folders = list(map(lambda title: title.lstrip('.'), sorted_folders))

    options_path = os.path.join(input_path, CONTRATOS)
    create_or_clear_folder(options_path)

    for option_folder in sorted_folders:
        option_path = os.path.join(options_path, option_folder)
        if not os.path.exists(option_path):
            os.makedirs(option_path)
            print(f"Created {option_path}")


def run():
    # Use the first command-line argument if provided, otherwise use today's date in the format YYYYMMDD
    date = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y%m%d")

    input_path = os.getenv("INPUT_PATH")
    ticker = os.getenv("TICKER")

    # Ask for which folder option to run and execute based on the input
    option = input(
        "Which option do you want to run?\n"
        "1: Create folder structure\n"
        "2: Add options folders\n"
    )
    if option == "1":
        create_folder_structure(input_path, date)
    elif option == "2":
        add_options_folders(input_path, date, ticker)
    else:
        print("Invalid option. Exiting...")


if __name__ == "__main__":
    run()
