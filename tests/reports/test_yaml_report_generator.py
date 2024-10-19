import unittest
from unittest.mock import patch, mock_open
import os
import yaml
from reports.pdt_yaml_report_generator import PdtYamlReportGenerator

class TestYamlReportGenerator(unittest.TestCase):
    def setUp(self):
        self.base_path = '/path/to/base'
        self.date = '20230101'
        self.ticker = 'SPY'
        self.report_generator = PdtYamlReportGenerator(self.base_path, self.date, self.ticker)

    def test_process_report(self):
        self.report_generator.process_report()
        expected_data = {
            "title": "SPY 2023-01-01",
            "ticker": "SPY",
            "date": "20230101",
            "author": "Omar Palomino",
            "summary": "SPY_20230101_summary.md",
            "sections": [
                {"graphs": []},
                {"options": []},
                {"gammas": []},
                {"screenshots": []},
                {"others": []}
            ]
        }
        self.assertEqual(self.report_generator.data, expected_data)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    def test_write_report(self, mock_makedirs, mock_open):
        self.report_generator.process_report()
        self.report_generator.write_report()

        yaml_file_path = os.path.join(self.base_path, self.date, f"{self.ticker}_{self.date}_summary.yaml")

        # Check if os.makedirs was called with the correct path
        mock_makedirs.assert_called_once_with(os.path.dirname(yaml_file_path), exist_ok=True)

        # Check if open was called with the correct path and mode
        mock_open.assert_called_once_with(yaml_file_path, 'w')

        # Check the content written to the file
        handle = mock_open()
        written_content = ''.join(call[0][0] for call in handle.write.call_args_list)
        expected_content = yaml.dump(self.report_generator.data)
        self.assertEqual(written_content, expected_content)

if __name__ == '__main__':
    unittest.main()