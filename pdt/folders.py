import os
import sys
import shutil
from datetime import datetime
from dotenv import load_dotenv
from md_utils import extract_contract_titles


load_dotenv()

def create_folder_structure(base_path, date):
    # Define the folder structure
    folder_structure = ["graficos", "contratos", "gammas", "screenshots"]
    graphs_structure = ["v1d", "ichim", "v5m", "v1m"]

    # Create the base directory if it does not exist
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    # Create the folder structure
    for folder in folder_structure:
        folder_path = os.path.join(base_path, folder)
        create_or_clear_folder(folder_path)

        if folder == "graficos":
            for graph in graphs_structure:
                graph_path = os.path.join(folder_path, graph)
                create_or_clear_folder(graph_path)

    # Find any MD file and remove them.
    for file in os.listdir(base_path):
        if file.endswith(".md"):
            os.remove(os.path.join(base_path, file))

    # Add a summary file to the folder
    # with name format SPY_{date}_summary.md
    # based on the summary.sample.md file
    summary_file = os.path.join(base_path, f"SPY_{date}_summary.md")
    if not os.path.exists(summary_file):
        sample_md = os.path.join(os.path.dirname(__file__), "../templates", "summary.sample.md")
        with open(sample_md, "r") as f:
            content = f.read()
            content = content.replace("{{date}}", f"<u>{date}</u>")
            with open(summary_file, "w") as f:
                f.write(content)

        print(f"Folder structure created at: {base_path}")
    else:
        print(f"Folder structure already exists at {base_path}")


def create_or_clear_folder(folder_path):
    if not os.path.exists(folder_path):
        # create folder
        os.makedirs(folder_path)
    else:
        # clear folder contents
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isdir(file_path):
                # if is folder remove it recursively
                shutil.rmtree(file_path)
            else:
                # remove file
                os.remove(file_path)

def add_options_folders(input_path, date, ticker):
    sorted_folders = extract_contract_titles(os.path.join(input_path, f"SPY_{date}_summary.md"))
    sorted_folders = list(map(lambda title: title.lstrip('.'), sorted_folders))

    options_path = os.path.join(input_path, "contratos")
    for option_folder in sorted_folders:
        option_path = os.path.join(options_path, option_folder)
        if not os.path.exists(option_path):
            os.makedirs(option_path)
            print(f"Created {option_path}")

def add_options_to_contracts_monthly_summary(input_path, date, ticker):
    sorted_folders = extract_contract_titles(os.path.join(input_path, f"SPY_{date}_summary.md"))
    sorted_folders = list(map(lambda title: title.lstrip('.'), sorted_folders))

    # TODO: Add to contratos.txt or contratos.md?

if __name__ == "__main__":
    # Use the first command-line argument if provided, otherwise use today's date in the format YYYYMMDD
    date = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y%m%d")

    input_path = os.getenv("INPUT_PATH")
    ticker = os.getenv("TICKER")

    # TODO: add running option?
    # create_folder_structure(input_path, date)
    add_options_folders(input_path, date, ticker)
