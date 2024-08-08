import os
import sys
from dotenv import load_dotenv
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from pdf_strategy.pdf_generator_context import PDFGeneratorContext
from pdf_strategy.generate_pdf_md_strategy import GeneratePDFMdStrategy
from pdf_strategy.generate_pdf_graphs_strategy import GeneratePDFGraphsStrategy
from pdf_strategy.generate_pdf_options_strategy import GeneratePDFOptionsStrategy
from pdf_strategy.generate_pdf_gammas_strategy import GeneratePDFGammasStrategy
from pdf_strategy.generate_pdf_screenshots_strategy import GeneratePDFScreenshotsStrategy


load_dotenv()


def generate_pdf(base_path, date, ticker = 'SPY'):
    print("Generating PDF file...")

    context = PDFGeneratorContext(GeneratePDFMdStrategy())
    context.generate_pdf(base_path, date, ticker)

    context = PDFGeneratorContext(GeneratePDFGraphsStrategy())
    context.generate_pdf(base_path, date, ticker)

    context = PDFGeneratorContext(GeneratePDFOptionsStrategy())
    context.generate_pdf(base_path, date, ticker)

    context = PDFGeneratorContext(GeneratePDFGammasStrategy())
    context.generate_pdf(base_path, date, ticker)

    context = PDFGeneratorContext(GeneratePDFScreenshotsStrategy())
    context.generate_pdf(base_path, date, ticker)

    _generate_pdf_merge(base_path, date, ticker)


def _pdf_filenames(base_path, date, ticker):
    file_path = os.path.join(base_path, date)
    pdf_files = {
        'md': os.path.join(file_path, f"{ticker}_{date}_summary_md.pdf"),
        'graphs': os.path.join(file_path, f"{ticker}_{date}_summary_graphs.pdf"),
        'options': os.path.join(file_path, f"{ticker}_{date}_summary_options.pdf"),
        'gammas': os.path.join(file_path, f"{ticker}_{date}_summary_gammas.pdf"),
        'screenshots': os.path.join(file_path, f"{ticker}_{date}_summary_screenshots.pdf")
    }
    return pdf_files


def _generate_pdf_merge(base_path, date, ticker):
    file_path = os.path.join(base_path, date)
    pdf_files = _pdf_filenames(base_path, date, ticker).values()

    # merge the pdf files using PyPDF2 classes
    merged_pdf = PdfWriter()
    for pdf_file in pdf_files:
        with open(pdf_file, 'rb') as file:
            pdf = PdfReader(file)
            for page in pdf.pages:
                merged_pdf.add_page(page)

    # Save merged PDF
    summary_filename = f"{ticker}_{date}_summary.pdf"
    merged_pdf_file_path = os.path.join(file_path, summary_filename)
    with open(merged_pdf_file_path, 'wb') as output_file:
        merged_pdf.write(output_file)
        print(f"{ticker} PDF File: {summary_filename}")

    # Cleanup pdf files
    for pdf_file in pdf_files:
        os.remove(pdf_file)
    print(f"Cleaning up PDF files: {len(pdf_files)}")


def run():
    # Use the first command-line argument if provided, otherwise use today's date in the format YYYYMMDD
    date = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y%m%d")
    base_path = os.getenv("BASE_PATH")
    ticker = os.getenv("TICKER")
    generate_pdf(base_path, date, ticker)


if __name__ == "__main__":
    run()
