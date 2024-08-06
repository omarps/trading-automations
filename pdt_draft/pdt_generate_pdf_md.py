import os
import markdown
import pdfkit
import emoji

def generate_pdf_md(base_path, date, ticker):
    # file_path = os.path.join(base_path, date)
    file_path = base_path
    filename = os.path.join(file_path, f"{ticker}_{date}_summary.md")
    mode = "r"
    encoding = "utf-8"

    with open(filename, mode, encoding=encoding) as file:
        markdown_text = file.read()
        # Fix color emojis -- NA
        # markdown_text = emoji.emojize(markdown_text, language='alias')

        # Ensure the HTML includes a meta charset tag for UTF-8
        html_text = f'<meta charset="UTF-8">\n{markdown.markdown(markdown_text, output_format="html5")}'

        # Specify the path to your custom CSS file
        css_path = os.path.join(os.path.dirname(__file__), 'styles.css')
        options = {
            'user-style-sheet': css_path
        }
        pdfkit.from_string(html_text, os.path.join(file_path, f"{ticker}_{date}_pdt.pdf"), options=options)

if __name__ == "__main__":
    base_path = "/Users/omarps/Downloads/pdt"  # Replace with the path to your base folder
    # base_path = "/Users/omarps/Library/CloudStorage/OneDrive-Personal/Proyectos/CDI/PDT/2024/2024q3"  # Replace with the path to your base folder
    date = "20240719"  # Replace with the date
    ticker = "SPY"  # Replace with the ticker
    generate_pdf_md(base_path, date, ticker)
