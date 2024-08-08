import os
import markdown
from PIL import Image, ImageDraw, ImageFont
from pdf_strategy.pdf_generation_strategy import PDFGenerationStrategy
from pdf_strategy.constants import emoticon_to_unicode

MODE_R = "r"
ENCODING_UTF = "utf-8"


class GeneratePDFMdStrategy(PDFGenerationStrategy):
    def __init__(self):
        super().__init__()
        self.set_section_attributes("md")

    def generate(self, base_path, date, ticker):
        super().generate(base_path, date, ticker)

        filename = os.path.join(self.full_path, f"{self.ticker}_{self.date}_summary.md")
        with open(filename, MODE_R, encoding=ENCODING_UTF) as file:
            # Read markdown text
            markdown_text = file.read()

            # Replace emojis with image tags
            markdown_text = self._replace_emojis_with_images(markdown_text)

            # Ensure the HTML includes a meta charset tag for UTF-8
            html_text = f'<meta charset="UTF-8">\n{markdown.markdown(markdown_text, output_format="html5")}'
            self._write_pdf_file(html_text)

            # Remove the temporary emoji files
            self._remove_emoji_images()

    def _replace_emojis_with_images(self, text):
        for emoticon, unicode_char in emoticon_to_unicode.items():
            img_tag = self._create_emoji_image(unicode_char)
            text = text.replace(emoticon, img_tag)
        return text

    # TODO: NTH -- color emojis
    def _create_emoji_image(self, unicode_char):
        try:
            # Create an image for the emoji
            font_path = "/System/Library/Fonts/Apple Color Emoji.ttc"
            font_size = 64  # Use a smaller font size
            font = ImageFont.truetype(font_path, font_size)
            image = Image.new("RGBA", (64, 64), (255, 255, 255, 0))
            draw = ImageDraw.Draw(image)
            draw.text((0, 0), unicode_char, font=font, fill="black")

            # Save the image
            img_path = os.path.join(self.full_path, f"{unicode_char}.png")
            image.save(img_path)

            # Return the HTML image tag
            return f'<img src="{img_path}" alt="{unicode_char}" width="20" height="20">'
        except OSError as e:
            print(f"Error creating emoji image: {e}")
            return unicode_char  # Fallback to unicode character if image creation fails

    def _remove_emoji_images(self):
        for img_file in os.listdir(self.full_path):
            if img_file.endswith(".png"):
                os.remove(os.path.join(self.full_path, img_file))