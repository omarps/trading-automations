import os
import markdown
import shutil
import re
import json
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
from pdf_strategy.pdf_generation_strategy import PDFGenerationStrategy
from pdf_strategy.constants import emoticon_to_unicode
from utils.constants import MD

MODE_R = "r"
ENCODING_UTF = "utf-8"
RESOURCE_FILE = 'emoticon_to_unicode.json'


load_dotenv()


class GeneratePDFMdStrategy(PDFGenerationStrategy):
    """
    Class for generating PDF reports from markdown files.

    This class extends the `PDFGenerationStrategy` to provide functionality for generating
    PDF reports from markdown files. It reads the markdown content, replaces emojis with
    image tags, converts the markdown to HTML, and writes the HTML to a PDF file. Temporary
    emoji image files are created and removed during the process.
    """

    def __init__(self, suffix=None):
        """
        Initializes the `GeneratePDFMdStrategy` instance and sets the section attributes to "utils".

        Args:
            suffix (str, optional): The suffix to be added to the PDF filename. Default is None.
        """
        super().__init__()
        self.set_section_attributes(MD)
        self.suffix = suffix

    def generate(self, base_path, date, ticker):
        """
        Generates the PDF from the markdown file.

        Args:
            base_path (str): The base path where the markdown file is located.
            date (str): The date associated with the file.
            ticker (str): The ticker symbol associated with the file.
            suffix (str, optional): The suffix to be added to the PDF filename. Default is None.
        """
        super().generate(base_path, date, ticker)

        filename = os.path.join(self._full_path(), f"{self.ticker}_{self.date}_summary.md")
        with open(filename, MODE_R, encoding=ENCODING_UTF) as file:
            # Read markdown text
            markdown_text = file.read()

            # TODO: Look for a better way to handle new emojis

            # Replace emojis with image tags
            markdown_text = self._replace_emojis_with_images(markdown_text)
            # markdown_text = self.replace_emojis_with_images(markdown_text)

            # Ensure the HTML includes a meta charset tag for UTF-8
            html_text = f'<meta charset="UTF-8">\n{markdown.markdown(markdown_text, output_format="html5")}'
            self._write_pdf_file(html_text)

            # Remove the temporary emoji files
            self._remove_emoji_images()

    def load_emoticon_to_unicode(self):
        resource_path = os.path.join(os.path.dirname(__file__), "../templates", RESOURCE_FILE)
        with open(resource_path, 'r', encoding='utf-8') as file:
            emoticon_to_unicode = json.load(file)

        # Process the Unicode representations to handle escaped backslashes
        for emoji, unicode_repr in emoticon_to_unicode.items():
            emoticon_to_unicode[emoji] = unicode_repr.encode('utf-8').decode('raw_unicode_escape')

        return emoticon_to_unicode

    def save_emoticon_to_unicode(self, emoticon_to_unicode):
        resource_path = os.path.join(os.path.dirname(__file__), "../templates", RESOURCE_FILE)
        with open(resource_path, 'w', encoding='utf-8') as file:
            json.dump(emoticon_to_unicode, file, ensure_ascii=False, indent=4)

    def update_emoticon_to_unicode(self, new_emojis):
        emoticon_to_unicode = self.load_emoticon_to_unicode()
        updated = False

        for emoji in new_emojis:
            if emoji not in emoticon_to_unicode:
                # Convert emoji to Unicode code points
                unicode_repr = ''.join(f"\\U{ord(char):08X}" for char in emoji)
                emoticon_to_unicode[emoji] = unicode_repr
                updated = True

        if updated:
            self.save_emoticon_to_unicode(emoticon_to_unicode)

    def replace_emojis_with_images(self, md_content):
        emoticon_to_unicode = self.load_emoticon_to_unicode()

        # Updated regex to match emojis
        emoji_pattern = re.compile(
            "[\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F700-\U0001F77F"  # alchemical symbols
            "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
            "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            "\U0001FA00-\U0001FA6F"  # Chess Symbols
            "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
            "\U00002702-\U000027B0"  # Dingbats
            "\U000024C2-\U0001F251"  # Enclosed characters
            "]+", flags=re.UNICODE)

        new_emojis = set(emoji_pattern.findall(md_content)) - set(emoticon_to_unicode.keys())

        if new_emojis:
            self.update_emoticon_to_unicode(new_emojis)
            emoticon_to_unicode = self.load_emoticon_to_unicode()

        for emoji, unicode in emoticon_to_unicode.items():
            img_tag = self._create_emoji_image(unicode)
            md_content = md_content.replace(emoji, img_tag)

        return md_content

    def _replace_emojis_with_images(self, text):
        """
        Replaces emojis in the text with corresponding image tags.

        Args:
            text (str): The text containing emojis.

        Returns:
            str: The text with emojis replaced by image tags.
        """
        for emoticon, unicode_char in emoticon_to_unicode.items():
            img_tag = self._create_emoji_image(unicode_char)
            text = text.replace(emoticon, img_tag)
        return text

    # TODO: NTH -- color emojis
    def _create_emoji_image(self, unicode_char):
        """
        Creates an image for the given emoji character.

        Args:
            unicode_char (str): The unicode character of the emoji.

        Returns:
            str: The HTML image tag for the emoji or the unicode character if image creation fails.
        """
        try:
            # Create an image for the emoji
            font_path = os.getenv("FONT_PATH", "/System/Library/Fonts/Apple Color Emoji.ttc")
            font_size = 64  # Use a smaller font size
            font = ImageFont.truetype(font_path, font_size)
            image = Image.new("RGBA", (64, 64), (255, 255, 255, 0))
            draw = ImageDraw.Draw(image)
            draw.text((0, 0), unicode_char, font=font, fill="black")

            # Save the image
            img_folder = os.path.join(self.full_path, "emoji_images")
            if not os.path.exists(img_folder):
                os.makedirs(img_folder)
            img_path = os.path.join(img_folder, f"{unicode_char}.png")
            image.save(img_path)

            # Return the HTML image tag
            return f'<img src="{img_path}" alt="{unicode_char}" width="20" height="20">'
        except OSError as e:
            print(f"Error creating emoji image: {e}. Font path: {font_path}")
            return unicode_char  # Fallback to unicode character if image creation fails

    def _remove_emoji_images(self):
        """
        Removes temporary emoji image folder.
        """
        img_folder = os.path.join(self.full_path, "emoji_images")
        if os.path.exists(img_folder):
            shutil.rmtree(img_folder)
