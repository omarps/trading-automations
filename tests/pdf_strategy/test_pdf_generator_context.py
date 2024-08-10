import unittest
from pdf_strategy.pdf_generator_context import PDFGeneratorContext


class MockPDFGenerationStrategy:
    def __init__(self):
        self.generate_called = False
        self.base_path = None
        self.date = None
        self.ticker = None

    def generate(self, base_path, date, ticker):
        self.generate_called = True
        self.base_path = base_path
        self.date = date
        self.ticker = ticker


class TestPDFGeneratorContext(unittest.TestCase):
    def setUp(self):
        self.mock_strategy = MockPDFGenerationStrategy()
        self.context = PDFGeneratorContext(self.mock_strategy)

    def test_init(self):
        self.assertEqual(self.context._strategy, self.mock_strategy)

    def test_set_strategy(self):
        new_strategy = MockPDFGenerationStrategy()
        self.context.set_strategy(new_strategy)
        self.assertEqual(self.context._strategy, new_strategy)

    def test_generate_pdf(self):
        base_path = "/path/to/files"
        date = "2024-01-01"
        ticker = "SPY"
        self.context.generate_pdf(base_path, date, ticker)
        self.assertTrue(self.mock_strategy.generate_called)
        self.assertEqual(self.mock_strategy.base_path, base_path)
        self.assertEqual(self.mock_strategy.date, date)
        self.assertEqual(self.mock_strategy.ticker, ticker)


if __name__ == "__main__":
    unittest.main()
