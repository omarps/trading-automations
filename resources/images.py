from PIL import Image


def rotate_image(input_path, output_path, angle=-90):
    """Rotate the given image and save it to the output path."""
    with Image.open(input_path) as img:
        rotated_img = img.rotate(angle, expand=True)
        rotated_img.save(output_path)
