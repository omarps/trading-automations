import os
import re
import yaml
from reports.report_generator import ReportGenerator
from utils.md import extract_contract_titles, extract_contract_contents
from utils.constants import *
from reports.utils import get_image_paths


# Regular expression patterns to extract the required variables
qty_pattern = re.compile(r"Qty:\s*(\d+)")
price_pattern = re.compile(r"Price:\s*([\d.]+)")
# risk_pattern = re.compile(r"Risk:\s*([\d.]+)")
target_pattern = re.compile(r"Target:\s*(\w+)")
max_pattern = re.compile(r"Max:\s*([\d.]+)")


def contract_transactions(contract_data, option_folder):
    transactions = contract_data[option_folder] if contract_data[option_folder] else ""
    return transactions


def format_strike(qty, price, target, max_value):
    return f"- Qty: {qty}, Price: {price}, 50%: {round(price + 0.6, 2)}, 30%: {round(price + 1.0, 2)}, 20%: {max_value} * [{target}]"


def contract_strikes(transactions):
    # Extracting the values using the regex patterns
    qtys = qty_pattern.findall(transactions)
    prices = price_pattern.findall(transactions)
    # risks = risk_pattern.findall(transactions)
    targets = target_pattern.findall(transactions)
    max_values = max_pattern.findall(transactions)

    strike_array = []
    for i, _qty in enumerate(qtys):
        qty = int(qtys[i])
        price = float(prices[i])
        target = targets[i]
        max_value = float(max_values[i])
        strike_array.append(format_strike(qty, price, target, max_value))

    return '<br/>'.join(strike_array) if strike_array else ""


class PdtYamlReportGenerator(ReportGenerator):
    """
    A class to generate PDT YAML reports, inheriting from ReportGenerator.

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

    def _add_graphs_section(self):
        """
        Adds the graphs section to the report data.
        """
        full_path = self.full_path()
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
        full_path = self.full_path()
        options_path = os.path.join(full_path, CONTRATOS)
        options_section = {OPTIONS: []}
        if os.path.exists(options_path):
            summary_path = os.path.join(full_path, f"{self.ticker}_{self.date}_summary.md")
            sorted_folders = extract_contract_titles(summary_path)

            contract_data = extract_contract_contents(summary_path)

            sorted_folders = list(map(lambda title: title.lstrip('.'), sorted_folders))
            for option_folder in sorted_folders:
                option_data = {"name": option_folder}
                option_path = os.path.join(options_path, option_folder)
                if os.path.isdir(option_path):
                    option_data["images"] = [os.path.basename(path) for path in get_image_paths(option_path)]
                    transactions = contract_transactions(contract_data, option_folder)
                    option_data["transactions"] = transactions

                    option_data["strikes"] = contract_strikes(transactions)

                    options_section[OPTIONS].append(option_data)
        self.data["sections"].append(options_section)

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
