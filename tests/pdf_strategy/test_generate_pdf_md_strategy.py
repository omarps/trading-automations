import unittest
from unittest.mock import patch, mock_open
from pdf_strategy.generate_pdf_md_strategy import GeneratePDFMdStrategy


class TestGeneratePDFMdStrategy(unittest.TestCase):
    def setUp(self):
        self.strategy = GeneratePDFMdStrategy()

    @patch("builtins.open", new_callable=mock_open, read_data="# Markdown content")
    @patch("os.path.join", return_value="fake_path")
    @patch("markdown.markdown", return_value="<p>HTML content</p>")
    def test_generate(self, mock_markdown, mock_join, mock_open):
        with patch.object(self.strategy, "_write_pdf_file") as mock_write_pdf_file, \
             patch.object(self.strategy, "_remove_emoji_images") as mock_remove_emoji_images:
            self.strategy.generate("base_path", "date", "ticker")
            mock_write_pdf_file.assert_called_once_with('<meta charset="UTF-8">\n<p>HTML content</p>')
            mock_remove_emoji_images.assert_called_once()

    @patch("os.path.join", return_value="fake_path")
    @patch("os.remove")
    def test_remove_emoji_images(self, mock_remove, mock_join):
        with patch("os.listdir", return_value=["emoji1.png", "emoji2.png"]):
            self.strategy._remove_emoji_images()
            self.assertEqual(mock_remove.call_count, 2)

    @patch("os.path.join", return_value="fake_path")
    @patch("PIL.ImageFont.truetype", side_effect=OSError("cannot open resource"))
    @patch("PIL.ImageDraw.Draw")
    @patch("PIL.Image.Image.save")
    def test_create_emoji_image(self, mock_save, mock_draw, mock_truetype, mock_join):
        mock_draw_instance = mock_draw.return_value
        img_tag = self.strategy._create_emoji_image("😊")
        self.assertIn("😊", img_tag)  # Fallback to unicode character if image creation fails
        mock_truetype.assert_called_once()
        mock_save.assert_not_called()
        mock_draw_instance.text.assert_not_called()


if __name__ == "__main__":
    unittest.main()
