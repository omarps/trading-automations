import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import shutil
from reports.pdf_report_generator import PDFReportGenerator


class TestPDFReportGenerator(unittest.TestCase):

    def setUp(self):
        self.base_path = 'test_reports'
        self.date = '20230101'
        self.ticker = 'SPY'
        os.makedirs(self.base_path, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.base_path)

    def test_initialization(self):
        generator = PDFReportGenerator(self.base_path, self.date, self.ticker)
        self.assertEqual(generator.base_path, self.base_path)
        self.assertEqual(generator.date, self.date)
        self.assertEqual(generator.ticker, self.ticker)
        self.assertEqual(len(generator.strategies), 5)

    @patch('reports.pdf_report_generator.PDFGeneratorContext')
    def test_process_report(self, MockPDFGeneratorContext):
        mock_context = MockPDFGeneratorContext.return_value
        generator = PDFReportGenerator(self.base_path, self.date, self.ticker)
        generator.process_report()
        self.assertEqual(mock_context.generate_pdf.call_count, 5)

    @patch('reports.pdf_report_generator.PdfWriter')
    @patch('reports.pdf_report_generator.PdfReader')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    @patch('os.remove')
    def test_write_report(self, mock_remove, mock_makedirs, mock_open, MockPdfReader, MockPdfWriter):
        generator = PDFReportGenerator(self.base_path, self.date, self.ticker)
        generator._report_filenames = MagicMock(return_value={'part1': 'file1.pdf', 'part2': 'file2.pdf'})

        # Mock the PdfReader to avoid FileNotFoundError
        mock_pdf_reader_instance = MockPdfReader.return_value
        mock_pdf_reader_instance.pages = [MagicMock(), MagicMock()]

        # Mock the open function to simulate file presence
        m_open = mock_open()
        mock_open.side_effect = [
            m_open.return_value,
            m_open.return_value,
            m_open.return_value,
            m_open.return_value
        ]

        generator.write_report()

        self.assertTrue(mock_open.called)
        self.assertTrue(MockPdfWriter.return_value.write.called)
        self.assertTrue(MockPdfReader.called)


if __name__ == '__main__':
    unittest.main()