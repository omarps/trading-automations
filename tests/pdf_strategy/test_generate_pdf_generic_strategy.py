import unittest
from unittest.mock import patch
from pdf_strategy.generate_pdf_generic_strategy import GeneratePDFGenericStrategy
from utils.constants import SCREENSHOTS


class TestGeneratePDFScreenshotsStrategy(unittest.TestCase):

    @patch('pdf_strategy.generate_pdf_generic_strategy.PDFGenerationStrategy.__init__')
    def test_initialization(self, mock_super_init):
        mock_super_init.return_value = None
        strategy = GeneratePDFGenericStrategy(SCREENSHOTS, SCREENSHOTS)
        self.assertEqual(strategy.section_name, SCREENSHOTS)
        self.assertEqual(strategy.folder_name, SCREENSHOTS)

    @patch('pdf_strategy.generate_pdf_generic_strategy.PDFGenerationStrategy.generate')
    @patch('pdf_strategy.generate_pdf_generic_strategy.GeneratePDFGenericStrategy.get_yaml_data_by_section')
    @patch('pdf_strategy.generate_pdf_generic_strategy.GeneratePDFGenericStrategy._render_html_text')
    @patch('pdf_strategy.generate_pdf_generic_strategy.GeneratePDFGenericStrategy._write_pdf_file')
    def test_generate(self, mock_write_pdf, mock_render_html, mock_get_yaml, mock_super_generate):
        mock_super_generate.return_value = None
        mock_get_yaml.return_value = {
            SCREENSHOTS: ['screenshot1.png', 'screenshot2.png']
        }
        mock_render_html.return_value = '<html></html>'

        strategy = GeneratePDFGenericStrategy(SCREENSHOTS, SCREENSHOTS)
        strategy.full_path = '/test/path'
        strategy.generate('/base/path', '2023-10-01', 'TICKER')

        mock_super_generate.assert_called_once_with('/base/path', '2023-10-01', 'TICKER')
        mock_get_yaml.assert_called_once_with(SCREENSHOTS)
        mock_render_html.assert_called_once()
        mock_write_pdf.assert_called_once_with('<html></html>')


if __name__ == '__main__':
    unittest.main()