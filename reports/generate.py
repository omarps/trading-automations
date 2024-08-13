import os
import sys
from dotenv import load_dotenv
from datetime import datetime

from reports.pdf_report_generator import PDFReportGenerator
from reports.yaml_report_generator import YamlReportGenerator


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
        report_generator = YamlReportGenerator(base_path, date, ticker)
        report_generator.generate_report()
    elif option == "2":
        report_generator = PDFReportGenerator(base_path, date, ticker)
        report_generator.generate_report()
    else:
        print("Invalid option. Exiting...")


if __name__ == "__main__":
    run()
