import os
from dotenv import load_dotenv
from utils import dates

from reports.pdf_report_generator import PDFReportGenerator
from reports.yaml_report_generator import YamlReportGenerator


load_dotenv()


def run():
    date = dates.get_date_param()
    base_path = os.getenv("BASE_PATH")
    ticker = os.getenv("TICKER")

    # Ask for which option to run for reports
    option = input(
        "Which report do you want to run?\n"
        "1: Generate YAML (PDT)\n"
        "2: Generate PDF (PDT)\n"
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
