import os
import yaml
import pdfkit
from abc import ABC, abstractmethod
from jinja2 import Environment, FileSystemLoader, TemplateError


class PDFGenerationStrategy(ABC):
    """
    Abstract base class for generating PDF reports.

    This class provides a template for generating PDF reports for a given ticker and date.
    Subclasses must implement the `generate` method to handle the specifics of PDF creation
    and saving. The class also provides utility methods and attributes to assist in the
    PDF generation process.

    Attributes:
        base_path (str): The base directory path where the PDF will be saved.
        date (str): The date for which the report is generated, in 'YYYYMMDD' format.
        ticker (str): The ticker symbol for which the report is generated.
        section_name (str): The section name for which the report is generated.
        folder_name (str): The folder name for which the report is generated.
        full_path (str): The full file path where the PDF will be saved.
        pdf_template (str): The template to be used for generating the PDF report.
    """

    def __init__(self):
        self.base_path = None
        self.date = None
        self.ticker = None
        self.section_name = None
        self.folder_name = None
        self.full_path = None
        self.pdf_template = None

    def set_section_attributes(self, section_name, folder_name=None):
        """
        Sets the section attributes for generating the PDF report.

        Args:
            section_name (str): The section name for which the report is generated.
            folder_name (str, optional): The folder name for which the report is generated.
        """
        self.section_name = section_name
        self.folder_name = folder_name

    @abstractmethod
    def generate(self, base_path, date, ticker):
        """
        Generates a PDF report for a given ticker and date.

        This is an abstract method that must be implemented by subclasses to generate
        a PDF report. The implementation should handle the creation and saving of the
        PDF file based on the provided parameters.

        Args:
            base_path (str): The base directory path where the PDF will be saved.
            date (str): The date for which the report is generated, in 'YYYYMMDD' format.
            ticker (str): The ticker symbol for which the report is generated.

        Returns:
            None
        """
        self.base_path = base_path
        self.date = date
        self.ticker = ticker

        # processed values
        self.full_path = os.path.join(base_path, date)
        self.pdf_filename = f"{ticker}_{date}_summary_{self.section_name}.pdf"

        pass

    def get_yaml_data_by_section(self, section_name):
        """
        Retrieves data from a YAML file for a specified section.

        Args:
            section_name (str): The name of the section to retrieve from the YAML file.

        Returns:
            dict: A dictionary containing the data for the specified section.

        Raises:
            KeyError: If the specified section is not found in the YAML file.
            FileNotFoundError: If the YAML file does not exist.
            yaml.YAMLError: If there is an error parsing the YAML file.
        """
        # Method implementation here
        yaml_file_path = os.path.join(self.full_path, f"{self.ticker}_{self.date}_summary.yaml")
        with open(yaml_file_path, 'r') as file:
            summary_data = yaml.safe_load(file)

        # get section data from summary_data['sections'] array
        section_data = next((section for section in summary_data['sections'] if section_name in section), None)
        return section_data

    @staticmethod
    def _template_options():
        """
        Provides a dictionary of template options for PDF generation.

        This function returns a dictionary containing various options that can be used
        to customize the PDF generation process. These options may include settings
        for margins, page size, orientation, and other relevant parameters.

        Returns:
            dict: A dictionary containing template options for PDF generation.
        """
        # Method implementation here
        # Specify the path to your custom CSS file
        css_path = os.path.join(os.path.dirname(__file__), "../templates", "styles.css")

        options = {
            'enable-local-file-access': True,
            'user-style-sheet': css_path
        }
        return options

    def _render_html_text(self, section_name, data):
        """
        Renders HTML text for a specified section using provided data.

        Args:
            section_name (str): The name of the section to render.
            data (dict): A dictionary containing the data to be used for rendering the HTML text.

        Returns:
            str: A string containing the rendered HTML text.

        Raises:
            KeyError: If the specified section is not found in the data.
            TemplateError: If there is an error in the HTML template rendering process.
        """
        try:
            # Method implementation here
            templates_path = os.path.join(os.path.dirname(__file__), "../templates")
            env = Environment(loader=FileSystemLoader(templates_path))
            template = env.get_template(f"{section_name}.html")

            # Render the template with the graphs variable
            html_text = template.render(ticker=self.ticker, section_name=section_name, data=data, enumerate=enumerate)
            return html_text
        except KeyError as e:
            print(f"KeyError: {e} - The section '{section_name}' was not found in the data.")
            raise
        except TemplateError as e:
            print(f"TemplateError: {e} - There was an error rendering the template for section '{section_name}'.")

    # TODO: Add error handling for PDF file writing
    def _write_pdf_file(self, html_text):
        """
        Writes the provided HTML text to a PDF file.

        Args:
            html_text (str): The HTML content to be written to the PDF file.

        Returns:
            None
        """
        # Method implementation here
        options = self._template_options()
        # Generate the PDF file
        pdfkit.from_string(html_text, os.path.join(self.full_path, self.pdf_filename), options=options)
        # Print the PDF file name
        print(f"MD PDF File: {self.pdf_filename}")
