import os
import yaml
from reports.report_generator import ReportGenerator
from utils.constants import *
from reports.utils import get_image_paths


class PdtsYamlReportGenerator(ReportGenerator):
    """
        A class to generate  PDTS YAML reports, inheriting from ReportGenerator.

        Attributes:
            base_path (str): The base path where the report files are stored.
            date (str): The date for which the report is generated.
            ticker (str): The ticker symbol for the report. Default is 'SPY'.
            data (dict): A dictionary to store the report data.
        """

    def __init__(self, base_path, date, ticker='SPY'):
        """
        Initializes the YamlReportGenerator with the given base path, date, and ticker.

        Args:
            base_path (str): The base path where the report files are stored.
            date (str): The date for which the report is generated.
            ticker (str): The ticker symbol for the report. Default is 'SPY'.
        """
        super().__init__(base_path, date, ticker, "week")
        self.data = {}

    def process_report(self):
        """
        Processes the report data by populating the data dictionary with relevant information.

        This method constructs the report title, author, summary, and sections including graphs, options, gammas,
        screenshots, and others.
        """
        # TODO: Replace with report.sample.yaml
        self.data = {
            "title": f"{self.ticker} {self.date[:4]}-{self.date[4:6]}-{self.date[6:]}",
            "ticker": self.ticker,
            "date": self.date,
            "author": "Omar Palomino",
            "summary": f"{self.ticker}_{self.date}_summary.md",
            "sections": []
        }

        # TODO: Graphs section
        # self._add_graphs_section()

        # Screenshots section
        self._add_section(SCREENSHOTS)

        # Others section
        self._add_section(OTHERS)

    def write_report(self):
        """
        Writes the processed report data to a YAML file.

        This method creates the necessary directories and writes the data dictionary to a YAML file.
        """
        yaml_file_path = os.path.join(self.base_path, self.date + "-week", f"{self.ticker}_{self.date}_summary.yaml")
        os.makedirs(os.path.dirname(yaml_file_path), exist_ok=True)
        with open(yaml_file_path, 'w') as yaml_file:
            yaml.dump(self.data, yaml_file)
        print(f"YAML file created: {yaml_file_path}")

    def _add_section(self, section_name):
        """
        Adds a section to the report data.

        Args:
            section_name (str): The name of the section.
        """
        section_path = os.path.join(self.full_path(), section_name)
        section = {section_name: []}
        if os.path.exists(section_path):
            section[section_name] = [os.path.basename(path) for path in get_image_paths(section_path)]
        self.data["sections"].append(section)
