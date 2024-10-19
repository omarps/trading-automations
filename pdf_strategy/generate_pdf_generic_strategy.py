import os
from pdf_strategy.pdf_generation_strategy import PDFGenerationStrategy


class GeneratePDFGenericStrategy(PDFGenerationStrategy):
    def __init__(self, section_name, folder_name=None, suffix=None):
        super().__init__()
        self.set_section_attributes(section_name, folder_name)
        self.suffix = suffix

    def generate(self, base_path, date, ticker):
        super().generate(base_path, date, ticker)

        # Read YAML file
        section = self.get_yaml_data_by_section(self.section_name)

        if section:
            section_data = section[self.section_name]

            data = list(map(lambda image_tuple: {
                'image_name': image_tuple[1],
                'image_path': f"file:///{os.path.join(self.full_path, self.folder_name, image_tuple[1])}",
                'pagebreak': (image_tuple[0] + 1) % 2 == 0,
                'index': image_tuple[0] + 1
            }, enumerate(section_data)))

        html_text = self._render_html_text(self.section_name, data)

        self._write_pdf_file(html_text)
