import os
from pdf_generation_strategy import PDFGenerationStrategy


class GeneratePDFGammasStrategy(PDFGenerationStrategy):
    def __init__(self):
        super().__init__()
        self.set_section_attributes('gammas', 'gammas')

    def generate(self, base_path, date, ticker):
        super().generate(base_path, date, ticker)

        # Read YAML file
        gammas_section = self.get_yaml_data_by_section(self.section_name)

        if gammas_section:
            gammas = gammas_section[self.section_name]

            gamma_array = list(map(lambda image_tuple: {
                'image_name': image_tuple[1],
                'image_path': f"file:///{os.path.join(self.full_path, self.folder_name, image_tuple[1])}",
                'pagebreak': (image_tuple[0] + 1) % 2 == 0,
                'index': image_tuple[0] + 1
            }, enumerate(gammas)))

        html_text = self._render_html_text(self.section_name, gamma_array)
        self._write_pdf_file(html_text)
