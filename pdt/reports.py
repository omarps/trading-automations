import os
import sys
import yaml
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from pdt.pdfpdt import PDFGeneratorContext, GeneratePDFMdStrategy, GeneratePDFGraphsStrategy, GeneratePDFOptionsStrategy, GeneratePDFGammasStrategy, GeneratePDFScreenshotsStrategy
from md_utils import extract_contract_titles


def _get_image_paths(folder_path):
    """Get all image paths in the specified folder."""
    image_paths = []
    for file in os.listdir(folder_path):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_paths.append(os.path.join(folder_path, file))
    return sorted(image_paths)

def generate_yaml(base_path, date):
    print("Generating YAML file...")
    full_path = os.path.join(base_path, date)
    data = {
        "title": f"SPY {date[:4]}-{date[4:6]}-{date[6:]}",
        "ticker": "SPY",  # Hardcoded for now, but can be extracted from the folder name
        "date": date,
        "author": "Omar Palomino",
        "summary": f"SPY_{date}_summary.md",
        "sections": []
    }

    # Graphs section
    graphs_path = os.path.join(full_path, "graficos")
    graphs_section = {"graphs": []}
    graph_order = ["v1d", "ichim", "v5m", "v1m"]

    for prefix in graph_order:
        graph_files = [f for f in _get_image_paths(graphs_path) if f"{prefix}" in os.path.basename(f)]
        for image_path in graph_files:
            filename = os.path.basename(image_path)
            graphs_section["graphs"].append(filename)

    data["sections"].append(graphs_section)

    # Options section
    options_path = os.path.join(full_path, "contratos")
    options_section = {"options": []}

    sorted_folders = extract_contract_titles(os.path.join(full_path, f"SPY_{date}_summary.md"))
    sorted_folders = list(map(lambda title: title.lstrip('.'), sorted_folders))

    for option_folder in sorted_folders:
        option_path = os.path.join(options_path, option_folder)
        if os.path.isdir(option_path):
            option_data = {option_folder: [os.path.basename(path) for path in _get_image_paths(option_path)]}
            options_section["options"].append(option_data)

    data["sections"].append(options_section)

    # Gammas section
    gammas_path = os.path.join(full_path, "gammas")
    gammas_section = {"gammas": [os.path.basename(path) for path in _get_image_paths(gammas_path)]}
    data["sections"].append(gammas_section)

    # Screenshots section
    screenshots_path = os.path.join(full_path, "screenshots")
    screenshots_section = {"screenshots": [os.path.basename(path) for path in _get_image_paths(screenshots_path)]}
    data["sections"].append(screenshots_section)

    yaml_file_path = os.path.join(full_path, f"SPY_{date}_summary.yaml")
    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)
    print(f"YAML file created: {yaml_file_path}")

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

if __name__ == "__main__":
    # Use the first command-line argument if provided, otherwise use today's date in the format YYYYMMDD
    date = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y%m%d")

    if len(sys.argv) > 2:
        base_path = sys.argv[2]
    else:
        base_path = "/Users/omarps/Library/CloudStorage/OneDrive-Personal/Proyectos/CDI/PDT/2024/2024q3"

    print(base_path)
    ticker = "SPY"
    generate_pdf(base_path, date, ticker)