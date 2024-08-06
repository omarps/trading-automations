import os
import markdown2
import yaml
import emoji
from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image, ImageOps
from html.parser import HTMLParser

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.current_image_name = ''

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", 'I', 8)
        self.cell(0, 10, f"Image: {self.current_image_name}", 0, 0, 'C')

    def add_section_title(self, title):
        self.set_font("Helvetica", 'B', 14)
        self.cell(200, 10, txt=title, ln=True)
        self.ln(10)

    def add_image_full_page(self, image_path, rotate_90=False):
        self.current_image_name = os.path.basename(image_path)
        self.add_page()
        try:
            with Image.open(image_path) as img:
                # fix the rotation -- NA
                # if rotate_90:
                  # img = img.rotate(90, expand=True)
                  # img = ImageOps.exif_transpose(img, in_place=True)
                  # img= rotated.resize((int(width), int(height)), Image.ANTIALIAS)
                img_width, img_height = img.size
                # Calculate aspect ratio to fit the image on a full page with a 0.75 factor
                aspect_ratio = (img_width / img_height) * 0.75
                page_width = self.w - 2 * self.l_margin
                page_height = self.h - 2 * self.t_margin
                if aspect_ratio > 1:
                    width = page_width
                    height = page_width / aspect_ratio
                else:
                    height = page_height
                    width = page_height * aspect_ratio
                self.image(image_path, x=self.l_margin, y=self.t_margin, w=width, h=height)
        except Exception as e:
            print(f"Error adding image {image_path}: {e}")

    def add_images_two_per_page_vertically(self, image_paths):
        for i in range(0, len(image_paths), 2):
            self.add_page()
            for j in range(2):
                if i + j < len(image_paths):
                    image_path = image_paths[i + j]
                    self.current_image_name = os.path.basename(image_path)
                    y_offset = self.t_margin if j == 0 else self.h / 2
                    try:
                        with Image.open(image_path) as img:
                            img_width, img_height = img.size
                            aspect_ratio = img_width / img_height
                            page_width = self.w - 2 * self.l_margin
                            page_height = (self.h / 2) - self.t_margin * 1.5
                            if aspect_ratio > 1:
                                width = page_width
                                height = page_width / aspect_ratio
                            else:
                                height = page_height
                                width = page_height * aspect_ratio
                            self.image(image_path, x=self.l_margin, y=y_offset, w=width, h=height)
                    except Exception as e:
                        print(f"Error adding image {image_path}: {e}")

def add_pdf_to_pdf(main_pdf_path, add_pdf_path):
    main_pdf = PdfReader(main_pdf_path)
    add_pdf = PdfReader(add_pdf_path)
    writer = PdfWriter()
    
    for page in main_pdf.pages:
        writer.add_page(page)
    
    for page in add_pdf.pages:
        writer.add_page(page)
    
    with open(main_pdf_path, "wb") as f_out:
        writer.write(f_out)

def generate_pdf_from_yaml(base_path, date, ticker):
    full_path = os.path.join(base_path, date)
    yaml_file_path = os.path.join(full_path, f"{ticker}_{date}_summary.yaml")

    # Read YAML file
    with open(yaml_file_path, 'r') as file:
        summary_data = yaml.safe_load(file)

    # Create PDF
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(200, 10, txt=summary_data['title'], ln=True, align='C')
    pdf.ln(10)

    # generate pdt.pdf -- NA

    # Add summary content
    # add_pdf_to_pdf(f"{full_path}/{ticker}_{date}_summary.pdf", f"{full_path}/{ticker}_{date}_pdt.pdf")

    # Process sections
    for section in summary_data['sections']:
        for section_name, images in section.items():
            pdf.add_page()
            pdf.add_section_title(section_name.capitalize())

            if section_name == 'graphs':
                folder_name = 'graficos'
                for image_name in images:
                    image_path = os.path.join(full_path, folder_name, image_name)
                    rotate_90 = "v1m" in image_name
                    pdf.add_image_full_page(image_path, rotate_90)
            elif section_name == 'options':
                folder_name = 'contratos'
                for option in images:
                    for option_name, option_images in option.items():
                        pdf.add_section_title(option_name)
                        image_paths = [os.path.join(full_path, folder_name, option_name, image_name) for image_name in option_images]
                        pdf.add_images_two_per_page_vertically(image_paths)
            elif section_name == 'gammas':
                folder_name = 'gammas'
                image_paths = [os.path.join(full_path, folder_name, image_name) for image_name in images]
                pdf.add_images_two_per_page_vertically(image_paths)


    # Save PDF
    pdf_file_path = os.path.join(full_path, f"{ticker}_{date}_summary.pdf")
    pdf.output(pdf_file_path)

    add_pdf_to_pdf(f"{full_path}/{ticker}_{date}_summary.pdf", f"{full_path}/{ticker}_{date}_pdt.pdf")
    print(f"PDF file created: {pdf_file_path}")

if __name__ == "__main__":
    base_path = "/Users/omarps/Library/CloudStorage/OneDrive-Personal/Proyectos/CDI/PDT/2024/2024q3"  # Replace with the path to your base folder
    date = "20240718"  # Replace with the date
    ticker = "SPY"  # Replace with the ticker
    generate_pdf_from_yaml(base_path, date, ticker)
