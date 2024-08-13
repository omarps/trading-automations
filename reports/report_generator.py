class ReportGenerator:
    """
    A base class for generating reports.

    Attributes:
        base_path (str): The base path where the report files are stored.
        date (str): The date for which the report is generated.
        ticker (str): The ticker symbol for the report. Default is 'SPY'.
    """

    def __init__(self, base_path, date, ticker='SPY'):
        """
        Initializes the ReportGenerator with the given base path, date, and ticker.

        Args:
            base_path (str): The base path where the report files are stored.
            date (str): The date for which the report is generated.
            ticker (str): The ticker symbol for the report. Default is 'SPY'.
        """
        self.base_path = base_path
        self.date = date
        self.ticker = ticker

    def generate_report(self):
        """
        Generates the report by processing and writing it.

        This method calls the process_report and write_report methods.
        """
        self.process_report()
        self.write_report()

    def process_report(self):
        """
        Processes the report data.

        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method")

    def write_report(self):
        """
        Writes the report to a file.

        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method")
