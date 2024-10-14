from PIL import Image


def rotate_image(input_path, output_path, angle=-90):
    """
    Rotate the given image and save it to the output path.

    Args:
        input_path (str): The path to the input image file.
        output_path (str): The path to save the rotated image.
        angle (int): The angle to rotate the image by. Default is -90 degrees.
    """
    with Image.open(input_path) as img:
        rotated_img = img.rotate(angle, expand=True)
        rotated_img.save(output_path)


def get_image_orientation(image_path):
    """
    Get the orientation of an image.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The orientation of the image ('Horizontal' or 'Vertical').
    """
    with Image.open(image_path) as img:
        width, height = img.size
        if width > height:
            return 'Horizontal'
        else:
            return 'Vertical'
