import unittest
from unittest.mock import patch
from pdf_strategy.generate_pdf_screenshots_strategy import GeneratePDFScreenshotsStrategy


class TestGeneratePDFScreenshotsStrategy(unittest.TestCase):

    @patch('pdf_strategy.generate_pdf_screenshots_strategy.PDFGenerationStrategy.__init__')
    def test_initialization(self, mock_super_init):
        mock_super_init.return_value = None
        strategy = GeneratePDFScreenshotsStrategy()
        self.assertEqual(strategy.section_name, 'screenshots')
        self.assertEqual(strategy.folder_name, 'screenshots')

    @patch('pdf_strategy.generate_pdf_screenshots_strategy.PDFGenerationStrategy.generate')
    @patch('pdf_strategy.generate_pdf_screenshots_strategy.GeneratePDFScreenshotsStrategy.get_yaml_data_by_section')
    @patch('pdf_strategy.generate_pdf_screenshots_strategy.GeneratePDFScreenshotsStrategy._render_html_text')
    @patch('pdf_strategy.generate_pdf_screenshots_strategy.GeneratePDFScreenshotsStrategy._write_pdf_file')
    def test_generate(self, mock_write_pdf, mock_render_html, mock_get_yaml, mock_super_generate):
        mock_super_generate.return_value = None
        mock_get_yaml.return_value = {
            'screenshots': ['screenshot1.png', 'screenshot2.png']
        }
        mock_render_html.return_value = '<html></html>'

        strategy = GeneratePDFScreenshotsStrategy()
        strategy.full_path = '/test/path'
        strategy.generate('/base/path', '2023-10-01', 'TICKER')

        mock_super_generate.assert_called_once_with('/base/path', '2023-10-01', 'TICKER')
        mock_get_yaml.assert_called_once_with('screenshots')
        mock_render_html.assert_called_once()
        mock_write_pdf.assert_called_once_with('<html></html>')


if __name__ == '__main__':
    unittest.main()