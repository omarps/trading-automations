import os
import locale
import inflect
import string
import yfinance as yf
from datetime import datetime
from dotenv import load_dotenv
from folders.utils import create_or_clear_folder
from utils.dates import get_date_param
from utils.md import extract_contract_titles
from utils.constants import *


load_dotenv()


# TODO: move to utils to reuse?
def titleize_and_pluralize(section_name):
    p = inflect.engine()
    titleized = string.capwords(section_name)
    # pluralized = p.plural(titleized)
    # return pluralized
    return titleized


# TODO: move to utils to reuse?
def get_current_vix_value():
    # Fetch VIX data from Yahoo Finance
    vix = yf.Ticker("^VIX")
    vix_data = vix.history(period="1d")

    # Get the last closing price
    if not vix_data.empty:
        current_vix_value = vix_data['Close'].iloc[-1]
        return current_vix_value
    else:
        raise ValueError("No data found for VIX")


# Get the weekday event:
# - MMJ: From Tuesday or Wednesday
# - VL: Friday or Monday
# - STA: Thursday
def get_weekday_event(date):
    weekday_event = "MMJ" if datetime.strptime(date, "%Y%m%d").weekday() in [1, 2]\
        else "VL" if datetime.strptime(date, "%Y%m%d").weekday() in [4, 0]\
        else "STA"
    return weekday_event


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

        weekday_event = get_weekday_event(date)
        content = content.replace("{{weekday_event}}", f"{weekday_event}")

        # Get the VIX value for the date
        vix_value = get_current_vix_value()
        content = content.replace("{{vix}}", str(round(vix_value, 2)))

        # Set the locale to spanish
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        # Get the weekday for the date in spanish
        weekday = datetime.strptime(date, "%Y%m%d").strftime("%A")
        content = content.replace("{{weekday}}", f"<u>{titleize_and_pluralize(weekday)}</u>")

        with open(summary_file, "w") as f:
            f.write(content)

    print(f"Folder structure created at: {base_path}")


def create_folder_structure_week(base_path, date):
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
    folder_structure = [GRAFICOS, SCREENSHOTS, OTHERS]

    # Create the folder structure
    for folder in folder_structure:
        folder_path = os.path.join(base_path, folder)
        create_or_clear_folder(folder_path)

    # Add a summary file to the folder
    # with name format pdts_{date}_summary.md
    # based on the summary.sample.utils file
    summary_file = os.path.join(base_path, f"pdts_{date}_summary.md")
    sample_md = os.path.join(os.path.dirname(__file__), "../templates", "pdts_summary.sample.md")
    with open(sample_md, "r") as f:
        content = f.read()

        content = content.replace("{{date}}", f"<u>{date}</u>")

        with open(summary_file, "w") as f:
            f.write(content)

    print(f"Folder structure created at: {base_path}")



def extract_contract_details(contract, ticker="SPY"):
    # Assuming the contract format is "TICKER DATE C/P STRIKE"
    if not contract.startswith(ticker) or len(contract) < len(ticker) + 8:
        raise ValueError(f"Invalid contract format: {contract}")

    date = contract[len(ticker):len(ticker) + 6]
    call_put = "Call" if contract[len(ticker) + 6].upper() == "C" else "Put"
    strike = contract[len(ticker) + 7:]
    return date, call_put, strike


def create_option_yaml(output_path, folder_name, ticker, contract):
    # Read the template file
    template_path = os.path.join(os.path.dirname(__file__), "../templates", "option.sample.yaml")
    with open(template_path, "r") as template_file:
        content = template_file.read()

    try:
        # Extract details from contract
        date, call_put, strike = extract_contract_details(contract, ticker)
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Replace placeholders with actual values
    content = content.replace("{{date}}", date)
    content = content.replace("{{ticker}}", ticker)
    content = content.replace("{{contract}}", contract)
    content = content.replace("{{strike}}", strike)
    content = content.replace("{{call_put}}", call_put)

    # Write the content to a new YAML file using the folder name
    output_file_path = os.path.join(output_path, f"{folder_name}.yaml")
    with open(output_file_path, "w") as output_file:
        output_file.write(content)

    print(f"YAML file created at: {output_file_path}")


def add_options_folders(input_path, date, ticker):
    sorted_folders = extract_contract_titles(os.path.join(input_path, f"SPY_{date}_summary.md"))
    sorted_folders = list(map(lambda title: title.lstrip('.'), sorted_folders))

    # Ask if you want to overwrite or exit
    options_path = os.path.join(input_path, CONTRATOS)
    if os.path.exists(options_path):
        overwrite = input(f"Options folders already exist at {options_path}. Do you want to overwrite it? (y/n): ")
        if overwrite.lower() != "y":
            print("Exiting...")
            return

    create_or_clear_folder(options_path)

    for option_folder in sorted_folders:
        option_path = os.path.join(options_path, option_folder)

        if not os.path.exists(option_path):
            os.makedirs(option_path)

            create_option_yaml(option_path, option_folder, ticker, option_folder)

            print(f"Created {option_path}")


def run():
    date = get_date_param()
    input_path = os.getenv("INPUT_PATH")
    week_path = os.getenv("WEEK_PATH")
    ticker = os.getenv("TICKER")

    # Ask for which folder option to run and execute based on the input
    option = input(
        "Which option do you want to run?\n"
        "1: Create folder structure (PDT)\n"
        "2: Add options folder (PDT)s\n"
        "3: Create folder structure (Week1)\n"
    )
    if option == "1":
        create_folder_structure(input_path, date)
    elif option == "2":
        add_options_folders(input_path, date, ticker)
    elif option == "3":
        create_folder_structure_week(week_path, date)
    else:
        print("Invalid option. Exiting...")


if __name__ == "__main__":
    run()
