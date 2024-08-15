import os
from PyPDF2 import PdfReader, PdfWriter
from reports.report_generator import ReportGenerator
from pdf_strategy.pdf_generator_context import PDFGeneratorContext
from pdf_strategy.generate_pdf_md_strategy import GeneratePDFMdStrategy
from pdf_strategy.generate_pdf_graphs_strategy import GeneratePDFGraphsStrategy
from pdf_strategy.generate_pdf_options_strategy import GeneratePDFOptionsStrategy
from pdf_strategy.generate_pdf_generic_strategy import GeneratePDFGenericStrategy
from utils.constants import *


class PDFReportGenerator(ReportGenerator):
    """
    A class to generate PDF reports, inheriting from ReportGenerator.

    Attributes:
        base_path (str): The base path where the report files are stored.
        date (str): The date for which the report is generated.
        ticker (str): The ticker symbol for the report. Default is 'SPY'.
        strategies (list): A list of strategies to generate different parts of the PDF report.
    """

    def __init__(self, base_path, date, ticker='SPY'):
        """
        Initializes the PDFReportGenerator with the given base path, date, and ticker.

        Args:
            base_path (str): The base path where the report files are stored.
            date (str): The date for which the report is generated.
            ticker (str): The ticker symbol for the report. Default is 'SPY'.
        """
        super().__init__(base_path, date, ticker)
        self.strategies = [
            GeneratePDFMdStrategy(),
            GeneratePDFGraphsStrategy(),
            GeneratePDFOptionsStrategy(),
            GeneratePDFGenericStrategy(GAMMAS),
            GeneratePDFGenericStrategy(SCREENSHOTS),
            GeneratePDFGenericStrategy(OTHERS)
        ]

    def process_report(self):
        """
        Processes the report data by applying each strategy to generate parts of the PDF report.

        This method iterates over the strategies and uses them to generate the PDF content.
        """
        print("Generating PDF file...")

        for strategy in self.strategies:
            context = PDFGeneratorContext(strategy)
            context.generate_pdf(self.base_path, self.date, self.ticker)

    def write_report(self):
        """
        Writes the processed report data to a single merged PDF file.

        This method merges individual PDF files generated by the strategies into a single PDF file.
        """
        file_path = os.path.join(self.base_path, self.date)
        pdf_files = self._report_filenames().values()

        # merge the pdf files using PyPDF2 classes
        merged_pdf = PdfWriter()
        for pdf_file in pdf_files:
            with open(pdf_file, 'rb') as file:
                reader = PdfReader(pdf_file)
                for page in reader.pages:
                    merged_pdf.add_page(page)

        # Save merged PDF
        summary_filename = f"{self.ticker}_{self.date}_summary.pdf"
        # os.makedirs(os.path.dirname(summary_filename), exist_ok=True)
        merged_pdf_file_path = os.path.join(file_path, summary_filename)
        with open(merged_pdf_file_path, 'wb') as output_file:
            merged_pdf.write(output_file)
            print(f"{self.ticker} PDF File: {summary_filename}")

        # Cleanup pdf files
        for pdf_file in pdf_files:
            os.remove(pdf_file)
        print(f"Cleaning up PDF files: {len(pdf_files)}")

    def _report_filenames(self):
        """
        Returns a dictionary of PDF filenames generated by the strategies.
        keys are the section names and values are the PDF filenames.
        """
        file_path = os.path.join(self.base_path, self.date)
        pdf_files = dict(
            map(
                lambda strategy: (strategy.section_name, os.path.join(file_path, strategy.summary_filename())),
                self.strategies
            )
        )
        return pdf_files
