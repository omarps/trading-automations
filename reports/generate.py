import os
from dotenv import load_dotenv
from utils import dates

from reports.pdt_pdf_report_generator import PdtPDFReportGenerator
from reports.pdt_yaml_report_generator import PdtYamlReportGenerator
from reports.pdts_yaml_report_generator import PdtsYamlReportGenerator
from reports.pdts_pdf_report_generator import PdtsPDFReportGenerator


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
        "3: Generate YAML (Week)\n"
        "4: Generate PDF (Week)\n"
    )

    if option == "1":
        report_generator = PdtYamlReportGenerator(base_path, date, ticker)
        report_generator.generate_report()
    elif option == "2":
        report_generator = PdtPDFReportGenerator(base_path, date, ticker)
        report_generator.generate_report()
    elif option == "3":
        report_generator = PdtsYamlReportGenerator(base_path, dates.get_date_param("week"), "PDTS")
        report_generator.generate_report()
    elif option == "4":
        report_generator = PdtsPDFReportGenerator(base_path, dates.get_date_param("week"), "PDTS")
        report_generator.generate_report()
    else:
        print("Invalid option. Exiting...")


if __name__ == "__main__":
    run()
