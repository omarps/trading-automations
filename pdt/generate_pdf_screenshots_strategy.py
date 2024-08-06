import os
from pdf_generation_strategy import PDFGenerationStrategy


class GeneratePDFScreenshotsStrategy(PDFGenerationStrategy):
    def __init__(self):
        super().__init__()
        self.set_section_attributes('screenshots', 'screenshots')

    def generate(self, base_path, date, ticker):
        super().generate(base_path, date, ticker)

        # Read YAML file
        screenshots_section = self.get_yaml_data_by_section(self.section_name)

        if screenshots_section:
            screenshots = screenshots_section[self.section_name]

            screenshot_array = list(map(lambda image_tuple: {
                'image_name': image_tuple[1],
                'image_path': f"file:///{os.path.join(self.full_path, self.folder_name, image_tuple[1])}",
                'pagebreak': (image_tuple[0] + 1) % 2 == 0,
                'index': image_tuple[0] + 1
            }, enumerate(screenshots)))

        html_text = self._render_html_text(self.section_name, screenshot_array)

        # # Write the HTML text to the file
        # output_file_path = os.path.join(self.full_path, "screenshots.html")
        # with open(output_file_path, "w", encoding="utf-8") as file:
        #     file.write(html_text)

        self._write_pdf_file(html_text)
