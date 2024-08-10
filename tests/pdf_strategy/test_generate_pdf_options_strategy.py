import os
import unittest
from unittest.mock import patch
from pdf_strategy.generate_pdf_options_strategy import GeneratePDFOptionsStrategy


class TestGeneratePDFOptionsStrategy(unittest.TestCase):

    @patch('pdf_strategy.generate_pdf_options_strategy.PDFGenerationStrategy.__init__')
    def test_initialization(self, mock_super_init):
        mock_super_init.return_value = None
        strategy = GeneratePDFOptionsStrategy()
        self.assertEqual(strategy.section_name, 'options')
        self.assertEqual(strategy.folder_name, 'contratos')

    @patch('pdf_strategy.generate_pdf_options_strategy.PDFGenerationStrategy.generate')
    @patch('pdf_strategy.generate_pdf_options_strategy.GeneratePDFOptionsStrategy.get_yaml_data_by_section')
    @patch('pdf_strategy.generate_pdf_options_strategy.GeneratePDFOptionsStrategy._render_html_text')
    @patch('pdf_strategy.generate_pdf_options_strategy.GeneratePDFOptionsStrategy._write_pdf_file')
    def test_generate(self, mock_write_pdf, mock_render_html, mock_get_yaml, mock_super_generate):
        mock_super_generate.return_value = None
        mock_get_yaml.return_value = {
            'options': [
                {'option1': ['image1.png', 'image2.png']},
                {'option2': ['image3.png']}
            ]
        }
        mock_render_html.return_value = '<html></html>'

        strategy = GeneratePDFOptionsStrategy()
        strategy.full_path = '/test/path'
        strategy.generate('/base/path', '2023-10-01', 'TICKER')

        mock_super_generate.assert_called_once_with('/base/path', '2023-10-01', 'TICKER')
        mock_get_yaml.assert_called_once_with('options')
        mock_render_html.assert_called_once()
        mock_write_pdf.assert_called_once_with('<html></html>')


if __name__ == '__main__':
    unittest.main()