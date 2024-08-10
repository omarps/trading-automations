import unittest
from unittest.mock import patch, mock_open, MagicMock
from pdf_strategy.pdf_generation_strategy import PDFGenerationStrategy


class MockPDFGenerationStrategy(PDFGenerationStrategy):
    def __init__(self):
        super().__init__()
        self.pdf_filename = None

    def generate(self, base_path, date, ticker):
        pass


class TestPDFGenerationStrategy(unittest.TestCase):
    def setUp(self):
        self.strategy = MockPDFGenerationStrategy()

    def test_set_section_attributes(self):
        self.strategy.set_section_attributes("summary", "folder")
        self.assertEqual(self.strategy.section_name, "summary")
        self.assertEqual(self.strategy.folder_name, "folder")

    @patch("builtins.open", new_callable=mock_open, read_data="sections:\n  - summary: data")
    @patch("os.path.join", return_value="fake_path")
    @patch("yaml.safe_load", return_value={"sections": [{"summary": "data"}]})
    def test_get_yaml_data_by_section(self, mock_join, mock_safe_load, mock_open):
        section_data = self.strategy.get_yaml_data_by_section("summary")
        self.assertEqual(section_data, {"summary": "data"})

    @patch("os.path.join", return_value="fake_path")
    def test_template_options(self, mock_join):
        options = self.strategy._template_options()
        self.assertIn("enable-local-file-access", options)
        self.assertIn("user-style-sheet", options)

    @patch("pdf_strategy.pdf_generation_strategy.Environment.get_template")
    @patch("os.path.join", return_value="fake_path")
    def test_render_html_text(self, mock_join, mock_get_template):
        mock_template = MagicMock()
        mock_template.render.return_value = "rendered_html"
        mock_get_template.return_value = mock_template

        html_text = self.strategy._render_html_text("summary", {"key": "value"})
        self.assertEqual(html_text, "rendered_html")

    @patch("pdfkit.from_string")
    @patch("os.path.join", return_value="fake_path")
    def test_write_pdf_file(self, mock_join, mock_from_string):
        self.strategy._write_pdf_file("html_text")
        mock_from_string.assert_called_once()


if __name__ == "__main__":
    unittest.main()
