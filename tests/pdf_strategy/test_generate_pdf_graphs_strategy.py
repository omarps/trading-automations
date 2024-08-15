import os
import unittest
from unittest.mock import patch
from pdf_strategy.generate_pdf_graphs_strategy import GeneratePDFGraphsStrategy
from utils.constants import GRAPHS, GRAFICOS


class TestGeneratePDFGraphsStrategy(unittest.TestCase):

    @patch('pdf_strategy.generate_pdf_graphs_strategy.PDFGenerationStrategy.__init__')
    def test_initialization(self, mock_super_init):
        mock_super_init.return_value = None
        strategy = GeneratePDFGraphsStrategy()
        self.assertEqual(strategy.section_name, GRAPHS)
        self.assertEqual(strategy.folder_name, GRAFICOS)

    @patch('pdf_strategy.generate_pdf_graphs_strategy.PDFGenerationStrategy.generate')
    @patch('pdf_strategy.generate_pdf_graphs_strategy.GeneratePDFGraphsStrategy.get_yaml_data_by_section')
    @patch('pdf_strategy.generate_pdf_graphs_strategy.rotate_image')
    @patch('pdf_strategy.generate_pdf_graphs_strategy.GeneratePDFGraphsStrategy._render_html_text')
    @patch('pdf_strategy.generate_pdf_graphs_strategy.GeneratePDFGraphsStrategy._write_pdf_file')
    def test_generate(self, mock_write_pdf, mock_render_html, mock_rotate_image, mock_get_yaml, mock_super_generate):
        mock_super_generate.return_value = None
        mock_get_yaml.return_value = {
            GRAPHS: ['graph1.png', 'graph2_v1m.png']
        }
        mock_render_html.return_value = '<html></html>'

        strategy = GeneratePDFGraphsStrategy()
        strategy.full_path = '/test/path'
        strategy.generate('/base/path', '2023-10-01', 'TICKER')

        mock_super_generate.assert_called_once_with('/base/path', '2023-10-01', 'TICKER')
        mock_get_yaml.assert_called_once_with(GRAPHS)
        mock_rotate_image.assert_called_once_with('/test/path/graficos/graph2_v1m.png', '/test/path/graficos/graph2_v1m_rotated.png', -90)
        mock_render_html.assert_called_once()
        mock_write_pdf.assert_called_once_with('<html></html>')

    @patch('os.path.exists')
    @patch('os.remove')
    @patch('resources.images.rotate_image')
    def test_image_rotation(self, mock_rotate_image, mock_remove, mock_exists):
        mock_exists.side_effect = lambda path: path.endswith('_rotated.png')
        strategy = GeneratePDFGraphsStrategy()
        strategy.full_path = '/test/path'
        graph_array = [
            {'image_name': 'graph1.png', 'image_path': 'file:///test/path/graficos/graph1.png', 'rotate_90': False,
            'class_name': 'single-page'},
            {'image_name': 'graph2_v1m.png', 'image_path': 'file:///test/path/graficos/graph2_v1m.png',
            'rotate_90': True, 'class_name': 'single-page'}
        ]

        for graph in graph_array:
            if graph['rotate_90']:
                image_path = graph['image_path'].replace('file://', '')
                rotated_image_path = image_path.replace('.png', '_rotated.png')
                if os.path.exists(rotated_image_path):
                    os.remove(rotated_image_path)
                mock_rotate_image(image_path, rotated_image_path, -90)
                graph['image_path'] = f'file://{rotated_image_path}'
                graph['class_name'] = 'full-90deg'

        mock_exists.assert_called_once_with('/test/path/graficos/graph2_v1m_rotated.png')
        mock_remove.assert_called_once_with('/test/path/graficos/graph2_v1m_rotated.png')
        mock_rotate_image.assert_called_once_with('/test/path/graficos/graph2_v1m.png',
                                                '/test/path/graficos/graph2_v1m_rotated.png', -90)


if __name__ == '__main__':
    unittest.main()