import os
import yaml
from reports.report_generator import ReportGenerator
from utils.md import extract_contract_titles
from utils.constants import *
from reports.utils import get_image_paths


class YamlReportGenerator(ReportGenerator):
    """
    A class to generate YAML reports, inheriting from ReportGenerator.

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
        super().__init__(base_path, date, ticker)
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

        # Graphs section
        self._add_graphs_section()

        # Options section
        self._add_options_section()

        # Gammas section
        self._add_section(GAMMAS)

        # Screenshots section
        self._add_section(SCREENSHOTS)

        # Others section
        self._add_section(OTHERS)

    def write_report(self):
        """
        Writes the processed report data to a YAML file.

        This method creates the necessary directories and writes the data dictionary to a YAML file.
        """
        yaml_file_path = os.path.join(self.base_path, self.date, f"{self.ticker}_{self.date}_summary.yaml")
        os.makedirs(os.path.dirname(yaml_file_path), exist_ok=True)
        with open(yaml_file_path, 'w') as yaml_file:
            yaml.dump(self.data, yaml_file)
        print(f"YAML file created: {yaml_file_path}")

    def _full_path(self):
        """
        Returns the full path to the report directory.
        """
        return os.path.join(self.base_path, self.date)

    def _add_graphs_section(self):
        """
        Adds the graphs section to the report data.
        """
        full_path = self._full_path()
        graphs_path = os.path.join(full_path, GRAFICOS)
        graphs_section = {GRAPHS: []}
        if os.path.exists(graphs_path):
            graph_order = ["v1d", "ichim", "v5m", "v1m"]
            for prefix in graph_order:
                graph_files = [f for f in get_image_paths(graphs_path) if f"{prefix}" in os.path.basename(f)]
                graphs_section[GRAPHS].extend(map(os.path.basename, graph_files))
        self.data["sections"].append(graphs_section)

    def _add_options_section(self):
        """
        Adds the options section to the report data.
        """
        full_path = self._full_path()
        options_path = os.path.join(full_path, CONTRATOS)
        options_section = {OPTIONS: []}
        if os.path.exists(options_path):
            sorted_folders = extract_contract_titles(os.path.join(full_path, f"{self.ticker}_{self.date}_summary.md"))
            # TODO: use extract_contract_contents
            # TODO: Add summary seccion with screenshot
            sorted_folders = list(map(lambda title: title.lstrip('.'), sorted_folders))
            for option_folder in sorted_folders:
                # TODO: use option.yaml
                option_path = os.path.join(options_path, option_folder)
                if os.path.isdir(option_path):
                    option_data = {option_folder: [os.path.basename(path) for path in get_image_paths(option_path)]}
                    options_section[OPTIONS].append(option_data)
        self.data["sections"].append(options_section)

    def _add_section(self, section_name):
        """
        Adds a section to the report data.

        Args:
            section_name (str): The name of the section.
        """
        section_path = os.path.join(self._full_path(), section_name)
        section = {section_name: []}
        if os.path.exists(section_path):
            section[section_name] = [os.path.basename(path) for path in get_image_paths(section_path)]
        self.data["sections"].append(section)
