from pdf_strategy.pdf_generation_strategy import PDFGenerationStrategy


class PDFGeneratorContext:
    """
    The PDFGeneratorContext class is responsible for managing the PDF generation strategy.
    It allows setting different strategies for generating PDFs and uses the current strategy
    to generate PDFs based on the provided parameters.

    Attributes:
        _strategy (PDFGenerationStrategy): The current strategy used for generating PDFs.

    Methods:
        __init__(strategy: PDFGenerationStrategy):
            Initializes the PDFGeneratorContext with a specific PDF generation strategy.

        set_strategy(strategy: PDFGenerationStrategy):
            Sets a new strategy for generating PDFs.

        generate_pdf(base_path: str, date: str, ticker: str):
            Generates a PDF using the current strategy with the provided base path, date, and ticker.
    """

    def __init__(self, strategy: PDFGenerationStrategy):
        """
        Initializes the PDFGeneratorContext with a specific PDF generation strategy.

        Args:
            strategy (PDFGenerationStrategy): The strategy to be used for generating PDFs.
        """
        self._strategy = strategy

    def set_strategy(self, strategy: PDFGenerationStrategy):
        """
        Sets a new strategy for generating PDFs.

        Args:
            strategy (PDFGenerationStrategy): The new strategy to be used for generating PDFs.
        """
        self._strategy = strategy

    def generate_pdf(self, base_path, date, ticker):
        """
        Generates a PDF using the current strategy with the provided base path, date, and ticker.

        Args:
            base_path (str): The base path where the PDF files are located.
            date (str): The date to be used in the PDF generation.
            ticker (str): The ticker symbol to be used in the PDF generation.
        """
        self._strategy.generate(base_path, date, ticker)
