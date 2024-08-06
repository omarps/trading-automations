import os
from pdf_generation_strategy import PDFGenerationStrategy
from resources import rotate_image


class GeneratePDFGraphsStrategy(PDFGenerationStrategy):
    def __init__(self):
        super().__init__()
        self.set_section_attributes('graphs', 'graficos')

    def generate(self, base_path, date, ticker):
        super().generate(base_path, date, ticker)

        # Read YAML file
        graphs_section = self.get_yaml_data_by_section(self.section_name)

        if graphs_section:
            graphs = graphs_section[self.section_name]
            graph_array = list(map(lambda image: {
                            'image_name': image,
                            'image_path': f"file://{os.path.join(self.full_path, self.folder_name, image)}",
                            'rotate_90': "v1m" in image,
                            'class_name': 'single-page'
                        }, filter(lambda image: "_rotated" not in image, graphs)))

            # graphs extra processing for rotated images
            for graph in graph_array:
                if graph['rotate_90']:
                    image_path = graph['image_path'].replace("file://", "")
                    rotated_image_path = image_path.replace(".png", "_rotated.png")
                    # remove the rotate image if already exists
                    if os.path.exists(rotated_image_path):
                        os.remove(rotated_image_path)
                    # Rotate the image
                    rotate_image(image_path, rotated_image_path, -90)
                    graph['image_path'] = f"file://{rotated_image_path}"
                    graph['class_name'] = 'full-90deg'

        html_text = self._render_html_text(self.section_name, graph_array)
        self._write_pdf_file(html_text)
