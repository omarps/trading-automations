import unittest
from reports.report_generator import ReportGenerator


class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        self.report_generator = ReportGenerator(base_path='/path/to/base', date='20230101')

    def test_generate_report(self):
        with self.assertRaises(NotImplementedError):
            self.report_generator.generate_report()

    def test_process_report(self):
        with self.assertRaises(NotImplementedError):
            self.report_generator.process_report()

    def test_write_report(self):
        with self.assertRaises(NotImplementedError):
            self.report_generator.write_report()


if __name__ == '__main__':
    unittest.main()