import os
from pdf_strategy.pdf_generation_strategy import PDFGenerationStrategy
from utils.constants import OPTIONS, CONTRATOS


class GeneratePDFOptionsStrategy(PDFGenerationStrategy):
    def __init__(self):
        super().__init__()
        self.set_section_attributes(OPTIONS, CONTRATOS)

    def generate(self, base_path, date, ticker):
        super().generate(base_path, date, ticker)

        # Read YAML file
        options_section = self.get_yaml_data_by_section(self.section_name)

        if options_section:
            options = options_section[self.section_name]

            option_array = list(map(lambda option: {
                'name': option['name'],
                "transactions": option['transactions'],
                "strikes": option['strikes'] if 'strikes' in option else '',
                'option_images': list(map(lambda image_tuple: {
                    'image_name': image_tuple[1],
                    'image_path': f"file:///{os.path.join(self.full_path, self.folder_name, option['name'], image_tuple[1])}",
                    'pagebreak': (image_tuple[0] + 1) % 2 == 0,
                    'index': image_tuple[0] + 1
                }, enumerate(option['images'])))
            }, options))

        html_text = self._render_html_text(self.section_name, option_array)
        self._write_pdf_file(html_text)
