import os
import sys
from dotenv import load_dotenv
from datetime import datetime
from reports.yamls import generate_yaml
from reports.pdfs import generate_pdf


load_dotenv()


def run():
    # Use the first command-line argument if provided, otherwise use today's date in the format YYYYMMDD
    date = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y%m%d")
    base_path = os.getenv("BASE_PATH")
    ticker = os.getenv("TICKER")

    # Ask for which option to run for reports
    option = input(
        "Which report do you want to run?\n"
        "1: Generate YAML\n"
        "2: Generate PDF\n"
    )

    if option == "1":
        generate_yaml(base_path, date)
    elif option == "2":
        generate_pdf(base_path, date, ticker)
    else:
        print("Invalid option. Exiting...")


if __name__ == "__main__":
    run()
