from pdf_strategy.pdf_generation_strategy import PDFGenerationStrategy


class PDFGeneratorContext:
    def __init__(self, strategy: PDFGenerationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: PDFGenerationStrategy):
        self._strategy = strategy

    def generate_pdf(self, base_path, date, ticker):
        self._strategy.generate(base_path, date, ticker)
